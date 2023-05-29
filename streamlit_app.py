import websocket
import threading
import time
import json
import pyaudio

# OpenAI API details
API_TOKEN = ["KEY", "Python"]
ASR_MODEL_ID = 'whisper-english-6'

# Audio settings
AUDIO_CHUNK_SIZE = 2048
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHANNELS = 1
AUDIO_RATE = 16000

# WebSocket connection
ws = None

# Callback for handling audio stream
def audio_callback(in_data, frame_count, time_info, status):
    ws.send_binary(in_data)
    return (None, pyaudio.paContinue)

# WebSocket connection established
def on_open(ws):
    print('Connected to the server.')

    # Start audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=AUDIO_FORMAT,
                    channels=AUDIO_CHANNELS,
                    rate=AUDIO_RATE,
                    input=True,
                    frames_per_buffer=AUDIO_CHUNK_SIZE,
                    stream_callback=audio_callback)

    stream.start_stream()

    # Keep the connection alive
    while True:
        time.sleep(1)

# WebSocket message received
def on_message(ws, message):
    response = json.loads(message)

    if 'text' in response['partial']:
        print('Partial:', response['partial']['text'])

    if 'text' in response['final']:
        print('Final:', response['final']['text'])

# WebSocket connection closed
def on_close(ws):
    print('Connection closed.')

# Start the WebSocket connection
def start_ws_connection():
    global ws

    # Initialize WebSocket connection
    ws = websocket.WebSocketApp('wss://api.openai.com/v1/asr/stream',
                                header={'Authorization': f'Bearer {API_TOKEN}'},
                                on_open=on_open,
                                on_message=on_message,
                                on_close=on_close)

    ws.run_forever()

# Start the speech-to-text process
def start_speech_to_text():
    threading.Thread(target=start_ws_connection).start()

# Main function
def main():
    print('Speech-to-Text using Whisper ASR')

    # Start the speech-to-text process
    start_speech_to_text()

    # Wait for the process to complete
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
