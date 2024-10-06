from langdetect import detect
from googletrans import Translator, LANGUAGES

def detect_and_translate(text):
    # Detect the language of the input text
    detected_lang = detect(text)
    print(f"Detected language: {LANGUAGES.get(detected_lang, 'unknown')} ({detected_lang})")

    # Check if the detected language is English
    if detected_lang == 'en':
        #print("Text is already in English.")
        return text

    # Translate the text to English
    translator = Translator()
    translation = translator.translate(text, dest='en')
    #print("Translation:", translation.text)
    return translation.text

