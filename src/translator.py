from googletrans import Translator, constants
from pprint import pprint

# init the Google API translator

def translate(text):
    translator = Translator()

    detection = translator.detect(text)
    # print("Language code:", detection.lang)
    # print("Confidence:", detection.confidence)
    # print the detected language
    detectedlanguage = constants.LANGUAGES[detection.lang]
    # print("Language:", detectedlanguage)

    if detectedlanguage != 'english':
    # translate text to english text (by default)
       translation = translator.translate(text)
    #    print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
       translatedtext = f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})"
       return translatedtext
    
    else:
        return text





