import speech_recognition as sr
import pyttsx3
import requests
import datetime
import wikipedia
import openai
import os
import random

# Initialize OpenAI API
openai.api_key = "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"

# Initialize text-to-speech engine
def speak(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

# AI Chatbot functionality
def ai_chatbot(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return "Sorry, I couldn't process that request."

# Tell a random joke
def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the computer go to the doctor? Because it caught a virus!",
        "Why was the math book sad? It had too many problems."
    ]
    return random.choice(jokes)

# Set a reminder
def set_reminder(task, time):
    speak(f"Reminder set for {task} at {time}.")
    # Logic to store the reminder can be added

# Play music
def play_music():
    speak("Playing your favorite song.")
    os.system("start wmplayer")  # Adjust for your OS

# Smart home integration placeholder
def control_smart_device(device, action):
    speak(f"Attempting to {action} the {device}.")
    # Example: Add integration logic with smart home devices via APIs

# Play a quiz game
def play_quiz():
    questions = {
        "What is the capital of France?": "paris",
        "What is 5 + 7?": "12",
        "Who wrote Hamlet?": "shakespeare",
    }
    question, answer = random.choice(list(questions.items()))
    speak(question)
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            user_answer = recognizer.recognize_google(audio, language="en-US").lower()
            if user_answer == answer:
                speak("Correct answer!")
            else:
                speak(f"Wrong answer! The correct answer is {answer}.")
        except Exception as e:
            speak("I couldn't hear your answer. Let's try again later.")

# Interactive assistant main loop
speak("Hello! Sir, Alfred is here to assist you. What should we do today?")

while True:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Please say something:")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language="en-US")
            print("You said: " + text)
        except Exception as e:
            speak("Sorry, I couldn't understand. Can you please repeat?")
            continue

        text = text.lower()

        # Greeting
        if "good morning" in text or "hello" in text:
            speak("Greetings, Sir! How can I help you today?")

        # Weather Information
        elif "weather" in text:
            speak("Please tell me the city name.")
            try:
                with sr.Microphone() as source:
                    city_audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    city = recognizer.recognize_google(city_audio, language="en-US")
                api_key = "3fefe0e8b49a4267c906b1573d5fce18"
                base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(base_url)
                if response.status_code == 200:
                    data = response.json()
                    current_temperature = data["main"]["temp"]
                    current_weather = data["weather"][0]["description"]
                    speak(f"The weather in {city} is {current_weather} with a temperature of {current_temperature} degrees Celsius.")
                else:
                    speak("Sorry, I couldn't fetch the weather information.")
            except Exception as e:
                speak("Sorry, I couldn't understand the city name.")

        # News Headlines
        elif "news" in text:
            api_key_news = "047d667835fb4f1baac6b88cfb783187"
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key_news}"
            response = requests.get(url)
            if response.status_code == 200:
                articles = response.json().get("articles", [])[:3]
                headlines = [article['title'] for article in articles]
                speak("Here are the top 3 headlines:")
                for i, headline in enumerate(headlines, 1):
                    speak(f"{i}. {headline}")
            else:
                speak("Sorry, I couldn't fetch the news.")

        # Time
        elif "time" in text:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {time}.")

        # Wikipedia Search
        elif "search" in text:
            query = text.replace("search", "").strip()
            if query:
                speak(f"Searching Wikipedia for {query}.")
                try:
                    summary = wikipedia.summary(query, sentences=2)
                    speak(summary)
                except Exception as e:
                    speak("Sorry, I couldn't find any information.")
            else:
                speak("What would you like me to search for?")

        # Open Application
        elif "open" in text:
            app_name = text.replace("open", "").strip()
            if "notepad" in app_name:
                os.system("notepad")
                speak("Opening Notepad.")
            elif "calculator" in app_name:
                os.system("calc")
                speak("Opening Calculator.")
            else:
                speak("Sorry, I cannot open that application.")

        # AI Chatbot
        elif "chat" in text or "ask" in text:
            speak("What would you like to ask?")
            try:
                with sr.Microphone() as source:
                    chat_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    chat_query = recognizer.recognize_google(chat_audio, language="en-US")
                    ai_response = ai_chatbot(chat_query)
                    speak(ai_response)
            except Exception as e:
                speak("Sorry, I couldn't understand your query.")

        # Tell a Joke
        elif "joke" in text:
            joke = tell_joke()
            speak(joke)

        # Set Reminder
        elif "remind me" in text:
            speak("What would you like me to remind you about?")
            try:
                with sr.Microphone() as source:
                    task_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    task = recognizer.recognize_google(task_audio, language="en-US")
                speak("When should I remind you?")
                with sr.Microphone() as source:
                    time_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    reminder_time = recognizer.recognize_google(time_audio, language="en-US")
                set_reminder(task, reminder_time)
            except Exception as e:
                speak("Sorry, I couldn't understand the reminder details.")

        # Smart Home Control
        elif "control" in text:
            speak("Which device would you like to control?")
            try:
                with sr.Microphone() as source:
                    device_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    device = recognizer.recognize_google(device_audio, language="en-US")
                speak(f"What action should I perform on the {device}?")
                with sr.Microphone() as source:
                    action_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    action = recognizer.recognize_google(action_audio, language="en-US")
                control_smart_device(device, action)
            except Exception as e:
                speak("Sorry, I couldn't control the device.")

        # Play Quiz
        elif "quiz" in text:
            play_quiz()

        # Exit
        elif "exit" in text or "bye" in text:
            speak("Goodbye, Sir! Have a nice day!")
            break

        # Fallback
        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")
