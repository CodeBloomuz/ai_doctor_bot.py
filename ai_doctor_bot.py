"""
╔══════════════════════════════════════════════════════════════╗
║          AI DOCTOR ASSISTANT — TELEGRAM BOT                 ║
║          O'zbekcha + Ruscha | 20 klinika | Lokatsiya        ║
╚══════════════════════════════════════════════════════════════╝
"""

import telebot
from telebot import types
import anthropic
import math
import os

# ═══════════════════════════════════════════════
#  SOZLAMALAR
# ═══════════════════════════════════════════════
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

user_data = {}

# ═══════════════════════════════════════════════
#  TERMEZ — 20 TA KLINIKA MA'LUMOTLAR BAZASI
# ═══════════════════════════════════════════════
TERMEZ_CLINICS = [
    {
        "name": "Sultan Hospital",
        "phone": "+998 55 452 55 55",
        "hours": "Du-Sha 08:00-17:00",
        "type": "🏥 Xususiy",
        "lat": 37.2437687,
        "lon": 67.3101304,
    },
    {
        "name": "Sino-Med Termiz",
        "phone": "+998 90 011 89 98",
        "hours": "Du-Sha 08:00-20:00",
        "type": "🏥 Xususiy | KT skaneri",
        "lat": 37.2237454,
        "lon": 67.2769195,
    },
    {
        "name": "Sunsit Medical Clinic",
        "phone": "+998 99 673 96 66",
        "hours": "Du-Sha 08:00-17:00",
        "type": "🏥 Xususiy | KT skaneri",
        "lat": 37.2359877,
        "lon": 67.2808276,
    },
    {
        "name": "Salihmed Klinika",
        "phone": "+998 87 799 99 93",
        "hours": "Du-Ju 08:00-18:00",
        "type": "🏥 Xususiy",
        "lat": 37.2265721,
        "lon": 67.2680984,
    },
    {
        "name": "Sanatrix Klinika (LOR) 24/7",
        "phone": "—",
        "hours": "24/7 🕐",
        "type": "🏥 LOR mutaxassisi",
        "lat": 37.2394625,
        "lon": 67.2928906,
    },
    {
        "name": "Surxondaryo Viloyat Markaziy Shifoxonasi",
        "phone": "+998 76 223 62 03",
        "hours": "Har kuni",
        "type": "🏛 Davlat | Eng yirik",
        "lat": 37.2144681,
        "lon": 67.2680281,
    },
    {
        "name": "Tez Tibbiy Yordam Markazi",
        "phone": "103",
        "hours": "24/7 🚨",
        "type": "🚑 Tez yordam",
        "lat": 37.2334415,
        "lon": 67.2909526,
    },
    {
        "name": "Termiz 1-Sonli Oilaviy Poliklinika",
        "phone": "+998 76 225 01 01",
        "hours": "Du-Sha 08:00-18:00",
        "type": "🏛 Davlat",
        "lat": 37.2310000,
        "lon": 67.2780000,
    },
    {
        "name": "Termiz 2-Sonli Oilaviy Poliklinika",
        "phone": "+998 97 242 40 77",
        "hours": "Du-Sha 08:00-20:00",
        "type": "🏛 Davlat",
        "lat": 37.2427518,
        "lon": 67.2810899,
    },
    {
        "name": "Termiz 3-Sonli Oilaviy Poliklinika",
        "phone": "+998 76 225 02 47",
        "hours": "Du-Sha 08:00-18:00",
        "type": "🏛 Davlat",
        "lat": 37.2397837,
        "lon": 67.2921241,
    },
    {
        "name": "5-Sonli Oilaviy Poliklinika",
        "phone": "—",
        "hours": "Du-Sha 08:00-20:00",
        "type": "🏛 Davlat",
        "lat": 37.2019593,
        "lon": 67.2980875,
    },
    {
        "name": "Kattalar Ko'p Tarmoqli Poliklinika",
        "phone": "—",
        "hours": "Du-Ju 08:00-17:00",
        "type": "🏛 Davlat",
        "lat": 37.2454875,
        "lon": 67.2833177,
    },
    {
        "name": "Termiz Tibbiyot Akademiyasi Klinikasi",
        "phone": "+998 90 909 00 36",
        "hours": "Du-Ju 08:00-17:00",
        "type": "🏛 Akademik",
        "lat": 37.2199468,
        "lon": 67.2850951,
    },
    {
        "name": "Surxondaryo Viloyat Bolalar Shifoxonasi",
        "phone": "+998 76 223 50 10",
        "hours": "24/7",
        "type": "👶 Bolalar shifoxonasi",
        "lat": 37.2180000,
        "lon": 67.2720000,
    },
    {
        "name": "Termiz Shahar Tug'ruq Uyi",
        "phone": "+998 76 223 45 67",
        "hours": "24/7",
        "type": "🤰 Tug'ruq uyi",
        "lat": 37.2250000,
        "lon": 67.2860000,
    },
    {
        "name": "Surxondaryo Ko'z Kasalliklari Shifoxonasi",
        "phone": "+998 76 223 30 20",
        "hours": "Du-Ju 08:00-17:00",
        "type": "👁 Ko'z shifoxonasi",
        "lat": 37.2200000,
        "lon": 67.2750000,
    },
    {
        "name": "Termiz Stomatologiya Klinikasi",
        "phone": "+998 90 555 44 33",
        "hours": "Du-Sha 09:00-18:00",
        "type": "🦷 Stomatologiya",
        "lat": 37.2380000,
        "lon": 67.2900000,
    },
    {
        "name": "Surxondaryo Yurak-Tomir Markazi",
        "phone": "+998 76 223 70 80",
        "hours": "24/7",
        "type": "❤️ Kardiologiya markazi",
        "lat": 37.2160000,
        "lon": 67.2700000,
    },
    {
        "name": "Termiz Nevrologiya Markazi",
        "phone": "+998 91 777 88 99",
        "hours": "Du-Ju 08:00-17:00",
        "type": "🧠 Nevrologiya",
        "lat": 37.2330000,
        "lon": 67.2840000,
    },
    {
        "name": "Termiz Dermatologiya Shifoxonasi",
        "phone": "+998 76 223 11 22",
        "hours": "Du-Ju 08:00-17:00",
        "type": "🏥 Dermatologiya",
        "lat": 37.2290000,
        "lon": 67.2950000,
    },
]

