# 🚂 Railway Deploy Qo'llanmasi — AI Doctor Bot

## KERAKLI FAYLLAR (hammasi bir papkada bo'lsin):
```
📁 ai-doctor-bot/
   ├── ai_doctor_bot.py
   ├── requirements.txt
   └── Procfile
```

---

## 1-QADAM: GitHub Repo yaratish

1. https://github.com ga kiring (ro'yxatdan o'ting)
2. **"New repository"** tugmasini bosing
3. Nom: `ai-doctor-bot`
4. **"Create repository"** tugmasini bosing
5. Fayllarni yuklang:
   - `ai_doctor_bot.py`
   - `requirements.txt`
   - `Procfile`

---

## 2-QADAM: Railway ga kirish

1. https://railway.app ga kiring
2. **"Login with GitHub"** tugmasini bosing
3. GitHub akkauntingiz bilan kiring

---

## 3-QADAM: Yangi Loyiha yaratish

1. **"New Project"** tugmasini bosing
2. **"Deploy from GitHub repo"** ni tanlang
3. `ai-doctor-bot` reponi tanlang
4. **"Deploy Now"** tugmasini bosing

---

## 4-QADAM: Environment Variables (MUHIM!)

> Bu yerda tokenlarni kiritasiz — kodga yozmasdan!

1. Loyihangizni oching
2. **"Variables"** bo'limiga kiring
3. Quyidagi 2 ta o'zgaruvchini qo'shing:

```
BOT_TOKEN = 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ANTHROPIC_API_KEY = sk-ant-api03-...
```

---

## 5-QADAM: Kodni yangilash

`ai_doctor_bot.py` faylida tokenlarni environment variable dan olishi uchun
quyidagi qatorlarni o'zgartiring:

### ESKI (o'chirish kerak):
```python
BOT_TOKEN = "BU_YERGA_BOT_TOKENINI_KO'CHING"
ANTHROPIC_API_KEY = "BU_YERGA_ANTHROPIC_API_KEYni_KO'CHING"
```

### YANGI (shu bilan almashtiring):
```python
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
```

---

## 6-QADAM: Deploy

1. GitHub ga o'zgartirilgan faylni yuklang
2. Railway avtomatik qayta deploy qiladi
3. **"Logs"** bo'limida `🏥 AI Doctor Bot ishga tushdi!` ko'rsangiz — muvaffaqiyat!

---

## ✅ TEKSHIRISH

Telegramda botingizni toping va `/start` yozing.
Ishlasa — tabriklaymiz! 🎉

---

## ❌ XATO BO'LSA

| Xato | Yechim |
|------|--------|
| `ModuleNotFoundError` | requirements.txt to'g'ri yuklanganini tekshiring |
| `Invalid token` | BOT_TOKEN ni Railway Variables da tekshiring |
| `AuthenticationError` | ANTHROPIC_API_KEY ni tekshiring |
| Bot javob bermayapti | Railway Logs ni ko'ring |

---

## 💡 FOYDALI MA'LUMOT

- Railway **bepul** $5 kredit beradi (oyiga ~500 soat)
- Bot 24/7 ishlaydi
- Loglarni real vaqtda ko'rish mumkin
- GitHub ga har push qilganda avtomatik yangilanadi
