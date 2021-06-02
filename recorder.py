import pyaudio
import wave
import requests
from array import array
import config as cf

import serial
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
BUFFER = 1024
SILENCE_THREASHOLD = 8000
RECORD_SECONDS = 1

OUTPUT_FILE_NAME = cf.OUTPUT_PATH

# ser = serial.Serial('COM4',9600)
# time.sleep(2)


def detect_sound():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("소리 감지 시작")
    while True:
        # print("소리 감지 중")
        volume_sum = 0;
        frames = []

        try:
            for _ in range(0, int(RATE / CHUNK)):
                if not stream.is_active():
                    stream = audio.open(format=FORMAT,
                                        channels=CHANNELS,
                                        rate=RATE,
                                        input=True,
                                        frames_per_buffer=CHUNK)

                data = stream.read(CHUNK, exception_on_overflow=False)
                volume = max(array('h', data))
                volume_sum += volume

                if volume >= SILENCE_THREASHOLD:
                    print('특정 볼륨 이상의 소리가 감지되었습니다.')
                    print("볼륨 = " + str(volume_sum))
                    frames.append(data)

                    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                        data = stream.read(CHUNK)
                        frames.append(data)
                    print("녹음 완료. 저장 시작")
                    save_audio(frames, audio)
                    post_audio()
        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            pass


def save_audio(frames, audio):
    wav_file = wave.open(OUTPUT_FILE_NAME, "wb")
    wav_file.setnchannels(CHANNELS)
    wav_file.setsampwidth(audio.get_sample_size(FORMAT))
    wav_file.setframerate(RATE)
    wav_file.writeframes(b''.join(frames))
    wav_file.close()
    print("저장 끝")


def post_audio():
    wav_file = open(OUTPUT_FILE_NAME, "rb")
    headers = {'Content-Type': 'audio/wave'}
    file = {'file': wav_file}
    uri = cf.URI
    response = requests.post(uri, files=file)

    response_data = response.json()
    print("결과 => " + str(response_data))
    flash(response_data)


def flash(response_data):
    id = response_data['id']
    name = response_data['sound_name']

    print(id)
    print(name)

    if id == 1:
        print(str(name) + "소리가 감지되었습니다.")
        # ser.write(b'A')
    elif id == 2:
        print(str(name) + "소리가 감지되었습니다.")
        # ser.write(b'B')
    elif id == 3:
        print(str(name) + "소리가 감지되었습니다.")
        # ser.write(b'C')
    elif id == 4:
        print(str(name) + "소리가 감지되었습니다.")
        # ser.write(b'A')
    elif id == 5:
        print(str(name) + "소리가 감지되었습니다.")
        # ser.write(b'A')
    elif id == 6:
        print(str(name) + "소리가 감지되었습니다.")
        # ser.write(b'C')
    elif id == 7:
        print(str(name) + "소리가 감지되었습니다.")
        # ser.write(b'C')
    elif id == 8:
        print(str(name) + "소리가 감지되었습니다.")
        # ser.write(b'D')
    elif id == 9:
        print(str(name) + "소리가 감지되었습니다.")
        # ser.write(b'D')
    elif id == 10:
        print(str(name) + "소리가 감지되었습니다.")
        # ser.write(b'D')



if __name__ == '__main__':
    detect_sound()