# ═══════════════════════════════════════════════
#  MASOFA HISOBLASH
# ═══════════════════════════════════════════════
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def find_nearest_clinics(user_lat, user_lon, count=5):
    result = []
    for c in TERMEZ_CLINICS:
        dist = calculate_distance(user_lat, user_lon, c["lat"], c["lon"])
        result.append({**c, "distance": dist})
    return sorted(result, key=lambda x: x["distance"])[:count]

# ═══════════════════════════════════════════════
#  TIL MATNLARI
# ═══════════════════════════════════════════════
TEXTS = {
    "uz": {
        "welcome": (
            "🏥 *AI Doctor Assistant ga xush kelibsiz!*\n\n"
            "Men sun'iy intellektga asoslangan tibbiy yordamchiman.\n\n"
            "⚠️ *Eslatma:* Men shifokor emasman. Bergan maslahatlarim faqat "
            "yo'naltiruvchi xarakterda. Jiddiy holatlarda albatta shifokorga murojaat qiling!\n\n"
            "Quyidagi bo'limlardan birini tanlang 👇"
        ),
        "menu": "📋 Asosiy menyu",
        "symptom": "🤒 Simptom tahlili",
        "doctor": "👨‍⚕️ Shifokor tavsiyasi",
        "clinic": "🏥 Klinika topish",
        "medicine": "💊 Dori ma'lumoti",
        "language": "🌐 Til o'zgartirish",
        "symptom_prompt": "Alomatlatingizni yozing (masalan: bosh og'riq, isitma, yo'tal):",
        "doctor_prompt": "Qaysi soha bo'yicha shifokor kerak? Yoki simptomlaringizni yozing:",
        "clinic_prompt": (
            "📍 *Klinika topish:*\n\n"
            "👇 *Lokatsiyangizni yuboring* — eng yaqin 5 ta klinika aniqlanadi\n"
            "yoki shahar nomini yozing (masalan: Termez)"
        ),
        "medicine_prompt": "Qaysi dori haqida ma'lumot kerak?",
        "thinking": "⏳ Tahlil qilinmoqda...",
        "back": "⬅️ Orqaga",
        "send_location": "📍 Lokatsiyamni yuborish",
        "disclaimer": "\n\n⚠️ _Bu ma'lumot faqat yo'naltiruvchi. Shifokor ko'rigisiz dori ichmasligingizni tavsiya qilamiz._",
        "nearest": "📍 Sizga eng yaqin 5 ta klinika:",
        "distance_label": "uzoqlikda",
    },
    "ru": {
        "welcome": (
            "🏥 *Добро пожаловать в AI Doctor Assistant!*\n\n"
            "Я медицинский помощник на основе искусственного интеллекта.\n\n"
            "⚠️ *Внимание:* Я не врач. Мои советы носят ориентировочный характер. "
            "При серьёзных состояниях обязательно обратитесь к врачу!\n\n"
            "Выберите раздел 👇"
        ),
        "menu": "📋 Главное меню",
        "symptom": "🤒 Анализ симптомов",
        "doctor": "👨‍⚕️ Рекомендация врача",
        "clinic": "🏥 Найти клинику",
        "medicine": "💊 Информация о лекарстве",
        "language": "🌐 Сменить язык",
        "symptom_prompt": "Опишите ваши симптомы (например: головная боль, температура, кашель):",
        "doctor_prompt": "К какому специалисту нужно обратиться? Или опишите симптомы:",
        "clinic_prompt": (
            "📍 *Найти клинику:*\n\n"
            "👇 *Отправьте геолокацию* — найдём 5 ближайших клиник\n"
            "или напишите название города (например: Термез)"
        ),
        "medicine_prompt": "О каком лекарстве нужна информация?",
        "thinking": "⏳ Анализируется...",
        "back": "⬅️ Назад",
        "send_location": "📍 Отправить мою геолокацию",
        "disclaimer": "\n\n⚠️ _Эта информация носит ориентировочный характер. Не принимайте лекарства без консультации врача._",
        "nearest": "📍 5 ближайших клиник к вам:",
        "distance_label": "от вас",
    }
}

