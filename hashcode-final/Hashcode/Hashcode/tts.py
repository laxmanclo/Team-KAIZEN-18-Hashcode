import speech_recognition as sr

def speech_to_text():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    # Recognize speech using Google Speech Recognition
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))
        return ""

if __name__ == "__main__":
    output_file = open("recognized_text.txt", "a")  # Open a file in append mode
    while True:
        speech = speech_to_text()
        if speech.lower() == "exit":
            print("Exiting...")
            output_file.close()
            break
        elif speech:
            print("You said:", speech)
            output_file.write(speech + "\n")  # Write recognized text to the file
