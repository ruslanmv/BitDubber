import pyautogui
from PIL import Image
import pandas as pd
import gradio as gr
import os
import base64
import requests
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to take a screenshot
def take_screenshot(output_path="screenshot.png"):
    try:
        pyautogui.screenshot(output_path)
        logging.info(f"Screenshot saved to {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"Error taking screenshot: {e}")
        return f"Error: {e}"

# Function to encode the image in base64
def get_encoded_string(file_name):
    try:
        with open(file_name, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        logging.error(f"Error encoding image: {e}")
        return f"Error: {e}"

# Function to get the IBM Cloud access token
def get_auth_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    data = {"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": api_key}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

# Function to send the screenshot to LLaMA 3.2 for UI element detection
def identify_ui_elements_with_llama32(screenshot_path):
    try:
        api_key = os.getenv("WATSONX_APIKEY")
        access_token = get_auth_token(api_key)
        encoded_image = get_encoded_string(screenshot_path)

        url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"
        body = {
            "messages": [
                {"role": "system", "content": "Extract UI elements from the image."},
                {"role": "user", "content": encoded_image}
            ],
            "project_id": os.getenv("PROJECT_ID"),
            "model_id": "meta-llama/llama-3-2-90b-vision-instruct",
        }
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()

        # Simulate output
        elements = [
            {"coordinates": (50, 100), "description": "URL Bar"},
            {"coordinates": (200, 300), "description": "Search Button"}
        ]
        df = pd.DataFrame(elements)
        csv_path = "ui_elements.csv"
        df.to_csv(csv_path, index=False)
        logging.info(f"UI elements saved to {csv_path}")
        return csv_path
    except Exception as e:
        logging.error(f"Error identifying UI elements: {e}")
        return f"Error: {e}"

# Function to determine click sequence using LLaMA 3.1
def determine_click_sequence_with_llama31(user_request, csv_path):
    try:
        df = pd.read_csv(csv_path)
        if "wikipedia" in user_request.lower():
            return [
                {"action": "click", "coordinates": (50, 100)},
                {"action": "type", "text": "https://www.wikipedia.org"},
                {"action": "press", "key": "enter"}
            ]
        return []
    except Exception as e:
        logging.error(f"Error determining click sequence: {e}")
        return f"Error: {e}"

# Function to execute the click sequence
def execute_click_sequence(click_sequence):
    try:
        for action in click_sequence:
            if action["action"] == "click":
                pyautogui.moveTo(*action["coordinates"])
                pyautogui.click()
            elif action["action"] == "type":
                pyautogui.typewrite(action["text"])
            elif action["action"] == "press":
                pyautogui.press(action["key"])
        logging.info("Execution completed.")
        return "Execution completed."
    except Exception as e:
        logging.error(f"Error executing click sequence: {e}")
        return f"Error: {e}"

# Gradio Interface
def handle_user_request(user_request):
    screenshot_path = take_screenshot()
    if "Error" in screenshot_path:
        return screenshot_path

    csv_path = identify_ui_elements_with_llama32(screenshot_path)
    if "Error" in csv_path:
        return csv_path

    click_sequence = determine_click_sequence_with_llama31(user_request, csv_path)
    if not click_sequence:
        return "No valid actions determined."

    print("Planned sequence of actions:")
    for action in click_sequence:
        print(action)
    confirm = input("Do you want to execute these actions? (yes/no): ")
    if confirm.lower() != "yes":
        return "Execution cancelled by the user."

    return execute_click_sequence(click_sequence)

# Gradio Interface Setup
interface = gr.Interface(
    fn=handle_user_request,
    inputs="text",
    outputs="text",
    title="BitDubber: Automated UI Interaction",
    description="Provide a command, and the program will identify UI elements and perform actions accordingly."
)

if __name__ == "__main__":
    interface.launch()
