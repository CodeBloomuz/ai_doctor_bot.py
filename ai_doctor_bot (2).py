"""
╔══════════════════════════════════════════════════════════════╗
║          AI DOCTOR ASSISTANT — TELEGRAM BOT                 ║
║          O'zbekcha + Ruscha | Barcha funksiyalar            ║
╚══════════════════════════════════════════════════════════════╝

ISHGA TUSHIRISH:
1. pip install pytelegrambotapi anthropic requests
2. BOT_TOKEN va ANTHROPIC_API_KEY ni o'rnating
3. python ai_doctor_bot.py

"""

import telebot
from telebot import types
import anthropic
import requests
import os

# ═══════════════════════════════════════════════
#  SOZLAMALAR — Railway Variables dan avtomatik olinadi
# ═══════════════════════════════════════════════
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Foydalanuvchi tillari va holatlari saqlanadi
user_data = {}

# ═══════════════════════════════════════════════
#  TIL TANLASH MATNLARI
# ═══════════════════════════════════════════════
TEXTS = {
    "uz": {
        "welcome": """🏥 *AI Doctor Assistant ga xush kelibsiz!*

Men sun'iy intellektga asoslangan tibbiy yordamchiman.

⚠️ *Eslatma:* Men shifokor emasman. Bergan maslahatlarim faqat yo'naltiruvchi xarakterda. Jiddiy holatlarda albatta shifokorga murojaat qiling!

Quyidagi bo'limlardan birini tanlang 👇""",
        "menu": "📋 Asosiy menyu",
        "symptom": "🤒 Simptom tahlili",
        "doctor": "👨‍⚕️ Shifokor tavsiyasi",
        "clinic": "🏥 Klinika topish",
        "medicine": "💊 Dori ma'lumoti",
        "language": "🌐 Til o'zgartirish",
        "symptom_prompt": "Alomatlatingizni yozing (masalan: bosh og'riq, isitma, yo'tal):",
        "doctor_prompt": "Qaysi soha bo'yicha shifokor kerak? Yoki simptomlaringizni yozing:",
        "clinic_prompt": "Qaysi shaharda klinika qidirasiz?",
        "medicine_prompt": "Qaysi dori haqida ma'lumot kerak?",
        "thinking": "⏳ Tahlil qilinmoqda...",
        "back": "⬅️ Orqaga",
        "disclaimer": "\n\n⚠️ _Bu ma'lumot faqat yo'naltiruvchi. Shifokor ko'rigisiz dori ichmasligingizni tavsiya qilamiz._",
    },
    "ru": {
        "welcome": """🏥 *Добро пожаловать в AI Doctor Assistant!*

Я медицинский помощник на основе искусственного интеллекта.

⚠️ *Внимание:* Я не врач. Мои советы носят ориентировочный характер. При серьёзных состояниях обязательно обратитесь к врачу!

Выберите раздел 👇""",
        "menu": "📋 Главное меню",
        "symptom": "🤒 Анализ симптомов",
        "doctor": "👨‍⚕️ Рекомендация врача",
        "clinic": "🏥 Найти клинику",
        "medicine": "💊 Информация о лекарстве",
        "language": "🌐 Сменить язык",
        "symptom_prompt": "Опишите ваши симптомы (например: головная боль, температура, кашель):",
        "doctor_prompt": "К какому специалисту нужно обратиться? Или опишите симптомы:",
        "clinic_prompt": "В каком городе искать клинику?",
        "medicine_prompt": "О каком лекарстве нужна информация?",
        "thinking": "⏳ Анализируется...",
        "back": "⬅️ Назад",
        "disclaimer": "\n\n⚠️ _Эта информация носит ориентировочный характер. Не принимайте лекарства без консультации врача._",
    }
}

# ═══════════════════════════════════════════════
#  AI BILAN MULOQOT — ASOSIY FUNKSIYA
# ═══════════════════════════════════════════════
def ask_ai(prompt: str, lang: str) -> str:
    """Claude AI ga savol yuboradi va javob oladi"""
    
    system_uz = """Sen O'zbekistonlik foydalanuvchilar uchun AI tibbiy yordamchisan.
    
Qoidalar:
- Faqat O'zbek tilida javob ber
- Har doim "Men shifokor emasman, bu faqat yo'naltiruvchi maslahat" deb ogohlantir
- Simptomlarni tahlil qil va ehtimoliy kasalliklarni sanab ber
- Qaysi shifokorga borish kerakligini ayt
- Uy sharoitida nima qilish mumkinligini tushuntir
- Jiddiy hollarda darhol shifokorga borishni tavsiya qil
- Javoblarni qisqa, aniq va tushunarli qil
- Emoji ishlat (🤒 💊 👨‍⚕️ ⚠️ ✅)"""

    system_ru = """Ты медицинский AI-ассистент для пользователей Узбекистана.
    
Правила:
- Отвечай только на русском языке
- Всегда предупреждай: "Я не врач, это лишь ориентировочный совет"
- Анализируй симптомы и перечисляй возможные заболевания
- Указывай, к какому специалисту обратиться
- Объясняй, что можно сделать в домашних условиях
- При серьёзных симптомах срочно рекомендуй врача
- Давай короткие, чёткие и понятные ответы
- Используй эмодзи (🤒 💊 👨‍⚕️ ⚠️ ✅)"""

    system = system_uz if lang == "uz" else system_ru

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=system,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        if lang == "uz":
            return "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
        else:
            return "❌ Произошла ошибка. Пожалуйста, попробуйте снова."

