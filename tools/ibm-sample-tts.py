import json
from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Constants (replace these with your own values)
API_KEY = 'APIKEY'  # Replace with your IBM Cloud API key
SERVICE_URL = 'https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/abc'  # Replace with your service URL
OUTPUT_FILE = join(dirname(__file__), 'output.wav')

# Initialize the Text to Speech service
def initialize_service(api_key, service_url):
    authenticator = IAMAuthenticator(api_key)
    service = TextToSpeechV1(authenticator=authenticator)
    service.set_service_url(service_url)
    return service

# List available voices
def list_voices(service):
    voices = service.list_voices().get_result()
    print(json.dumps(voices, indent=2))

# Synthesize text to audio and save to file
def synthesize_to_file(service, text, output_file, voice="en-US_AllisonVoice", audio_format="audio/wav"):
    with open(output_file, 'wb') as audio_file:
        response = service.synthesize(
            text,
            accept=audio_format,
            voice=voice
        ).get_result()
        audio_file.write(response.content)
    print(f"Audio saved to {output_file}")

# WebSocket callback class for advanced synthesis
def synthesize_with_websocket(service, text, output_file, voice="en-US_AllisonVoice", audio_format="audio/wav"):
    class MySynthesizeCallback(SynthesizeCallback):
        def __init__(self):
            super().__init__()
            self.fd = open(output_file, 'ab')

        def on_connected(self):
            print('Connection was successful')

        def on_error(self, error):
            print(f'Error received: {error}')

        def on_content_type(self, content_type):
            print(f'Content type: {content_type}')

        def on_audio_stream(self, audio_stream):
            self.fd.write(audio_stream)

        def on_close(self):
            self.fd.close()
            print('Done synthesizing. Closing the connection')

    callback = MySynthesizeCallback()
    service.synthesize_using_websocket(
        text,
        callback,
        accept=audio_format,
        voice=voice
    )

# Main program
if __name__ == "__main__":
    text_to_speech_service = initialize_service(API_KEY, SERVICE_URL)

    # List voices
    print("Available voices:")
    list_voices(text_to_speech_service)

    # Synthesize and save to file
    text_to_synthesize = "Hello, world!"
    synthesize_to_file(text_to_speech_service, text_to_synthesize, OUTPUT_FILE)

    # Synthesize using WebSocket
    text_to_synthesize_ws = "I like to pet dogs."
    websocket_output_file = join(dirname(__file__), 'output_ws.wav')
    synthesize_with_websocket(text_to_speech_service, text_to_synthesize_ws, websocket_output_file)