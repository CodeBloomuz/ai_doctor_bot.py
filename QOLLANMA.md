# 🏥 AI Doctor Bot — Ishga Tushirish Qo'llanmasi

## 1-QADAM: Python o'rnatish
https://python.org ga kiring va Python 3.10+ ni yuklab oling

## 2-QADAM: Kutubxonalarni o'rnatish
Terminal (cmd) ni oching va yozing:
```
pip install pytelegrambotapi anthropic requests
```

## 3-QADAM: Bot Token olish (@BotFather)
1. Telegramda @BotFather ni toping
2. /newbot deb yozing
3. Bot nomini kiriting (masalan: AI Doctor Uz)
4. Username kiriting (masalan: ai_doctor_uz_bot)
5. Token beriladi — UNI SAQLANG!

## 4-QADAM: Anthropic API Key olish
1. https://console.anthropic.com ga kiring
2. Ro'yxatdan o'ting
3. "API Keys" bo'limiga kiring
4. "Create Key" tugmasini bosing
5. Kalitni saqlang

## 5-QADAM: Kodni sozlash
ai_doctor_bot.py faylini oching va:

```python
BOT_TOKEN = "BU_YERGA_BOT_TOKENINI_KO'CHING"
ANTHROPIC_API_KEY = "BU_YERGA_ANTHROPIC_API_KEYni_KO'CHING"
```

Bu ikki qatorni o'z tokenlaringiz bilan almashtiring.

## 6-QADAM: Botni ishga tushirish
```
python ai_doctor_bot.py
```

## BOT FUNKSIYALARI ✅
- 🤒 Simptom tahlili (AI tomonidan)
- 👨‍⚕️ Shifokor tavsiyasi
- 🏥 Klinika qidirish (Google Maps)
- 💊 Dori ma'lumoti
- 🌐 O'zbekcha / Ruscha til

## MUAMMO BO'LSA
@BotFather dan yangi token oling va qaytadan urinib ko'ring.
