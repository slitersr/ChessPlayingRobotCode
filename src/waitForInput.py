#https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
import speech_recognition as sr
from ctypes import *
from contextlib import contextmanager
import pyaudio

ERROR_HANDLER_FUNC = CFUNCTYPE(None)

def py_error_handler():
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

#read in text from microphone in this file and write to inputPlayer.txt
def microphoneReady():

    #initializes instance of library used to read in audio from mic
    r = sr.Recognizer()
    
    with noalsaerr():
        microphone = sr.Microphone() 
        
    #for as long as the user is speaking/the microphone volume is picked up beyond threshold, audio is turned into text with r.listen
    with microphone as source:
        # read the audio data from the default microphone
        audio = r.listen(source)
        print("Recognizing...")
        # verify input is valid
        try:
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # if input is valid, turn audio into text variable
        text = r.recognize_google(audio)
        print(text)
    return text