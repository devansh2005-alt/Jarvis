import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests

# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "3ce924136e5945c7894b264daf34e692"

# Speak function
def speak(text):
    import pyttsx3
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)

    print("Speaking:", text)
    engine.say(text)
    engine.runAndWait() 

def tell_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        res = requests.get(url)
        data = res.json()
        joke = f"{data['setup']} ... {data['punchline']}"
        speak(joke)
    except:
        speak("Sorry, I couldn't fetch a joke right now.")


# Function to process recognized command
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://Google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://Youtube.com")
    elif "open linkedIn" in c.lower():
        webbrowser.open("https://Linkdin.com")
    elif "open facebook" in c.lower():
        webbrowser.open("http://Facebook.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "joke" in c.lower():
        tell_joke()
    elif "news" in c.lower():
     r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
    if r.status_code == 200:
        data = r.json()
        articles = data.get('articles', [])
        
        if not articles:
            speak("Sorry, I couldn't fetch any news at the moment.")
        else:
            for article in articles[:5]:  # Just read top 5 headlines
                speak(article['title'])
    else:
        speak("Sorry, I couldn't reach the news service.")

        

     
# Main program
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            print("Listening for wake word...")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)
                print("You said:", word)

                if word.lower() == "jarvis":
                    speak("Yes I am listening")
                    
                    
                    # Listen for next command
                    print("Jarvis Active. Listening for command...")
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        try:
                            command = recognizer.recognize_google(audio)
                            print("Recognized command:", command)
                            processCommand(command)
                        except sr.UnknownValueError:
                            speak("Sorry, I didn't catch that.")
                        except sr.RequestError as e:
                            speak("Could not connect to Google: " + str(e))

        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except Exception as e:
            print("Unexpected error:",str(e))
