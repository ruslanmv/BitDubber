# Building BitDubber: Your Smart Desktop Assistant

## Introduction

BitDubber is an intelligent desktop assistant designed to read your screen, understand its content, and perform tasks based on your voice commands. Combining advanced screen-reading capabilities with LLaMA 3.2 and LLaMA 3.1 models, BitDubber provides a seamless user experience, automating desktop activities with voice interactions. This guide walks you through how to build BitDubber step by step, using the improved Python script and new architecture.

---

## Features

- **Screen Analysis**: Captures the current screen and identifies clickable UI elements.
- **Voice Command Interpretation**: Processes voice commands to understand and determine tasks.
- **Automated Actions**: Executes mouse clicks, keyboard inputs, and other actions to fulfill user requests.
- **Confirmation Pipeline**: Displays planned actions for user confirmation before execution.
- **User-Friendly Interface**: Provides a Gradio-based front end for interactive command input.

---

## Prerequisites

To get started, ensure the following are installed:

1. Python 3.8 or higher
2. Required Python libraries:
   ```bash
   pip install pyautogui pillow pandas gradio requests python-dotenv
   ```
3. Proper system permissions to capture screenshots and control mouse/keyboard actions.
4. A development environment with access to LLaMA models (3.2 and 3.1).

---

## Workflow Overview

1. **Screenshot Capture**:
   - Takes a screenshot of the desktop using `pyautogui`.

2. **UI Elements Identification (LLaMA 3.2)**:
   - Sends the screenshot to LLaMA 3.2 to detect clickable UI elements and saves their coordinates and descriptions in a CSV file.

3. **Request Interpretation (LLaMA 3.1)**:
   - Reads the CSV file and sends a new prompt to LLaMA 3.1 to map user voice commands to a sequence of actions (e.g., mouse clicks, keyboard inputs).

4. **Confirmation Pipeline**:
   - Displays the planned sequence of actions and asks for user confirmation before proceeding.

5. **Action Execution**:
   - Executes the planned sequence of actions using `pyautogui` to fulfill the user request.

6. **Interactive Gradio Frontend**:
   - Allows users to input commands and view results interactively.

---

## Step-by-Step Guide

### 1. Setting Up the Project

- Create a project directory and name it `BitDubber`.
- Inside the directory, create the Python script `bitdubber.py` and paste the improved code.

### 2. Understanding the Script

#### Core Functions

- **take_screenshot**: Captures the current desktop view and saves it as `screenshot.png`.
- **identify_ui_elements_with_llama32**: Sends the screenshot to LLaMA 3.2 to detect UI elements and saves them in `ui_elements.csv`.
- **determine_click_sequence_with_llama31**: Sends the CSV data and user request to LLaMA 3.1 to generate a sequence of actions.
- **confirmation_pipeline**: Displays the planned sequence of actions and waits for user confirmation before proceeding.
- **execute_click_sequence**: Executes the sequence of actions using `pyautogui`.

#### Gradio Frontend

- Provides an interactive interface for users to input commands and view results.

### 3. Running the Application

- Launch the application by running:
  ```bash
  python bitdubber.py
  ```
- Access the Gradio interface in your web browser at the provided URL.

### 4. Testing the Application

#### Example Workflow

- Input: `"Open Wikipedia"`
- Steps:
  1. Screenshot is taken.
  2. LLaMA 3.2 identifies UI elements (e.g., URL bar, search button) and saves them in `ui_elements.csv`.
  3. LLaMA 3.1 generates a sequence:
     - Click URL bar.
     - Type `https://www.wikipedia.org`.
     - Press Enter.
  4. Planned sequence is displayed for confirmation.
  5. Actions are executed upon user confirmation.

#### Expected Output

- The browser navigates to Wikipedia.
- The Gradio interface confirms execution.

---

## Key Components Explained

### Screenshot Capture
- Captures the screen using:
  ```python
  pyautogui.screenshot(output_path)
  ```
- Saves as `screenshot.png`.

### UI Elements Detection
- Sends the screenshot to LLaMA 3.2 to detect clickable elements:
  ```python
  encoded_string = get_encoded_string(screenshot_path)
  access_token = get_auth_token(os.getenv("WATSONX_APIKEY"))
  elements = extraction_request(encoded_string, access_token)
  save_to_csv(elements, "ui_elements.csv")
  ```

### Request Processing
- Maps voice commands to actions using LLaMA 3.1:
  ```python
  if "wikipedia" in user_request.lower():
      return [
          {"action": "click", "coordinates": (50, 100)},
          {"action": "type", "text": "https://www.wikipedia.org"},
          {"action": "press", "key": "enter"}
      ]
  ```

### Confirmation Pipeline
- Displays the planned sequence and waits for confirmation:
  ```python
  print("Planned sequence of actions:")
  for action in click_sequence:
      print(action)
  confirm = input("Do you want to execute these actions? (yes/no): ")
  if confirm.lower() != "yes":
      return "Execution cancelled by the user."
  ```

### Action Execution
- Performs the sequence using:
  ```python
  pyautogui.moveTo(x, y)
  pyautogui.click()
  pyautogui.typewrite(action["text"])
  pyautogui.press(action["key"])
  ```

### Gradio Frontend
- Provides a simple interface:
  ```python
  interface = gr.Interface(
      fn=handle_user_request,
      inputs="text",
      outputs="text",
      title="BitDubber: Automated UI Interaction",
      description="Provide a command, and the program will identify UI elements and perform actions accordingly."
  )
  ```

---

## Future Enhancements

- **Dynamic LLaMA Integration**: Replace simulations with real LLaMA 3.2 and 3.1 interactions.
- **Advanced Action Mapping**: Improve request-to-action mapping for complex workflows.
- **Voice Input**: Add direct voice command recognition.
- **Multi-Platform Support**: Extend functionality to Mac and Linux.

---

## Coming Soon

BitDubber is in active development, with future updates bringing:
- Enhanced AI capabilities.
- Expanded application support.
- A fully functional AI-driven desktop assistant.

Stay tuned for updates!

---


---

### Build BitDubber Today and Transform Your Desktop Experience!