# ═══════════════════════════════════════════════
#  KLINIKA QIDIRISH
# ═══════════════════════════════════════════════
def search_clinics(city: str, lang: str) -> str:
    """Shahar bo'yicha klinikalarni Google Maps orqali topadi"""
    
    # Google Maps Search URL
    query = f"klinikalar {city}" if lang == "uz" else f"клиники {city}"
    maps_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
    
    if lang == "uz":
        return f"""🏥 *{city} shahridagi klinikalar:*

📍 Google Maps da ko'rish:
{maps_url}

Yaqin klinikalarni topish uchun:
1. Yuqoridagi havolani bosing
2. Yoki Google Mapsda "{query}" deb qidiring

📞 *Toshkentdagi mashhur klinikalar:*
• Shoshilinch tibbiy yordam: *103*
• Tez yordam: *103*
• Respublika shifoxonasi: +998 71 237-20-02"""
    else:
        return f"""🏥 *Клиники в городе {city}:*

📍 Посмотреть на Google Maps:
{maps_url}

Для поиска ближайших клиник:
1. Нажмите на ссылку выше
2. Или введите "{query}" в Google Maps

📞 *Известные клиники Ташкента:*
• Скорая помощь: *103*
• Республиканская больница: +998 71 237-20-02"""

# ═══════════════════════════════════════════════
#  KLAVIATURALAR (TUGMALAR)
# ═══════════════════════════════════════════════
def main_menu_keyboard(lang: str):
    """Asosiy menyu tugmalari"""
    t = TEXTS[lang]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton(t["symptom"]),
        types.KeyboardButton(t["doctor"]),
        types.KeyboardButton(t["clinic"]),
        types.KeyboardButton(t["medicine"]),
        types.KeyboardButton(t["language"])
    )
    return kb

def back_keyboard(lang: str):
    """Orqaga tugmasi"""
    t = TEXTS[lang]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(t["back"]))
    return kb

def language_keyboard():
    """Til tanlash tugmalari"""
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton("🇺🇿 O'zbekcha"),
        types.KeyboardButton("🇷🇺 Русский")
    )
    return kb

# ═══════════════════════════════════════════════
#  HOLATLAR (USER STATE)
# ═══════════════════════════════════════════════
def get_user(user_id: int) -> dict:
    if user_id not in user_data:
        user_data[user_id] = {"lang": "uz", "state": "menu"}
    return user_data[user_id]

def set_state(user_id: int, state: str):
    get_user(user_id)["state"] = state

def get_lang(user_id: int) -> str:
    return get_user(user_id)["lang"]

# ═══════════════════════════════════════════════
#  BOT HANDLERLARI
# ═══════════════════════════════════════════════

@bot.message_handler(commands=["start"])
def start(message):
    """Botni boshlash"""
    user_id = message.from_user.id
    lang = get_lang(user_id)
    set_state(user_id, "menu")
    
    bot.send_message(
        message.chat.id,
        TEXTS[lang]["welcome"],
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(lang)
    )