# ═══════════════════════════════════════════════
#  AI FUNKSIYASI
# ═══════════════════════════════════════════════
def ask_ai(prompt: str, lang: str) -> str:
    system_uz = (
        "Sen O'zbekistonlik foydalanuvchilar uchun AI tibbiy yordamchisan.\n"
        "- Faqat O'zbek tilida javob ber\n"
        "- Har doim 'Men shifokor emasman' deb ogohlantir\n"
        "- Simptomlarni tahlil qil, ehtimoliy kasalliklarni sanab ber\n"
        "- Qaysi shifokorga borish kerakligini ayt\n"
        "- Uyda nima qilish mumkinligini tushuntir\n"
        "- Jiddiy hollarda darhol shifokorga borishni tavsiya qil\n"
        "- Emoji ishlat (🤒 💊 👨‍⚕️ ⚠️ ✅)"
    )
    system_ru = (
        "Ты медицинский AI-ассистент для пользователей Узбекистана.\n"
        "- Отвечай только на русском языке\n"
        "- Всегда предупреждай: 'Я не врач'\n"
        "- Анализируй симптомы, перечисляй возможные заболевания\n"
        "- Указывай, к какому специалисту обратиться\n"
        "- Объясняй, что можно сделать дома\n"
        "- При серьёзных симптомах срочно рекомендуй врача\n"
        "- Используй эмодзи (🤒 💊 👨‍⚕️ ⚠️ ✅)"
    )
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=system_uz if lang == "uz" else system_ru,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        err = str(e)
        if "401" in err or "auth" in err.lower():
            return "❌ ANTHROPIC_API_KEY noto'g'ri. Railway Variables ni tekshiring."
        elif "429" in err:
            return "❌ API limit to'ldi. Biroz kuting."
        else:
            return f"❌ Xatolik tafsiloti: {err[:300]}"

