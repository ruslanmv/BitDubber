# Setup Guide for BitDubber

This guide walks you through setting up the Python environment and installing the necessary dependencies for running BitDubber. Follow these steps carefully to ensure a seamless installation process.

---

## Prerequisites

Before setting up the environment, ensure the following:

1. **Python 3.10 Installed**:
   - Download and install Python 3.10 from the [official Python website](https://www.python.org/downloads/).
   - Verify the installation:
     ```bash
     python3 --version
     ```
     Ensure it outputs a version string starting with `3.10`.

2. **Git Installed**:
   - Download and install Git from the [official Git website](https://git-scm.com/).
   - Verify the installation:
     ```bash
     git --version
     ```

3. **IBM Cloud Credentials**:
   - Ensure you have API keys and service URLs for IBM Watson Speech-to-Text (STT) and Text-to-Speech (TTS).
   - Instructions to obtain these can be found in the main `README.md` file.

---

## Step-by-Step Setup

### 1. Clone the Repository

Clone the BitDubber project repository from GitHub:
```bash
git clone <repository-url>
cd <repository-directory>
```
Replace `<repository-url>` with the actual URL of the repository.

### 2. Create a Virtual Environment

It is recommended to create a virtual environment to manage project dependencies.

1. Create the virtual environment in a `.venv` folder:
   ```bash
   python3 -m venv .venv
   ```

2. Activate the virtual environment:
   - On Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

   You should see `(.venv)` at the beginning of your terminal prompt, indicating that the environment is active.

### 3. Install Required Python Libraries

Install the necessary Python packages:
```bash
pip install --upgrade pip
pip install pyautogui pillow pandas gradio requests python-dotenv ibm-watson
```

### 4. Set Up the `.env` File

Create a `.env` file in the root directory of the project and add the following credentials:
```plaintext
TTS_API_KEY=your_text_to_speech_api_key
TTS_URL=your_text_to_speech_service_url
STT_API_KEY=your_speech_to_text_api_key
STT_URL=your_speech_to_text_service_url
WATSONX_APIKEY=your_llama_service_api_key
PROJECT_ID=your_project_id
```
Replace the placeholders with the actual credentials obtained from IBM Cloud.

### 5. Verify Installation

Run the following command to verify the installation:
```bash
python bitdubber.py
```
This should start the Gradio interface and provide a local URL. Open the URL in your browser to test the application.

---

## Additional Notes

- **Deactivate Virtual Environment**:
  When you're done working, deactivate the virtual environment:
  ```bash
  deactivate
  ```

- **Reactivating Virtual Environment**:
  To work on the project again, navigate to the project directory and activate the environment:
  ```bash
  source .venv/bin/activate
  ```

- **Updating Dependencies**:
  If additional dependencies are added to the project, update your environment:
  ```bash
  pip install -r requirements.txt
  ```

- **Optional**: Export Installed Libraries
  You can export the current environment's dependencies to a `requirements.txt` file:
  ```bash
  pip freeze > requirements.txt
  ```

