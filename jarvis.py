import speech_recognition as sr
import openai
import webbrowser
import datetime
import os
import re
import spacy
import pyttsx3

class Jarvis:
    def __init__(self):
        file = open(r"creditentials", "r")
        openai.api_key = file.readline().strip()
        file.close()
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')  # gets you the details of the current voice

        self.engine.setProperty('voice', voices[0].id)  # 0-male voice , 1-female voice

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def takeCommand(self):
        query = self.__listen()

        options = [
            "google",
            "youtube",
            "now",
            "stack overflow",
            "durhack",
            "vs code",
            "image",
            "gpt",
            "who or what"
        ]
        mostRelevant = self.pick_relevant(options, query)

        if mostRelevant == "google":
            if re.findall("google\s+(.*)", query):
                if self.__confirm_option("open google and search for "+re.findall("google\s+(.*)", query)[0]):
                    webbrowser.open("www.google.com/search?q=" + re.findall("google\s+(.*)", query)[0])
            else:
                if self.__confirm_option("open google"):
                    webbrowser.open("www.google.com")
        elif mostRelevant == "youtube":
            if self.__confirm_option("open youtube"):
                webbrowser.open("youtube.com")
        elif mostRelevant == "time":
            if self.__confirm_option("tell current time"):
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                self.speak(f"Current time is {strTime}")
        elif mostRelevant == "stack overflow":
            if self.__confirm_option("open stack overflow"):
                webbrowser.open('stackoverflow.com')
        elif mostRelevant == "durhack":
            if self.__confirm_option("open durhack website"):
                webbrowser.open('durhack.com')
        elif mostRelevant == "vs code":
            if self.__confirm_option("open vs code"):
                os.startfile("code")
        elif mostRelevant == "image":
            if self.__confirm_option("generate an image"):
                url1 = self.generate(query)
                webbrowser.open(url1)
        elif mostRelevant == "who or what" or mostRelevant == "gpt":
            if self.__confirm_option("ask chat gpt"):
                try:
                    self.speak(self.__chat_with_chatgpt(query))
                except Exception as e:
                    print(e)
        elif mostRelevant == "stop":
            if self.__confirm_option("stop working"):
                try:
                    self.speak("It was a pleasure to be your assistant. I'll be back.")
                except Exception as e:
                    print(e)

    def __chat_with_chatgpt(self, msg, model="gpt-3.5-turbo"):
        msg = "Answer this question in one sentence no more than 20 words: " + msg
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": msg}],
            max_tokens=500,
            temperature=1.0
        )

        message = response.choices[0].message.content
        print(message)
        return message

    def __listen(self):
        r = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                r.pause_threshold = 0.5
                #r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, phrase_time_limit=None, timeout=None)
            try:
                query = r.recognize_google(audio, language='en-in')
                query = query.lower()
                print(f"{query}\n")
                return query
            except Exception as e:
                self.speak("Say that again please...")

    def __confirm_option(self, option):
        self.speak("Do you want me to "+option+"?")
        while True:
            answer = self.__listen().lower()
            if "yes" in answer:
                self.speak("Option confirmed")
                return True
            elif "no" in answer:
                self.speak("Option canceled")
                return False
            else:
                self.speak("Please repeat, do you want me to "+option+"?")

    def pick_relevant(self,options, question):
        # Load spaCy's English NLP model
        nlp = spacy.load("en_core_web_md")

        # Process the question
        question_doc = nlp(question)

        # Check for exact keyword matches
        for option in options:
            if option.lower() in question.lower():
                return option

        # If no exact keyword matches, resort to similarity scores
        option_scores = []
        for option in options:
            option_doc = nlp(option)
            similarity_score = question_doc.similarity(option_doc)
            option_scores.append((option, similarity_score))

        # Sort options based on similarity scores
        sorted_options = sorted(option_scores, key=lambda x: x[1], reverse=True)

        # Return the most suitable option
        return sorted_options[0][0]

    # function for text-to-image generation
    # using create endpoint of DALL-E API
    # function takes in a string argument
    def generate(self, text):
        res = openai.Image.create(
            # text describing the generated image
            prompt=text,
            # number of images to generate
            n=1,
            # size of each generated image
            size="256x256",
        )
        # returning the URL of one image as
        # we are generating only one image
        return res["data"][0]["url"]

if __name__ == "__main__":
    assistant = Jarvis()
    assistant.speak('Hello, I am Jarvis. Please tell me how may I help you.')

    while True:
        assistant.takeCommand()








