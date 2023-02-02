
from google_trans_new import google_translator

from deep_translator import GoogleTranslator
translated = GoogleTranslator(source='auto', target='de').translate("keep it up, you are awesome")  # output -> Weiter so, du bist großartig

print(translated)