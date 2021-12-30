#https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
import speech_recognition as sr


#read in text from microphone in this file and write to inputPlayer.txt
def microphoneReady():

    #initializes instance of library used to read in audio from mic
    r = sr.Recognizer()
    
    #for as long as the user is speaking/the microphone volume is picked up beyond threshold, audio is turned into text with r.listen
    with sr.Microphone() as source:
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
        
        #write text to playerInput.txt
        with open('C:/Users/seans/Desktop/SeniorDesignI/ProjectCode/' + 'playerInput.txt', 'w') as f:
            f.write(text)
            f.close

        


