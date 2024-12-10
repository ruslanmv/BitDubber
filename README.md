# Building BitDubber: Your Smart Desktop Assistant

## Introduction

BitDubber is an intelligent desktop assistant designed to read your screen, understand its content, and perform tasks based on your voice commands. By combining advanced screen-reading capabilities with LLaMA 3.2 and LLaMA 3.1 models, and integrating IBM Watson's Text-to-Speech (TTS) and Speech-to-Text (STT) services, BitDubber provides a seamless user experience for automating desktop activities with voice interactions. This guide walks you through building BitDubber step by step, using the improved Python script and new architecture.

---

## Features

- **Screen Analysis**: Captures the current screen and identifies clickable UI elements.
- **Voice Command Interpretation**: Processes voice commands to understand and determine tasks.
- **Automated Actions**: Executes mouse clicks, keyboard inputs, and other actions to fulfill user requests.
- **Speech Integration**: Uses IBM Watson services for speech-to-text (STT) and text-to-speech (TTS) conversions.
- **Confirmation Pipeline**: Displays planned actions for user confirmation before execution.
- **User-Friendly Interface**: Provides a Gradio-based front end for interactive command input.

---

## Prerequisites

To get started, ensure the following are installed:

1. Python 3.8 or higher.
2. Required Python libraries:
   ```bash
   pip install pyautogui pillow pandas gradio requests python-dotenv ibm-watson
   ```
3. Proper system permissions to capture screenshots and control mouse/keyboard actions.
4. IBM Watson Speech-to-Text (STT) and Text-to-Speech (TTS) API credentials.

---

## Setting Up IBM Watson Services

### 1. Create IBM Cloud Account
- Go to [IBM Cloud](https://cloud.ibm.com/) and create a free account if you don’t already have one.

### 2. Create Speech-to-Text and Text-to-Speech Services
- Navigate to the **Catalog** and search for `Speech-to-Text` and `Text-to-Speech`.
- Create an instance for both services.

### 3. Retrieve API Keys and URLs
- For each service, go to the **Service Credentials** section in the IBM Cloud dashboard.
- Copy the API Key and URL.

### 4. Update the `.env` File
Create a `.env` file in the project directory and add the following:
```plaintext
TTS_API_KEY=your_text_to_speech_api_key
TTS_URL=your_text_to_speech_service_url
STT_API_KEY=your_speech_to_text_api_key
STT_URL=your_speech_to_text_service_url
WATSONX_APIKEY=your_llama_service_api_key
PROJECT_ID=your_project_id
```

Replace the placeholders with the actual credentials.

---

## Workflow Overview

1. **Speech-to-Text Conversion (STT)**:
   - Captures audio input and converts it to text using IBM Watson's STT service.

2. **Screenshot Capture**:
   - Takes a screenshot of the desktop using `pyautogui`.

3. **UI Elements Identification (LLaMA 3.2)**:
   - Sends the screenshot to LLaMA 3.2 to detect clickable UI elements and saves their coordinates and descriptions in a CSV file.

4. **Request Interpretation (LLaMA 3.1)**:
   - Reads the CSV file and sends a new prompt to LLaMA 3.1 to map the user's voice commands to a sequence of actions (e.g., mouse clicks, keyboard inputs).

5. **Text-to-Speech Conversion (TTS)**:
   - Converts the planned sequence of actions into speech for user confirmation.

6. **Confirmation Pipeline**:
   - Displays the planned sequence of actions and asks for user confirmation before proceeding.

7. **Action Execution**:
   - Executes the planned sequence of actions using `pyautogui` to fulfill the user's request.

8. **Interactive Gradio Frontend**:
   - Allows users to input audio commands and view results interactively.

---

## Step-by-Step Guide

### 1. Setting Up the Project

- Create a project directory and name it `BitDubber`.
- Inside the directory, create the Python script `bitdubber.py` and paste the provided code.

### 2. Running the Application

- Launch the application by running:
  ```bash
  python bitdubber.py
  ```
- Access the Gradio interface in your web browser at the provided URL.

For more details of the setup click [here](setup.md)
---

## Example Workflow

### Input: Speak "Open Wikipedia"
1. **Speech-to-Text Conversion**: Captures the audio input and converts it to the text command: `"Open Wikipedia"`.
2. **Screenshot**: Takes a screenshot of the desktop.
3. **LLaMA 3.2 Processing**: Identifies UI elements (e.g., URL bar, search button) and saves them in `ui_elements.csv`.
4. **LLaMA 3.1 Processing**: Maps the command to actions:
   - Click the URL bar.
   - Type `https://www.wikipedia.org`.
   - Press Enter.
5. **Text-to-Speech Conversion**: Converts the planned actions to speech for user confirmation.
6. **User Confirmation**: Confirms the execution of planned actions.
7. **Action Execution**: Opens the browser, navigates to Wikipedia, and confirms the action.

---

## Key Components Explained

### Speech-to-Text Conversion
Converts audio input to text using:
```python
response = speech_to_text.recognize(
    audio=audio_file,
    content_type='audio/wav'
).get_result()
text = response['results'][0]['alternatives'][0]['transcript']
```

### Text-to-Speech Conversion
Converts text to audio using:
```python
response = text_to_speech.synthesize(
    text="Planned sequence of actions",
    voice="en-US_AllisonVoice",
    accept="audio/wav"
).get_result()
```

### Gradio Integration
Captures audio input and processes it:
```python
interface = gr.Interface(
    fn=handle_user_request,
    inputs=gr.Audio(source="microphone", type="filepath"),
    outputs="text",
    title="BitDubber: Automated UI Interaction with Speech",
    description="Speak a command, and the program will identify UI elements and perform actions accordingly."
)
```

---

## Future Enhancements

- **Dynamic LLaMA Integration**: Replace simulations with real LLaMA 3.2 and 3.1 interactions.
- **Improved Speech Recognition**: Enhance STT accuracy with custom language models.
- **Advanced Action Mapping**: Handle more complex workflows and edge cases.
- **Multi-Platform Support**: Extend functionality to Mac and Linux.

---
### Build BitDubber Today and Transform Your Desktop Experience!
