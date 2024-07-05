import speech_recognition as sr

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Please speak clearly into the microphone.")
        audio = recognizer.listen(source)

    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print(f"Recognized text: {text}")
        return text
    except sr.RequestError:
        print("API was unreachable or unresponsive.")
        return None
    except sr.UnknownValueError:
        print("Speech was unintelligible.")
        return None

def write_text_to_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)

if __name__ == "__main__":
    recognized_text = recognize_speech_from_mic()
    if recognized_text:
        output_filename = "output.txt"
        write_text_to_file(recognized_text, output_filename)
        print(f"Recognized speech has been written to {output_filename}.")
    else:
        print("No speech was recognized.")