@bot.message_handler(commands=["menu"])
def show_menu(message):
    start(message)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    """Barcha xabarlarni qayta ishlash"""
    user_id = message.from_user.id
    user = get_user(user_id)
    lang = user["lang"]
    state = user["state"]
    text = message.text
    t = TEXTS[lang]

    # ── TIL O'ZGARTIRISH ──
    if text in ["🌐 Til o'zgartirish", "🌐 Сменить язык"]:
        set_state(user_id, "menu")
        bot.send_message(message.chat.id, "🌐 Tilni tanlang / Выберите язык:", 
                        reply_markup=language_keyboard())
        return

    if text == "🇺🇿 O'zbekcha":
        user_data[user_id]["lang"] = "uz"
        lang = "uz"
        set_state(user_id, "menu")
        bot.send_message(message.chat.id, "✅ Til o'zgartirildi!", 
                        reply_markup=main_menu_keyboard("uz"))
        return

    if text == "🇷🇺 Русский":
        user_data[user_id]["lang"] = "ru"
        lang = "ru"
        set_state(user_id, "menu")
        bot.send_message(message.chat.id, "✅ Язык изменён!", 
                        reply_markup=main_menu_keyboard("ru"))
        return

    # ── ORQAGA ──
    if text == t["back"]:
        set_state(user_id, "menu")
        bot.send_message(message.chat.id, t["menu"], 
                        reply_markup=main_menu_keyboard(lang))
        return

    # ── MENYU TUGMALARI ──
    if text == t["symptom"]:
        set_state(user_id, "symptom")
        bot.send_message(message.chat.id, t["symptom_prompt"], 
                        reply_markup=back_keyboard(lang))
        return

    if text == t["doctor"]:
        set_state(user_id, "doctor")
        bot.send_message(message.chat.id, t["doctor_prompt"], 
                        reply_markup=back_keyboard(lang))
        return

    if text == t["clinic"]:
        set_state(user_id, "clinic")
        bot.send_message(message.chat.id, t["clinic_prompt"], 
                        reply_markup=back_keyboard(lang))
        return

    if text == t["medicine"]:
        set_state(user_id, "medicine")
        bot.send_message(message.chat.id, t["medicine_prompt"], 
                        reply_markup=back_keyboard(lang))
        return

    # ── AI JAVOBLARI ──
    if state == "symptom":
        thinking_msg = bot.send_message(message.chat.id, t["thinking"])
        
        if lang == "uz":
            prompt = f"Bemorning alomatlari: {text}\n\nQuyidagilarni tahlil qil:\n1. Ehtimoliy kasalliklar\n2. Qaysi shifokorga borish kerak\n3. Uyda nima qilish mumkin\n4. Qachon zudlik bilan shifokorga borish kerak"
        else:
            prompt = f"Симптомы пациента: {text}\n\nПроанализируй:\n1. Возможные заболевания\n2. К какому врачу обратиться\n3. Что можно сделать дома\n4. Когда срочно нужен врач"
        
        response = ask_ai(prompt, lang)
        bot.delete_message(message.chat.id, thinking_msg.message_id)
        bot.send_message(message.chat.id, response + t["disclaimer"], 
                        parse_mode="Markdown", reply_markup=back_keyboard(lang))

    elif state == "doctor":
        thinking_msg = bot.send_message(message.chat.id, t["thinking"])
        
        if lang == "uz":
            prompt = f"Savol: {text}\n\nQaysi shifokor mutaxassisiga murojaat qilish kerakligini aniq ayt. Sababini tushuntir."
        else:
            prompt = f"Вопрос: {text}\n\nУкажи конкретного специалиста. Объясни причину."
        
        response = ask_ai(prompt, lang)
        bot.delete_message(message.chat.id, thinking_msg.message_id)
        bot.send_message(message.chat.id, response + t["disclaimer"], 
                        parse_mode="Markdown", reply_markup=back_keyboard(lang))

    elif state == "clinic":
        result = search_clinics(text, lang)
        bot.send_message(message.chat.id, result, 
                        parse_mode="Markdown", reply_markup=back_keyboard(lang))

    elif state == "medicine":
        thinking_msg = bot.send_message(message.chat.id, t["thinking"])
        
        if lang == "uz":
            prompt = f"'{text}' dori haqida:\n1. Nima uchun ishlatiladi\n2. Qanday dozada ichiladi\n3. Yon ta'sirlari\n4. Kimlar ichmashi kerak emas\n5. Boshqa eslatmalar"
        else:
            prompt = f"О препарате '{text}':\n1. Для чего применяется\n2. Дозировка\n3. Побочные эффекты\n4. Противопоказания\n5. Важные примечания"
        
        response = ask_ai(prompt, lang)
        bot.delete_message(message.chat.id, thinking_msg.message_id)
        bot.send_message(message.chat.id, response + t["disclaimer"], 
                        parse_mode="Markdown", reply_markup=back_keyboard(lang))

    else:
        # Oddiy savollar uchun AI javob beradi
        thinking_msg = bot.send_message(message.chat.id, t["thinking"])
        response = ask_ai(text, lang)
        bot.delete_message(message.chat.id, thinking_msg.message_id)
        bot.send_message(message.chat.id, response + t["disclaimer"], 
                        parse_mode="Markdown", reply_markup=main_menu_keyboard(lang))

# ═══════════════════════════════════════════════
#  BOTNI ISHGA TUSHIRISH
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    print("🏥 AI Doctor Bot ishga tushdi!")
    print("Botni to'xtatish uchun: Ctrl+C")
    bot.infinity_polling()
