from googletrans import Translator
import functions

def translate(text=''):
    translator = Translator()
    # text = functions.voice
    
    translated = translator.translate(text, src='en', dest='ru')

    result = translated.text
    
    try:
        functions.speak(result)
    except:
        functions.speak("Обратитесь к переводчику, начиная со слова 'Переводчик'")