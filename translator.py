from googletrans import Translator

# Опции, чтобы убрать лишние слова из запроса
ALIASES = ("айрис", "арис", "рис", "аис", "iris", "airis", "ириска", "алиса")
TRIGGERS = (
    "скажи", "расскажи", "покажи", "сколько", "произнеси", "как", "поставь",
    "переведи", "засеки", "запусти", "переводчик", "translate", "какое сейчас время"
)

def clean_request(text):
    for x in ALIASES:
        text = text.replace(x, "")
    for x in TRIGGERS:
        text = text.replace(x, "")
    return text.strip()

def translate(request):
    translator = Translator()
    
    # Очищаем текст запроса
    clean_text = clean_request(request)
    
    try:
        translated = translator.translate(clean_text, src='en', dest='ru')
        return translated.text
    except Exception as e:
        return f"Ошибка перевода: {e}"