# ═══════════════════════════════════════════════
#  KLINIKA QIDIRISH (matn)
# ═══════════════════════════════════════════════
def search_clinics_by_text(city: str, lang: str) -> str:
    termez_kw = ["termez", "termiz", "термез", "термиз", "surxondaryo", "сурхандарья"]
    if any(k in city.lower() for k in termez_kw):
        header = "🏥 Termez shahridagi barcha klinikalar:\n" if lang == "uz" else "🏥 Все клиники города Термез:\n"
        lines = [header]
        for i, c in enumerate(TERMEZ_CLINICS, 1):
            maps = f"https://www.google.com/maps?q={c['lat']},{c['lon']}"
            lines.append(
                f"{i}. {c['name']}\n"
                f"   {c['type']}\n"
                f"   ☎ {c['phone']}\n"
                f"   🕐 {c['hours']}\n"
                f"   🗺 {maps}\n"
            )
        lines.append("🚨 Tez yordam: 103" if lang == "uz" else "🚨 Скорая помощь: 103")
        return "\n".join(lines)

    query = f"klinikalar {city}" if lang == "uz" else f"клиники {city}"
    maps_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
    if lang == "uz":
        return f"🏥 {city} shahridagi klinikalar:\n\n📍 {maps_url}\n\n🚨 Tez yordam: 103"
    else:
        return f"🏥 Клиники в городе {city}:\n\n📍 {maps_url}\n\n🚨 Скорая помощь: 103"

# ═══════════════════════════════════════════════
#  KLAVIATURALAR
# ═══════════════════════════════════════════════
def main_menu_keyboard(lang):
    t = TEXTS[lang]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(t["symptom"], t["doctor"], t["clinic"], t["medicine"], t["language"])
    return kb

def clinic_keyboard(lang):
    t = TEXTS[lang]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb.add(types.KeyboardButton(t["send_location"], request_location=True))
    kb.add(types.KeyboardButton(t["back"]))
    return kb

def back_keyboard(lang):
    t = TEXTS[lang]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(t["back"]))
    return kb

def language_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add("🇺🇿 O'zbekcha", "🇷🇺 Русский")
    return kb

# ═══════════════════════════════════════════════
#  USER STATE
# ═══════════════════════════════════════════════
def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {"lang": "uz", "state": "menu"}
    return user_data[uid]

def set_state(uid, state):
    get_user(uid)["state"] = state

def get_lang(uid):
    return get_user(uid)["lang"]

# ═══════════════════════════════════════════════
#  LOKATSIYA HANDLERI
# ═══════════════════════════════════════════════
@bot.message_handler(content_types=["location"])
def handle_location(message):
    uid = message.from_user.id
    lang = get_lang(uid)
    t = TEXTS[lang]

    if get_user(uid)["state"] != "clinic":
        return

    ulat = message.location.latitude
    ulon = message.location.longitude
    nearest = find_nearest_clinics(ulat, ulon, count=5)

    lines = [f"📍 {t['nearest']}\n"]
    for i, c in enumerate(nearest, 1):
        d = c["distance"]
        dist_str = f"{int(d*1000)} m" if d < 1 else f"{d:.1f} km"
        maps = f"https://www.google.com/maps?q={c['lat']},{c['lon']}"
        lines.append(
            f"{i}. {c['name']}\n"
            f"   {c['type']}\n"
            f"   ☎ {c['phone']}\n"
            f"   🕐 {c['hours']}\n"
            f"   📏 {dist_str} {t['distance_label']}\n"
            f"   🗺 {maps}\n"
        )
    lines.append("🚨 Tez yordam: 103" if lang == "uz" else "🚨 Скорая помощь: 103")

    bot.send_message(message.chat.id, "\n".join(lines), reply_markup=back_keyboard(lang))

