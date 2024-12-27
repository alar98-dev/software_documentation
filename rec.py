import speech_recognition as sr
#import keyboard
import gpy
import pygame
import time
import os

def extrair_audio(audio):
    pass


def get_next_filename(directory,prefix):
    existing_files = [f[6:] for f in os.listdir(directory) if f.startswith(prefix)]
    return f"voice {len(existing_files)+1}"

get_next_filename(directory='./my_voice_folder/',prefix='voice')

r = sr.Recognizer()
openai = gpy.gpt()

def abrir_microfone():

    while True:
        with sr.Microphone() as source:
            print("Say something:")

            r.adjust_for_ambient_noise(source=source)
            
            audio = r.listen(source=source)
            
            with open(f'./my_voice_folder/{get_next_filename(directory='./my_voice_folder/',prefix='voice')}','wb') as arq:
                    arq.write(audio.get_wav_data())

            try:

                text = r.recognize_google(audio_data=audio, language="pt-BR")
                print(f"You said: {text}")
                res = openai.send_chat(prompt=text)

                print(res)

                #tocar audio
                #if openai.type == 1:
                #    pygame.mixer.init()
                #    pygame.mixer.music.load('speech.mp3')
                #    pygame.mixer.music.play()

                #    while pygame.mixer.music.get_busy():
                #        time.sleep(0.2)
                    
                #    pygame.mixer.quit() 

                
            except sr.UnknownValueError:
                print('Audio não compreendido')
            except sr.RequestError:
                print("Request error")

               


abrir_microfone()
