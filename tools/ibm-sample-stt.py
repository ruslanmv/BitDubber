import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import threading

# Constants (replace these with your own values)
API_KEY = 'APIKEY'  # Replace with your IBM Cloud API key
SERVICE_URL = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/abc'  # Replace with your service URL
AUDIO_FILE_PATH = join(dirname(__file__), '../combined_audio.wav')
OUTPUT_FILE = 'transcriptions.json'

# Initialize the Speech to Text service
def initialize_service(api_key, service_url):
    authenticator = IAMAuthenticator(api_key)
    service = SpeechToTextV1(authenticator=authenticator)
    service.set_service_url(service_url)
    return service

# List available models
def list_models(service):
    models = service.list_models().get_result()
    print(json.dumps(models, indent=2))

# Get details of a specific model
def get_model_details(service, model_id):
    model = service.get_model(model_id).get_result()
    print(json.dumps(model, indent=2))

# Transcribe audio and save to JSON file
def transcribe_audio_to_file(service, audio_file_path, output_file, content_type="audio/wav"):
    with open(audio_file_path, 'rb') as audio_file:
        response = service.recognize(
            audio=audio_file,
            content_type=content_type
        ).get_result()
        with open(output_file, 'w') as f:
            json.dump(response, f, indent=4)
    print(f"Transcriptions saved to {output_file}")

# WebSocket callback class for advanced recognition
def transcribe_with_websocket(service, audio_file_path, content_type="audio/l16; rate=44100"):
    class MyRecognizeCallback(RecognizeCallback):
        def __init__(self):
            super().__init__()

        def on_connected(self):
            print('Connection was successful')

        def on_transcription(self, transcript):
            print(f'Transcription: {transcript}')

        def on_error(self, error):
            print(f'Error received: {error}')

        def on_inactivity_timeout(self, error):
            print(f'Inactivity timeout: {error}')

        def on_listening(self):
            print('Service is listening')

        def on_hypothesis(self, hypothesis):
            print(f'Hypothesis: {hypothesis}')

        def on_data(self, data):
            print(f'Data received: {json.dumps(data, indent=2)}')

    callback = MyRecognizeCallback()
    with open(audio_file_path, 'rb') as audio_file:
        audio_source = AudioSource(audio_file)
        recognize_thread = threading.Thread(
            target=service.recognize_using_websocket,
            args=(audio_source, content_type, callback)
        )
        recognize_thread.start()

# Main program
if __name__ == "__main__":
    speech_to_text_service = initialize_service(API_KEY, SERVICE_URL)

    # List available models
    print("Available models:")
    list_models(speech_to_text_service)

    # Get details of a specific model
    print("Model details:")
    get_model_details(speech_to_text_service, 'en-US_BroadbandModel')

    # Transcribe audio and save to file
    transcribe_audio_to_file(speech_to_text_service, AUDIO_FILE_PATH, OUTPUT_FILE)

    # Transcribe audio using WebSocket
    websocket_audio_file = join(dirname(__file__), '../resources/speech.wav')
    transcribe_with_websocket(speech_to_text_service, websocket_audio_file)