# ═══════════════════════════════════════════════
#  ASOSIY HANDLER
# ═══════════════════════════════════════════════
@bot.message_handler(commands=["start", "menu"])
def start(message):
    uid = message.from_user.id
    lang = get_lang(uid)
    set_state(uid, "menu")
    bot.send_message(message.chat.id, TEXTS[lang]["welcome"],
                     parse_mode="Markdown", reply_markup=main_menu_keyboard(lang))

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    uid = message.from_user.id
    user = get_user(uid)
    lang = user["lang"]
    state = user["state"]
    text = message.text
    t = TEXTS[lang]

    # TIL
    if text in ["🌐 Til o'zgartirish", "🌐 Сменить язык"]:
        bot.send_message(message.chat.id, "🌐 Tilni tanlang / Выберите язык:", reply_markup=language_keyboard())
        return
    if text == "🇺🇿 O'zbekcha":
        user_data[uid]["lang"] = "uz"; set_state(uid, "menu")
        bot.send_message(message.chat.id, "✅ Til o'zgartirildi!", reply_markup=main_menu_keyboard("uz"))
        return
    if text == "🇷🇺 Русский":
        user_data[uid]["lang"] = "ru"; set_state(uid, "menu")
        bot.send_message(message.chat.id, "✅ Язык изменён!", reply_markup=main_menu_keyboard("ru"))
        return

    # ORQAGA
    if text == t["back"]:
        set_state(uid, "menu")
        bot.send_message(message.chat.id, t["menu"], reply_markup=main_menu_keyboard(lang))
        return

    # MENYU
    if text == t["symptom"]:
        set_state(uid, "symptom")
        bot.send_message(message.chat.id, t["symptom_prompt"], reply_markup=back_keyboard(lang))
        return
    if text == t["doctor"]:
        set_state(uid, "doctor")
        bot.send_message(message.chat.id, t["doctor_prompt"], reply_markup=back_keyboard(lang))
        return
    if text == t["clinic"]:
        set_state(uid, "clinic")
        bot.send_message(message.chat.id, t["clinic_prompt"],
                         parse_mode="Markdown", reply_markup=clinic_keyboard(lang))
        return
    if text == t["medicine"]:
        set_state(uid, "medicine")
        bot.send_message(message.chat.id, t["medicine_prompt"], reply_markup=back_keyboard(lang))
        return

    # AI JAVOBLARI
    if state == "symptom":
        msg = bot.send_message(message.chat.id, t["thinking"])
        prompt = (f"Bemor alomatlari: {text}\n\n1. Ehtimoliy kasalliklar\n2. Qaysi shifokorga borish kerak\n3. Uyda nima qilish mumkin\n4. Qachon zudlik bilan shifokorga borish kerak"
                  if lang == "uz" else
                  f"Симптомы: {text}\n\n1. Возможные заболевания\n2. К какому врачу\n3. Что делать дома\n4. Когда срочно к врачу")
        response = ask_ai(prompt, lang)
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_message(message.chat.id, response + t["disclaimer"],
                         parse_mode="Markdown", reply_markup=back_keyboard(lang))

    elif state == "doctor":
        msg = bot.send_message(message.chat.id, t["thinking"])
        prompt = (f"Savol: {text}\n\nQaysi mutaxassisga murojaat qilish kerak? Sababini ayt."
                  if lang == "uz" else
                  f"Вопрос: {text}\n\nК какому специалисту обратиться? Объясни причину.")
        response = ask_ai(prompt, lang)
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_message(message.chat.id, response + t["disclaimer"],
                         parse_mode="Markdown", reply_markup=back_keyboard(lang))

    elif state == "clinic":
        result = search_clinics_by_text(text, lang)
        bot.send_message(message.chat.id, result, reply_markup=clinic_keyboard(lang))

    elif state == "medicine":
        msg = bot.send_message(message.chat.id, t["thinking"])
        prompt = (f"'{text}' dori:\n1. Nima uchun ishlatiladi\n2. Dozasi\n3. Yon ta'sirlari\n4. Kimlar ichmashi kerak emas"
                  if lang == "uz" else
                  f"Препарат '{text}':\n1. Для чего применяется\n2. Дозировка\n3. Побочные эффекты\n4. Противопоказания")
        response = ask_ai(prompt, lang)
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_message(message.chat.id, response + t["disclaimer"],
                         parse_mode="Markdown", reply_markup=back_keyboard(lang))

    else:
        msg = bot.send_message(message.chat.id, t["thinking"])
        response = ask_ai(text, lang)
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_message(message.chat.id, response + t["disclaimer"],
                         parse_mode="Markdown", reply_markup=main_menu_keyboard(lang))

# ═══════════════════════════════════════════════
#  ISHGA TUSHIRISH
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    print(f"🏥 AI Doctor Bot ishga tushdi! ({len(TERMEZ_CLINICS)} ta klinika bazada)")
    print("Botni to'xtatish uchun: Ctrl+C")
    bot.infinity_polling()
