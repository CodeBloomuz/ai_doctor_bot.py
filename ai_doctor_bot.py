"""
╔══════════════════════════════════════════════════════════════╗
║          AI DOCTOR ASSISTANT — TELEGRAM BOT                 ║
║          O'zbekcha + Ruscha | 20 klinika | Lokatsiya        ║
╚══════════════════════════════════════════════════════════════╝
"""

import telebot
from telebot import types
import math
import os

# ═══════════════════════════════════════════════
#  200 GA YAQIN KASALLIK BAZASI
# ═══════════════════════════════════════════════
DISEASES = {
    "bosh og'riq": {"ehtimoliy": ["Migren", "Zo'riqish bosh og'rig'i", "Gipertenziya", "Sinusit", "Ko'z charchashi"], "shifokor": "Nevropatolog yoki Terapevt", "uy": "Dam oling, suv iching, qorong'i xonada yoting, Paratsetamol 500mg", "xavfli": ["Qattiq to'satdan bosh og'riq", "Ko'rish buzilishi", "Qusish bilan birga"]},
    "bosh aylanish": {"ehtimoliy": ["BPPV", "Labirintit", "Gipotoniya", "Kamqonlik"], "shifokor": "Nevropatolog yoki LOR", "uy": "Sekin turing, suv iching, yoting", "xavfli": ["Yiqilish", "Gapirishda qiyinchilik", "Bir tomonda zaiflik"]},
    "bosh og'riq isitma": {"ehtimoliy": ["Gripp", "ARVI", "Meningit (xavfli)", "COVID-19"], "shifokor": "Terapevt", "uy": "Ko'p suv iching, Paratsetamol, dam oling", "xavfli": ["Bo'yin qattiqligi", "Yorug'likdan qo'rqish", "39°C dan yuqori"]},
    "isitma": {"ehtimoliy": ["ARVI", "Gripp", "Angina", "Pnevmoniya", "COVID-19"], "shifokor": "Terapevt", "uy": "Ko'p suv iching, Paratsetamol 500mg, nam lattadan bosing", "xavfli": ["39.5°C dan yuqori", "Teri toshmasi", "Nafas qisishi"]},
    "yuqori isitma": {"ehtimoliy": ["Gripp", "Pnevmoniya", "Angina"], "shifokor": "Terapevt — TEZDA", "uy": "Paratsetamol, suv, shifokor chaqiring", "xavfli": ["40°C dan yuqori — 103 ga qo'ng'iroq!"]},
    "isitma yo'tal": {"ehtimoliy": ["Gripp", "ARVI", "Bronxit", "Pnevmoniya", "COVID-19"], "shifokor": "Terapevt", "uy": "Issiq choy, asal, limon, dam oling", "xavfli": ["Nafas qisishi", "Qon aralash balg'am"]},
    "isitma tomoq og'rishi": {"ehtimoliy": ["Angina", "Faringit", "Gripp"], "shifokor": "LOR yoki Terapevt", "uy": "Tuzli suv bilan chayish, Strepsils", "xavfli": ["Yutishda juda qiyin", "Nafas qisishi"]},
    "tomoq og'rishi": {"ehtimoliy": ["Faringit", "Angina", "Laringit", "ARVI"], "shifokor": "LOR", "uy": "Tuzli suv bilan chayish, Strepsils, issiq choy", "xavfli": ["Nafas qisishi", "Og'iz ochib bo'lmasa"]},
    "tomoq og'rishi yutishda qiyin": {"ehtimoliy": ["Angina", "Peritonsillyar abscess"], "shifokor": "LOR — TEZDA", "uy": "Sovuq narsa iste'mol qiling", "xavfli": ["Nafas qisishi — 103!"]},
    "ovoz yo'qolishi": {"ehtimoliy": ["Laringit", "Sovuq"], "shifokor": "LOR", "uy": "Jim turing, issiq suv iching", "xavfli": ["2 haftadan ko'p davom etsa"]},
    "yo'tal": {"ehtimoliy": ["ARVI", "Bronxit", "Faringit", "Allergiya", "Astma"], "shifokor": "Terapevt yoki Pulmonolog", "uy": "Asal + limon, bug' ustida nafas oling, ko'p suv iching", "xavfli": ["Qon yo'talsangiz", "Nafas qisishi", "1 oydan ko'p"]},
    "quruq yo'tal": {"ehtimoliy": ["Faringit", "Allergiya", "Astma", "GERD"], "shifokor": "Terapevt", "uy": "Asal, nam havo", "xavfli": ["Tunda kuchayadigan yo'tal"]},
    "nam yo'tal": {"ehtimoliy": ["Bronxit", "Pnevmoniya"], "shifokor": "Terapevt yoki Pulmonolog", "uy": "Ko'p suv iching, bug' ustida nafas oling", "xavfli": ["Sariq-yashil balg'am", "Qon aralash"]},
    "nafas qisishi": {"ehtimoliy": ["Astma", "Pnevmoniya", "Yurak yetishmovchiligi", "Anemiya", "COVID-19"], "shifokor": "Terapevt — TEZDA", "uy": "O'tiring, toza havo, inhaler", "xavfli": ["Dam olishda ham nafas qisishi — 103!"]},
    "astma": {"ehtimoliy": ["Bronxial astma hujumi"], "shifokor": "Pulmonolog", "uy": "Inhaler ishlating, o'tiring, toza havo", "xavfli": ["Inhaler yordam bermasa — 103!"]},
    "ko'krak og'rishi": {"ehtimoliy": ["Stenokardia", "Miokard infarkti", "Qovurg'a nevralgia", "Gastrit"], "shifokor": "Kardiolog — TEZDA", "uy": "Dam oling, Nitroglitserin", "xavfli": ["Chap qo'lga tarqalsa", "Ter bossa — 103!"]},
    "yurak urishi tez": {"ehtimoliy": ["Taxikardiya", "Stress", "Anemiya", "Qalqonsimon bez"], "shifokor": "Kardiolog", "uy": "Dam oling, chuqur nafas, kofe ichmang", "xavfli": ["Ko'krak og'rig'i bilan"]},
    "yurak og'rishi": {"ehtimoliy": ["Stenokardia", "Miokard infarkti"], "shifokor": "Kardiolog — TEZDA", "uy": "Dam oling, Nitroglitserin", "xavfli": ["5 daqiqadan ko'p — 103!"]},
    "qon bosimi yuqori": {"ehtimoliy": ["Gipertenziya", "Stressdan", "Buyrak kasalligi"], "shifokor": "Kardiolog yoki Terapevt", "uy": "Dam oling, dori iching (buyurilgan bo'lsa)", "xavfli": ["180/120 dan yuqori — 103!"]},
    "qon bosimi past": {"ehtimoliy": ["Gipotoniya", "Degidratsiya", "Kamqonlik"], "shifokor": "Terapevt", "uy": "Yoting, oyoqlarni ko'taring, tuzli suv iching", "xavfli": ["Hushdan ketish"]},
    "kamqonlik": {"ehtimoliy": ["Temir tanqisligi anemiyasi", "B12 tanqisligi"], "shifokor": "Terapevt", "uy": "Temir ko'p oziqlar: jigar, grenat", "xavfli": ["Yurak tez urishi", "Nafas qisishi"]},
    "bo'g'im og'rishi": {"ehtimoliy": ["Artroz", "Artrit", "Revmatoid artrit", "Podagra"], "shifokor": "Revmatolog yoki Ortoped", "uy": "Iliq kompres, Ibuprofen", "xavfli": ["Shishish + qizarish + isitma birga"]},
    "tizza og'rishi": {"ehtimoliy": ["Artroz", "Menisk jarohati", "Bursit"], "shifokor": "Ortoped", "uy": "Dam oling, muz qo'ying", "xavfli": ["Qadam bosa olmasa"]},
    "bel og'rishi": {"ehtimoliy": ["Osteoxondroz", "Grij", "Buyrak toshi", "Mushak tortilishi"], "shifokor": "Nevropatolog yoki Ortoped", "uy": "Iliq kompres, dam oling, Diklofenak krem", "xavfli": ["Oyoqqa tarqaladigan og'riq"]},
    "bo'yin og'rishi": {"ehtimoliy": ["Osteoxondroz", "Mushak tortilishi"], "shifokor": "Nevropatolog", "uy": "Iliq kompres", "xavfli": ["Qo'lga tarqaladigan og'riq"]},
    "yelka og'rishi": {"ehtimoliy": ["Periartrit", "Rotator manjet sindromi", "Artroz"], "shifokor": "Ortoped", "uy": "Dam oling, iliq kompres", "xavfli": ["Ko'krak og'rig'i bilan — kardiologga!"]},
    "oyoq shishishi": {"ehtimoliy": ["Venoz yetishmovchilik", "Yurak yetishmovchiligi", "Tromboz"], "shifokor": "Kardiolog yoki Flebolog", "uy": "Oyoqlarni ko'taring", "xavfli": ["Bir oyoq qizarsa va og'risa — tromboz!"]},
    "oyoq uvushishi": {"ehtimoliy": ["Qon aylanish buzilishi", "Osteoxondroz", "Qand kasalligi"], "shifokor": "Nevropatolog", "uy": "Harakatlanib turing, massaj qiling", "xavfli": ["Doimiy uvushish"]},
    "qo'l titroq": {"ehtimoliy": ["Essential tremor", "Parkinson", "Qalqonsimon bez"], "shifokor": "Nevropatolog", "uy": "Kofe va alkogolni kamaytiring", "xavfli": ["Yurish buzilishi bilan"]},
    "me'da og'rishi": {"ehtimoliy": ["Gastrit", "Oshqozon yarasi", "Xelikobakter", "GERD"], "shifokor": "Gastroenterolog", "uy": "Almagel, kichik porsiyalarda yeing", "xavfli": ["Qora najas", "Qusishda qon"]},
    "ich ketishi": {"ehtimoliy": ["Gastroenterit", "Ovqat zaharlanishi", "IBS"], "shifokor": "Terapevt", "uy": "Ko'p suv, Regidron, BRAT parhezi", "xavfli": ["Qonli ich ketish", "12 soatdan ko'p"]},
    "ich qotishi": {"ehtimoliy": ["Funktsional ich qotishi", "IBS", "Suv kam ichish"], "shifokor": "Gastroenterolog", "uy": "Ko'p suv, sabzavot yeing, yuring", "xavfli": ["Qon aralash", "3 haftadan ko'p"]},
    "ko'ngil aynishi": {"ehtimoliy": ["Gastrit", "Ovqat zaharlanishi", "Migren", "Homiladorlik"], "shifokor": "Terapevt", "uy": "Kichik porsiyalarda yeing, zanjabil choy, Motilium", "xavfli": ["Kuchli qusish bilan"]},
    "qusish": {"ehtimoliy": ["Gastroenterit", "Ovqat zaharlanishi", "Migren"], "shifokor": "Terapevt", "uy": "Suv oz-ozdan, Cerucal", "xavfli": ["Qon aralash qusish", "12 soatdan ko'p"]},
    "qorin og'rishi": {"ehtimoliy": ["Gastrit", "Appendisit", "Ichak spazmi", "O't pufagi", "Buyrak toshi"], "shifokor": "Terapevt yoki Jarroh", "uy": "Dam oling", "xavfli": ["O'ng pastki qorin — appendisit!", "Isitma bilan"]},
    "appendisit": {"ehtimoliy": ["O'tkir appendisit"], "shifokor": "Jarroh — 103!", "uy": "HECH NARSA QILMANG — 103!", "xavfli": ["Kechiktirish xavfli!"]},
    "meteorizm": {"ehtimoliy": ["Dispepsiya", "IBS", "Laktoza toqimsizligi"], "shifokor": "Gastroenterolog", "uy": "Espumisan, sekin yeing", "xavfli": ["Kuchli og'riq bilan"]},
    "kuyish hissi me'dada": {"ehtimoliy": ["Gastrit", "GERD", "Oshqozon yarasi"], "shifokor": "Gastroenterolog", "uy": "Almagel, ovqatdan keyin 2 soat yotmang", "xavfli": ["Ko'krak og'rig'i bilan — kardiologga!"]},
    "ishtaha yo'qligi": {"ehtimoliy": ["Gastrit", "Depressiya", "Jigar kasalligi"], "shifokor": "Terapevt", "uy": "Kichik porsiyalarda yeng", "xavfli": ["Vazn yo'qotish bilan 2 haftadan ko'p"]},
    "o't pufagi og'rishi": {"ehtimoliy": ["O't toshlar", "Xoletsistit"], "shifokor": "Gastroenterolog", "uy": "Yog'li ovqatlardan saqlaning, No-shpa", "xavfli": ["Sariqlik", "Kuchli og'riq — 103!"]},
    "sariqlik": {"ehtimoliy": ["Gepatit A/B/C", "O't toshi", "Jigar kasalligi"], "shifokor": "Gastroenterolog — TEZDA", "uy": "Alkogoldan saqlaning, shifokorga boring", "xavfli": ["Isitma bilan — tez yordam!"]},
    "bel og'rishi siydik qilishda qiyin": {"ehtimoliy": ["Buyrak toshi", "Pielonefrit", "Siydik yo'li infeksiyasi"], "shifokor": "Urolog", "uy": "Ko'p suv iching", "xavfli": ["Siydikda qon", "Yuqori isitma — 103!"]},
    "siydik qilishda og'riq": {"ehtimoliy": ["Sistitit", "Uretrit", "Buyrak toshi"], "shifokor": "Urolog", "uy": "Ko'p suv iching, klyukva sharbati", "xavfli": ["Isitma bilan", "Siydikda qon"]},
    "tez-tez siydik": {"ehtimoliy": ["Sistitit", "Qand kasalligi", "Prostata"], "shifokor": "Urolog", "uy": "Ko'p suv iching", "xavfli": ["Og'riq bilan", "Qon bilan"]},
    "ko'z og'rishi": {"ehtimoliy": ["Konjunktivit", "Ko'z charchashi", "Glaukoma"], "shifokor": "Oftalmolog", "uy": "Ko'zingizni ishqamang, Vizin", "xavfli": ["Ko'rish keskin yomonlashsa"]},
    "ko'z qizarishi": {"ehtimoliy": ["Konjunktivit", "Allergiya", "Charchash"], "shifokor": "Oftalmolog", "uy": "Ko'zingizni ishqamang, sun'iy ko'z yoshi", "xavfli": ["Ko'rish buzilishi bilan"]},
    "ko'rish yomonlashishi": {"ehtimoliy": ["Ko'zoynak kerak", "Katarakta", "Glaukoma"], "shifokor": "Oftalmolog", "uy": "Ekrandan uzoqda bo'ling", "xavfli": ["To'satdan ko'rish yo'qolishi — 103!"]},
    "quloq og'rishi": {"ehtimoliy": ["Otit", "Tashqi otit", "Tish og'rig'i tarqalishi"], "shifokor": "LOR", "uy": "Issiq kompres, Otipaks tomchilari", "xavfli": ["Isitma bilan", "Quloqdan oqish"]},
    "quloq bitishi": {"ehtimoliy": ["Oltingugurt tiqin", "Otit", "Bosim o'zgarishi"], "shifokor": "LOR", "uy": "Aguli yuting, burun tomchilarini tomizdiring", "xavfli": ["Eshitish keskin yomonlashsa"]},
    "quloqda shovqin": {"ehtimoliy": ["Tinit", "Qon bosimi yuqori", "Osteoxondroz"], "shifokor": "LOR yoki Nevropatolog", "uy": "Shovqinli joylardan saqlaning", "xavfli": ["Bosh aylanish bilan"]},
    "burun bitishi": {"ehtimoliy": ["ARVI", "Rinit", "Allergiya", "Sinusit"], "shifokor": "LOR", "uy": "Tuzli suv (Aquamaris), Xylometazolin (3 kundan ko'p emas)", "xavfli": ["2 haftadan ko'p", "Sariq-yashil oqish"]},
    "burun oqishi": {"ehtimoliy": ["ARVI", "Allergik rinit", "Sinusit"], "shifokor": "LOR yoki Allergolog", "uy": "Tuzli suv bilan yuving", "xavfli": ["Sariq-yashil, qalin oqish — sinusit!"]},
    "qon ketishi burundan": {"ehtimoliy": ["Quruq havo", "Qon bosimi yuqori", "Travma"], "shifokor": "LOR", "uy": "Boshni oldinga eging, burunni qising, muz", "xavfli": ["15 daqiqa to'xtatib bo'lmasa — 103!"]},
    "toshma": {"ehtimoliy": ["Allergiya", "Eshakemi", "Ekzema", "Psoriaz", "Suv chechagi"], "shifokor": "Dermatolog", "uy": "Qashimang, Fenistil gel, Suprastin", "xavfli": ["Nafas qisishi bilan — 103! (anfilaksiya)"]},
    "qichishish": {"ehtimoliy": ["Allergiya", "Ekzema", "Quru teri", "Jigar kasalligi"], "shifokor": "Dermatolog", "uy": "Namlantiruvchi krem, Suprastin", "xavfli": ["Sariqlik bilan — jigar!"]},
    "ekzema": {"ehtimoliy": ["Atopik dermatit", "Kontakt dermatit"], "shifokor": "Dermatolog", "uy": "Yumshoq sovun, namlantiruvchi krem", "xavfli": ["Infeksiya qo'shilsa"]},
    "akne": {"ehtimoliy": ["Oddiy akne", "Gormon muvozanatsizligi"], "shifokor": "Dermatolog", "uy": "Baziron gel, to'g'ri ovqatlanish", "xavfli": ["Kistoz akne"]},
    "soch to'kilishi": {"ehtimoliy": ["Alopetsiya", "Temir tanqisligi", "Stress"], "shifokor": "Dermatolog yoki Trixolog", "uy": "Temir va B vitaminlari", "xavfli": ["Tezda ko'p to'kilsa"]},
    "charchash": {"ehtimoliy": ["Anemiya", "Qalqonsimon bez", "Depressiya", "Uyqu yetishmovchiligi"], "shifokor": "Terapevt", "uy": "Uyquni tartibga soling, vitaminlar", "xavfli": ["2 haftadan ko'p"]},
    "uyqu buzilishi": {"ehtimoliy": ["Insomnya", "Stress", "Depressiya"], "shifokor": "Nevropatolog", "uy": "Bir vaqtda yoting, ekranlarni o'chiring, Melatonin", "xavfli": ["1 oydan ko'p"]},
    "depressiya": {"ehtimoliy": ["Klinik depressiya", "Gormon muvozanatsizligi", "B12 tanqisligi"], "shifokor": "Psixiatr yoki Psixolog", "uy": "Yuring, muloqot qiling, quyosh nuri oling", "xavfli": ["O'z-o'ziga zarar fikrlari — 103!"]},
    "stress": {"ehtimoliy": ["Tashvish buzilishi"], "shifokor": "Psixolog", "uy": "Nafas mashqlari, meditatsiya", "xavfli": ["Panik hujumlar — psixiatrga"]},
    "panik hujum": {"ehtimoliy": ["Panik buzilish"], "shifokor": "Psixiatr", "uy": "Chuqur nafas (4-7-8 usuli), muzli suv", "xavfli": ["Yurak og'rig'i bilan — kardiologga!"]},
    "qand kasalligi belgilari": {"ehtimoliy": ["Qand kasalligi 1-tur", "Qand kasalligi 2-tur"], "shifokor": "Endokrinolog", "uy": "Shakarni kamaytiring, glyukometr bilan tekshiring", "xavfli": ["Hushdan ketish", "Nafasda asetoн hidi — 103!"]},
    "ko'p suv ichish": {"ehtimoliy": ["Qand kasalligi", "Qalqonsimon bez"], "shifokor": "Endokrinolog", "uy": "Qon şekerini tekshiring", "xavfli": ["Tez-tez siydik + holsizlik bilan"]},
    "vazn ortishi": {"ehtimoliy": ["Gipotireoz", "Qand kasalligi", "Ovqatlanish buzilishi"], "shifokor": "Endokrinolog", "uy": "Ovqatlanishni tartibga soling, yuring", "xavfli": ["Tez va sababsiz"]},
    "vazn yo'qotish": {"ehtimoliy": ["Gipertireoz", "Qand kasalligi", "Depressiya", "Onkologiya", "Sil"], "shifokor": "Terapevt — TEZDA", "uy": "Ko'p kaloriyali ovqat yeng", "xavfli": ["1 oyda 5 kg dan ko'p"]},
    "bo'qoq": {"ehtimoliy": ["Gipotireoz", "Gipertireoz", "Yod tanqisligi"], "shifokor": "Endokrinolog", "uy": "Yodlangan tuz ishlating", "xavfli": ["Tez o'sish", "Yutishda qiyin"]},
    "hayz og'rishi": {"ehtimoliy": ["Dismenoreya", "Endometrioz", "Mioma"], "shifokor": "Ginekolog", "uy": "Issiq xalta, Ibuprofen", "xavfli": ["Juda kuchli og'riq", "Ko'p qon ketish"]},
    "hayz kechikishi": {"ehtimoliy": ["Homiladorlik", "Stress", "PKOS", "Menopauza"], "shifokor": "Ginekolog", "uy": "Homiladorlik testini qiling", "xavfli": ["3 oydan ko'p kechikish"]},
    "homiladorlik belgilari": {"ehtimoliy": ["Homiladorlik"], "shifokor": "Ginekolog", "uy": "Homiladorlik testini qiling", "xavfli": ["Qon ketish bilan — tez yordam!"]},
    "prostata muammosi": {"ehtimoliy": ["Benign prostata giperplaziyasi", "Prostatit"], "shifokor": "Urolog", "uy": "Ko'p suv, sovuqdan saqlaning", "xavfli": ["Siydik to'xtatib bo'lmasa — 103!"]},
    "bola isitmasi": {"ehtimoliy": ["ARVI", "Tish chiqishi", "Otit", "Angina"], "shifokor": "Pediatr", "uy": "Paratsetamol (yoshga qarab), ko'p suv", "xavfli": ["3 oydan kichik bolada — 103!", "40°C dan yuqori"]},
    "bola yo'tali": {"ehtimoliy": ["ARVI", "Bronxit", "Allergiya"], "shifokor": "Pediatr", "uy": "Ko'p suv, asal (1 yoshdan)", "xavfli": ["Nafas qisishi", "Ko'karish"]},
    "bola ich ketishi": {"ehtimoliy": ["Rotavirus", "Ovqat zaharlanishi"], "shifokor": "Pediatr", "uy": "Regidron, ko'p suv", "xavfli": ["Dehidratsiya — quruq lab — 103!"]},
    "tish og'rishi": {"ehtimoliy": ["Karies", "Pulpit", "Parodontit"], "shifokor": "Stomatolog", "uy": "Ibuprofen, tuzli suv bilan chayish", "xavfli": ["Yuz shishishi — 103! (abstsess)"]},
    "milk og'rishi": {"ehtimoliy": ["Gingivit", "Parodontit"], "shifokor": "Stomatolog", "uy": "Xlorheksidin, yumshoq cho'tka", "xavfli": ["Isitma bilan"]},
    "allergiya": {"ehtimoliy": ["Mavsumiy allergiya", "Ovqat allergiyasi", "Dori allergiyasi"], "shifokor": "Allergolog", "uy": "Claritin, qo'zg'atuvchidan uzoqlashing", "xavfli": ["Nafas qisishi + yuz shishishi — 103!"]},
    "holsizlik": {"ehtimoliy": ["Anemiya", "Qalqonsimon bez", "Qand kasalligi", "Depressiya"], "shifokor": "Terapevt", "uy": "Vitaminlar, uyquni tartibga soling", "xavfli": ["Nafas qisishi bilan", "Ko'krak og'rig'i bilan"]},
    "ter ko'p": {"ehtimoliy": ["Gipertireoz", "Menopauza", "Yurak kasalligi"], "shifokor": "Terapevt", "uy": "Paxta kiyim, suv ko'p iching", "xavfli": ["Tunda ter + vazn yo'qotish — sil!"]},
    "harorat past": {"ehtimoliy": ["Gipotireoz", "Anemiya", "Qon bosimi past"], "shifokor": "Terapevt", "uy": "Isining, issiq choy", "xavfli": ["35°C dan past — 103!"]},
    "og'iz qurishi": {"ehtimoliy": ["Qand kasalligi", "Degidratsiya", "Dori yon ta'siri"], "shifokor": "Terapevt", "uy": "Ko'p suv iching", "xavfli": ["Ko'p siydik + charchash — qand kasalligi!"]},
    "badbo'y nafas": {"ehtimoliy": ["Tish kasalligi", "Gastrit", "Jigar kasalligi"], "shifokor": "Stomatolog, keyin Gastroenterolog", "uy": "Tishni yaxshi tozalang, suv ko'p iching", "xavfli": ["Asetoн hidi — qand kasalligi krizi!"]},
    "gemorroi": {"ehtimoliy": ["Ichki/tashqi gemorroy", "Anal yoriq"], "shifokor": "Proktolog", "uy": "Relieff, ko'p suv, kletchatka", "xavfli": ["Ko'p qon ketish"]},
    "varikoz": {"ehtimoliy": ["Varikoz venalar", "Venoz yetishmovchilik"], "shifokor": "Flebolog", "uy": "Kompressiya paypoq, oyoqlarni ko'taring", "xavfli": ["Qizarish + og'riq + isish — tromboflebit!"]},
    "shamollash": {"ehtimoliy": ["ARVI", "Rinit", "Faringit", "Gripp"], "shifokor": "Terapevt", "uy": "Ko'p suv, vitamin C, dam oling", "xavfli": ["Isitma 38.5°C dan yuqori"]},
    "gripp": {"ehtimoliy": ["Gripp A/B", "COVID-19"], "shifokor": "Terapevt", "uy": "Dam oling, Paratsetamol, izolyatsiya", "xavfli": ["Nafas qisishi", "Hushdan ketish"]},
    "covid": {"ehtimoliy": ["COVID-19"], "shifokor": "Terapevt", "uy": "Izolyatsiya, Paratsetamol, qorintubuq yoting", "xavfli": ["SpO2 94% dan past — 103!"]},
    "sil": {"ehtimoliy": ["O'pka sili"], "shifokor": "Ftiziatr — TEZDA", "uy": "Shifokorga boring", "xavfli": ["Qon yo'tal, tunda ter — tezda ftiziatrga!"]},
    "insult belgilari": {"ehtimoliy": ["O'tkir insult"], "shifokor": "103 — TEZDA!", "uy": "HECH NARSA QILMANG — 103!", "xavfli": ["Yuz qiyshayishi, qo'l zaiflik — 103!"]},
    "infarkt belgilari": {"ehtimoliy": ["Miokard infarkti"], "shifokor": "103 — TEZDA!", "uy": "Aspirinni bering, yotqizing — 103!", "xavfli": ["Ko'krak og'rig'i + ter + chap qo'lga — 103!"]},
    "semirish": {"ehtimoliy": ["Ortiqcha ovqatlanish", "Gipotireoz", "Qand kasalligi"], "shifokor": "Endokrinolog", "uy": "Ovqatlanishni tartibga soling, yuring", "xavfli": ["BMI 40 dan yuqori"]},
    "ovqat zaharlanishi": {"ehtimoliy": ["Bakterial gastroenterit", "Stafilokokk toksini"], "shifokor": "Terapevt", "uy": "Ko'p suv, Regidron, och turing 4-6 soat", "xavfli": ["39°C isitma", "Qon aralash qusish — 103!"]},
    "teri quruqligi": {"ehtimoliy": ["Gipotireoz", "Degidratsiya", "Ekzema", "Vitamins tanqisligi"], "shifokor": "Dermatolog", "uy": "Namlantiruvchi krem, ko'p suv", "xavfli": ["Qichishish + sariqlik bilan"]},
    "mushak og'rishi": {"ehtimoliy": ["Miozit", "Gripp", "Ortiqcha jismoniy faollik", "Fibromiyalgiya"], "shifokor": "Terapevt yoki Revmatolog", "uy": "Iliq kompres, Ibuprofen, dam oling", "xavfli": ["Zaiflik + qizarish bilan"]},
    "bo'g'in shishishi": {"ehtimoliy": ["Artrit", "Travma", "Podagra", "Infeksion artrit"], "shifokor": "Revmatolog yoki Ortoped", "uy": "Muz qo'ying, dam oling", "xavfli": ["Isitma + qizarish bilan — tezda!"]},
    "tez charchash yugurganda": {"ehtimoliy": ["Yurak yetishmovchiligi", "Anemiya", "Astma", "Past jismoniy tayyorgarlik"], "shifokor": "Kardiolog yoki Terapevt", "uy": "Asta-sekin mashq qiling", "xavfli": ["Ko'krak og'rig'i bilan"]},
    "ich og'rishi kindik atrofi": {"ehtimoliy": ["Gastroenterit", "IBS", "Ichak infeksiyasi"], "shifokor": "Gastroenterolog", "uy": "No-shpa, suv ko'p iching", "xavfli": ["Kuchayib boradigan og'riq — appendisit!"]},
    "qorin pastida og'riq": {"ehtimoliy": ["Sistitit", "Appendisit (o'ngda)", "Ginekologik (ayollarda)", "IBS"], "shifokor": "Terapevt yoki Ginekolog", "uy": "Issiq xalta (infeksiyada emas!)", "xavfli": ["Isitma bilan", "Kuchli og'riq — 103!"]},
    "ko'p terlash tunda": {"ehtimoliy": ["Sil", "Limfoma", "Gipertireoz", "Menopauza"], "shifokor": "Terapevt — TEZDA", "uy": "Shifokorga boring", "xavfli": ["Vazn yo'qotish bilan — albatta shifokorga!"]},
}

def analyze_symptoms(text, lang='uz'):
    text = text.lower().strip()
    if text in DISEASES:
        return DISEASES[text]
    best_match = None
    best_score = 0
    for key in DISEASES:
        words = key.split()
        score = sum(1 for w in words if w in text)
        if score > best_score:
            best_score = score
            best_match = key
    if best_score > 0:
        return DISEASES[best_match]
    return None

# ═══════════════════════════════════════════════
#  SOZLAMALAR
# ═══════════════════════════════════════════════
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

# 200 TA KASALLIK MA'LUMOTLAR BAZASI
DISEASES_DB = {
    # ═══════════════════ BOSh VA BOʻYIN ═══════════════════
    "bosh og'riq": {
        "name": "Bosh og'riq (Golovnaya bol')",
        "ehtimol": ["Migren", "Zo'riqish bosh og'rig'i", "Qon bosimi ko'tarilishi", "Sinusit"],
        "shifokor": "Nevropatolog yoki Terapevt",
        "uyda": "Dam oling, xona havosini yangilang, ko'p suv iching, qorong'u xonada yoting",
        "xavfli": ["Kuchli to'satdan bosh og'riq", "Ko'z oldi qorong'ilashsa", "Qusish bilan birga bo'lsa"],
        "dori": "Paracetamol 500mg yoki Ibuprofen 400mg (ovqatdan keyin)"
    },
    "migren": {
        "name": "Migren",
        "ehtimol": ["Migren"],
        "shifokor": "Nevropatolog",
        "uyda": "Qorong'u va tinch xonada yoting, sovuq kompres qo'ying, kofe iching",
        "xavfli": ["Hushingizdan ketsangiz", "Nutq buzilsa", "Qo'l-oyoq uvishsa"],
        "dori": "Sumatriptan yoki Ibuprofen 400mg"
    },
    "bosh aylanishi": {
        "name": "Bosh aylanishi (Vertigo)",
        "ehtimol": ["Vestibulyar nevrit", "BPPV", "Qon bosimi o'zgarishi", "Kamqonlik"],
        "shifokor": "Nevropatolog yoki LOR",
        "uyda": "Sekin turing, devorga suyaning, ko'p suv iching, keskin harakat qilmang",
        "xavfli": ["Hushdan ketsangiz", "Quloq bitsa", "Ko'rish buzilsa"],
        "dori": "Betaserc 16mg (shifokor tavsiyasi bilan)"
    },

    # ═══════════════════ HARORAT VA GRIPP ═══════════════════
    "isitma": {
        "name": "Isitma (Temperatura)",
        "ehtimol": ["ARVI", "Gripp", "Angina", "Pnevmoniya", "COVID-19"],
        "shifokor": "Terapevt",
        "uyda": "Ko'p suv iching, nam sochiq bilan artining, iliq kiyining",
        "xavfli": ["39.5 dan yuqori bo'lsa", "3 kundan ko'p davom etsa", "Nafas qiynalsa"],
        "dori": "Paracetamol 500mg (har 6 soatda), Ibuprofen 400mg"
    },
    "gripp": {
        "name": "Gripp",
        "ehtimol": ["Gripp A/B", "ARVI"],
        "shifokor": "Terapevt",
        "uyda": "Dam oling, ko'p issiq suv iching, asal-limon choy, vitaminC",
        "xavfli": ["Nafas qiynalsa", "Ko'krak og'risa", "Hushdan ketsangiz"],
        "dori": "Paracetamol, Oseltamivir (Tamiflu) — shifokor tavsiyasi bilan"
    },
    "yo'tal": {
        "name": "Yo'tal",
        "ehtimol": ["ARVI", "Bronxit", "Tomoq yallig'lanishi", "Allergiya"],
        "shifokor": "Terapevt yoki Pulmonolog",
        "uyda": "Asal-sutli ichimlik, bug' ustida nafas oling, hunichay choy",
        "xavfli": ["Qon bilan yo'talsangiz", "2 haftadan ko'p davom etsa", "Nafas qiynalsa"],
        "dori": "Ambroksol (nam yo'tal), Sinekod (quruq yo'tal)"
    },
    "tomoq og'riq": {
        "name": "Tomoq og'rig'i",
        "ehtimol": ["Angina", "Faringit", "Laringit", "ARVI"],
        "shifokor": "LOR yoki Terapevt",
        "uyda": "Tuzli suv bilan chayqash, iliq sut-asal, sovuq ovqat-ichimlikdan saqlaning",
        "xavfli": ["Yutnish qiyin bo'lsa", "Yuqori isitma bilan bo'lsa", "Nafas qiynalsa"],
        "dori": "Strepsils, Faringosept (so'rish uchun), Hexoral purkash"
    },
    "burun bitishi": {
        "name": "Burun bitishi",
        "ehtimol": ["ARVI", "Rinit", "Sinusit", "Allergiya"],
        "shifokor": "LOR",
        "uyda": "Tuzli suv bilan yuving, bug' ustida nafas oling, bosh baland yoting",
        "xavfli": ["2 haftadan ko'p davom etsa", "Yuz og'risa", "Sariq-yashil shilimshiq bo'lsa"],
        "dori": "Aquamaris (burun yuvish), Naftizin (2-3 kun), Xylometazoline"
    },
    "angina": {
        "name": "Angina (Tonsillat)",
        "ehtimol": ["Bakterial angina", "Viral angina"],
        "shifokor": "LOR yoki Terapevt",
        "uyda": "Tuzli suv bilan chayqash, iliq ichimlik, dam oling",
        "xavfli": ["Yutnish mumkin bo'lmasa", "Nafas qiynalsa", "Isitma 39 dan yuqori"],
        "dori": "Antibiotik faqat shifokor tavsiyasi bilan, Paracetamol"
    },
    "sinusit": {
        "name": "Sinusit",
        "ehtimol": ["O'tkir sinusit", "Surunkali sinusit"],
        "shifokor": "LOR",
        "uyda": "Tuzli suv bilan burun yuving, bug' ustida nafas oling, ko'p suv iching",
        "xavfli": ["Ko'z atrofi shishsa", "Kuchli bosh og'riq bo'lsa", "Isitma yuqori bo'lsa"],
        "dori": "Aquamaris, Nasonex (shifokor tavsiyasi bilan)"
    },

    # ═══════════════════ NAFAS OLISH ═══════════════════
    "nafas qiynalik": {
        "name": "Nafas qiynalishi",
        "ehtimol": ["Bronxial astma", "Pnevmoniya", "Yurak yetishmovchiligi", "Allergiya"],
        "shifokor": "Pulmonolog yoki Kardiolog — TEZDA!",
        "uyda": "Tik o'tiring, deraza oching, astma bo'lsa inhalyator ishlating",
        "xavfli": ["DARHOL 103 ga qo'ng'iroq qiling!"],
        "dori": "Salbutamol inhaler (astma uchun) — shifokor tavsiyasi bilan"
    },
    "bronxit": {
        "name": "Bronxit",
        "ehtimol": ["O'tkir bronxit", "Surunkali bronxit"],
        "shifokor": "Terapevt yoki Pulmonolog",
        "uyda": "Ko'p issiq ichimlik iching, dam oling, inhalyatsiya qiling",
        "xavfli": ["Qon bilan yo'talsangiz", "Nafas qiynalsa", "Isitma 38.5 dan yuqori"],
        "dori": "Ambroksol, Bromgeksin — shifokor tavsiyasi bilan"
    },
    "astma": {
        "name": "Bronxial astma",
        "ehtimol": ["Bronxial astma"],
        "shifokor": "Pulmonolog",
        "uyda": "Inhalyator ishlating, allergenllardan uzoqlashing, tik o'tiring",
        "xavfli": ["Inhalyator yordam bermasa — 103!"],
        "dori": "Salbutamol inhaler, Berodual — faqat shifokor tavsiyasi bilan"
    },
    "pnevmoniya": {
        "name": "Pnevmoniya (o'pka yallig'lanishi)",
        "ehtimol": ["Bakterial pnevmoniya", "Viral pnevmoniya"],
        "shifokor": "Terapevt — TEZDA murojaat qiling!",
        "uyda": "Dam oling, ko'p suv iching, haroratni tushiring",
        "xavfli": ["Nafas qiynalsa", "Lablari ko'karsa", "Isitma 39 dan yuqori"],
        "dori": "Antibiotik — FAQAT shifokor tavsiyasi bilan"
    },

    # ═══════════════════ YURAK VA QON TOMIR ═══════════════════
    "ko'krak og'riq": {
        "name": "Ko'krak og'rig'i",
        "ehtimol": ["Stenokardiya", "Miokard infarkti", "Osteoxondroz", "Gastrit"],
        "shifokor": "Kardiolog — TEZDA!",
        "uyda": "Tinch o'tiring, kiyimni bo'shating, deraza oching",
        "xavfli": ["DARHOL 103 ga qo'ng'iroq qiling! Infarkt bo'lishi mumkin!"],
        "dori": "Nitroglitserin (stenokardiya uchun) — shifokor tavsiyasi bilan"
    },
    "yurak urishi tez": {
        "name": "Yurak tez urishi (Taxikardiya)",
        "ehtimol": ["Taxikardiya", "Aritmiya", "Qalqonsimon bez muammosi", "Stress"],
        "shifokor": "Kardiolog",
        "uyda": "Yoting, chuqur nafas oling, yuzingizni sovuq suvga boting",
        "xavfli": ["Ko'krak og'risa", "Hushdan ketsangiz", "Nafas qiynalsa"],
        "dori": "Shifokor ko'rigisiz dori ichmang!"
    },
    "qon bosimi yuqori": {
        "name": "Qon bosimi yuqori (Gipertenziya)",
        "ehtimol": ["Arterial gipertenziya", "Stres", "Buyrak muammosi"],
        "shifokor": "Kardiolog yoki Terapevt",
        "uyda": "Tinch yoting, tuz va kofedan saqlaning, chuqur nafas oling",
        "xavfli": ["180/120 dan yuqori bo'lsa — 103!", "Bosh og'riq + ko'rish buzilsa"],
        "dori": "Kaptoril (vaziyat dori) — shifokor tavsiyasi bilan"
    },
    "qon bosimi past": {
        "name": "Qon bosimi past (Gipotenziya)",
        "ehtimol": ["Gipotenziya", "Kamqonlik", "Suvsizlik"],
        "shifokor": "Terapevt",
        "uyda": "Yoting, oyoqlarni ko'taring, tuzli suv yoki kofe iching",
        "xavfli": ["Hushdan ketsangiz", "Ko'ngil aynisa", "Teri sovib ketsа"],
        "dori": "Kofe, tuzli suv, Citramon"
    },
    "shish": {
        "name": "Shish (Otëk)",
        "ehtimol": ["Yurak yetishmovchiligi", "Buyrak kasalligi", "Venoz yetishmovchilik", "Allergiya"],
        "shifokor": "Kardiolog yoki Terapevt",
        "uyda": "Oyoqlarni ko'taring, tuz kamroq iste'mol qiling, ko'p yuring",
        "xavfli": ["To'satdan shishsa", "Nafas qiynalsa", "Yuz shishsa"],
        "dori": "Shifokor ko'rigisiz dori ichmang!"
    },

    # ═══════════════════ ME'DA VA ICHAK ═══════════════════
    "qorin og'riq": {
        "name": "Qorin og'rig'i",
        "ehtimol": ["Gastrit", "Yarа kasalligi", "Appenditsit", "Ichak spazmı"],
        "shifokor": "Gastroenterolog yoki Terapevt",
        "uyda": "Issiq narsa ichmang, yotib dam oling, engil ovqat iste'mol qiling",
        "xavfli": ["O'ng pastda kuchli og'riq (appenditsit!)", "Qon bilan najas", "Isitma bilan og'riq"],
        "dori": "No-shpa (spazm uchun), Omeprazol (gastrit uchun)"
    },
    "gastrit": {
        "name": "Gastrit",
        "ehtimol": ["O'tkir gastrit", "Surunkali gastrit", "H.pylori infektsiyasi"],
        "shifokor": "Gastroenterolog",
        "uyda": "Ovqat rejimini saqlang, achchiq-sho'r ovqatdan saqlaning, kichik porsiyada yeng",
        "xavfli": ["Qon qusish", "Qora najas", "Kuchli og'riq"],
        "dori": "Omeprazol 20mg, Almagel, Maalox"
    },
    "yarа kasalligi": {
        "name": "Oshqozon yarasi (Yazva)",
        "ehtimol": ["Oshqozon yarasi", "12 barmoq ichak yarasi"],
        "shifokor": "Gastroenterolog",
        "uyda": "Diet ovqat, stress kam, sigaret va alkogoldan saqlaning",
        "xavfli": ["Qon qusish — 103!", "Qora najas", "Kuchli keskin og'riq"],
        "dori": "Omeprazol, De-nol — shifokor tavsiyasi bilan"
    },
    "ich ketish": {
        "name": "Ich ketish (Diareya)",
        "ehtimol": ["Ovqat zaharlanishi", "Ichak infektsiyasi", "Disbakterioz"],
        "shifokor": "Infektsionist yoki Terapevt",
        "uyda": "KO'P suv iching (Regidron), engilgina ovqat yeng, dam oling",
        "xavfli": ["Qon bilan bo'lsa", "24 soatdan ko'p davom etsa", "Bolalarda"],
        "dori": "Regidron, Smekta, Enterofuril"
    },
    "qabziyat": {
        "name": "Qabziyat (Zapor)",
        "ehtimol": ["Funksional qabziyat", "Yo'g'on ichak kasalligi", "Kam suv ichish"],
        "shifokor": "Gastroenterolog",
        "uyda": "Ko'p suv iching, sabzavot-meva yeng, harakatchan bo'ling",
        "xavfli": ["1 haftadan ko'p davom etsa", "Qon bilan najas", "Kuchli qorin og'rig'i"],
        "dori": "Duphalac (laktuloza), Glitserin o'q dori"
    },
    "ko'ngil aynish": {
        "name": "Ko'ngil aynishi (Toshna)",
        "ehtimol": ["Gastrit", "Ovqat zaharlanishi", "Harakatdan bosh aylanish", "Homiladorlik"],
        "shifokor": "Terapevt",
        "uyda": "Yoting, kichik qultumlab sovuq suv iching, yangi havo oling",
        "xavfli": ["Qon bilan qusish", "Kuchli bosh og'riq bilan", "Hushdan ketsangiz"],
        "dori": "Motilium, Cerucal (shifokor tavsiyasi bilan)"
    },
    "qusish": {
        "name": "Qusish",
        "ehtimol": ["Ovqat zaharlanishi", "Gastrit", "Rotavirus", "Bosh miya kasalligi"],
        "shifokor": "Terapevt",
        "uyda": "Suv va Regidron iching, yotib dam oling, ovqat yemang",
        "xavfli": ["Qon bilan qusish — 103!", "To'xtamasa", "Bolalarda suvsizlik belgilari"],
        "dori": "Regidron, Smekta, Cerucal"
    },
    "meteorizm": {
        "name": "Gaz to'planishi (Meteorizm)",
        "ehtimol": ["Disbakterioz", "Laktoza murosasizligi", "IBS"],
        "shifokor": "Gastroenterolog",
        "uyda": "Gaz hosil qiluvchi ovqatlardan saqlaning, ko'p yuring",
        "xavfli": ["Kuchli qorin og'rig'i bilan", "Isitma bilan"],
        "dori": "Espumizan, Smekta"
    },
    "ovqat zaharlanishi": {
        "name": "Ovqat zaharlanishi",
        "ehtimol": ["Bakterial zaharlanish", "Toksik zaharlanish"],
        "shifokor": "Terapevt yoki Infektsionist",
        "uyda": "Ko'p suv iching, oshqozonni yuvish (suv ichirib qustiring), Regidron iching",
        "xavfli": ["Isitma yuqori bo'lsa", "Qon bilan qusish", "Hushdan ketsangiz — 103!"],
        "dori": "Aktivlashtirilgan ko'mir, Regidron, Smekta"
    },
    "appenditsit": {
        "name": "Appenditsit (shubhali)",
        "ehtimol": ["O'tkir appenditsit"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "Og'riq qoldiruvchi ichmang! Issiq qo'ymang! Tez yordam chaqiring!",
        "xavfli": ["O'ng pastda kuchli og'riq — BU XAVFLI!"],
        "dori": "Hech narsa ichmang — operatsiya kerak bo'lishi mumkin!"
    },

    # ═══════════════════ JİGAR VA O'T PUFAGI ═══════════════════
    "jigar og'riq": {
        "name": "Jigar og'rig'i",
        "ehtimol": ["Gepatit", "Jigar sirozi", "O't pufagi kasalligi"],
        "shifokor": "Gastroenterolog yoki Gepatolog",
        "uyda": "Yog'li, spirtli, achchiq ovqatdan saqlaning",
        "xavfli": ["Ko'zlar sariqsa", "Qorin kattalashsa", "Qorin o'ng yuqorisida kuchli og'riq"],
        "dori": "Shifokor ko'rigisiz dori ichmang!"
    },
    "sariqlik": {
        "name": "Sariqlik (Zheltukha)",
        "ehtimol": ["Gepatit A/B/C", "Jigar sirozi", "O't yo'li tiqilib qolishi"],
        "shifokor": "Infektsionist yoki Gastroenterolog — TEZDA!",
        "uyda": "Dam oling, yog'li ovqatdan saqlaning",
        "xavfli": ["Har doim shifokorga murojaat qiling!"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "o't pufagi og'riq": {
        "name": "O't pufagi og'rig'i",
        "ehtimol": ["Xoletsistit", "O't toshi", "Diskineziya"],
        "shifokor": "Gastroenterolog yoki Jarroh",
        "uyda": "Yog'li ovqatdan saqlaning, No-shpa iching",
        "xavfli": ["Kuchli kolik og'riq", "Isitma bilan og'riq", "Sariqlik ko'rinsa"],
        "dori": "No-shpa, Drotaverin — spazm uchun"
    },

    # ═══════════════════ BUYRAK VA SIYDIK YO'LLARI ═══════════════════
    "bel og'riq": {
        "name": "Bel og'rig'i",
        "ehtimol": ["Osteoxondroz", "Buyrak kasalligi", "Mushak tarangligi", "Grija"],
        "shifokor": "Nevropatolog yoki Urolog",
        "uyda": "Issiq belga qo'ying, dam oling, og'ir ko'tarmang",
        "xavfli": ["Siydik qon bilan bo'lsa", "Harorat bilan bel og'risa", "Oyoqlar uvishsa"],
        "dori": "Ibuprofen 400mg, Voltaren gel"
    },
    "buyrak og'riq": {
        "name": "Buyrak og'rig'i",
        "ehtimol": ["Pielonefrit", "Buyrak toshi", "Glomerulonefrit"],
        "shifokor": "Urolog yoki Nefrologik",
        "uyda": "Ko'p suv iching, issiq bel kompres, No-shpa",
        "xavfli": ["Isitma bilan og'riq", "Qon bilan siydik", "Kuchli kolik"],
        "dori": "No-shpa, Ko'p suv — shifokor ko'rigisiz boshqa dori ichmang"
    },
    "siydik qiyin": {
        "name": "Siydik qiyin chiqishi",
        "ehtimol": ["Siydik yo'li infektsiyasi", "Prostata adenomasi (erkaklar)", "Siydik toshi"],
        "shifokor": "Urolog",
        "uyda": "Ko'p suv iching, iliq hammom",
        "xavfli": ["Umuman siydik bo'lmasa — 103!", "Isitma bilan", "Qon bilan siydik"],
        "dori": "Shifokor ko'rigisiz dori ichmang!"
    },
    "tsistit": {
        "name": "Siydik qopi yallig'lanishi (Tsistit)",
        "ehtimol": ["Bakterial tsistit"],
        "shifokor": "Urolog yoki Ginekolog",
        "uyda": "Ko'p suv iching, iliq o'ting, sovuqdan saqlaning",
        "xavfli": ["Isitma bilan", "Qon bilan siydik", "Bel og'riq bilan"],
        "dori": "Furadonin, Monural — shifokor tavsiyasi bilan"
    },

    # ═══════════════════ SUYAK VA BO'G'IMLAR ═══════════════════
    "bo'g'im og'riq": {
        "name": "Bo'g'im og'rig'i (Artralgia)",
        "ehtimol": ["Artrit", "Artroz", "Podagra", "Revmatizm"],
        "shifokor": "Revmatolog",
        "uyda": "Dam oling, sovuq kompres, og'ir jismoniy ish qilmang",
        "xavfli": ["Shishish + qizarish + isitma", "Ko'p bo'g'im bir vaqtda og'risa"],
        "dori": "Ibuprofen 400mg, Voltaren gel"
    },
    "tizza og'riq": {
        "name": "Tizza og'rig'i",
        "ehtimol": ["Artroz", "Menisk yirtilishi", "Ligament jarohat", "Artrit"],
        "shifokor": "Ortoped yoki Travmatolog",
        "uyda": "Dam oling, elastik bandaj, sovuq kompres",
        "xavfli": ["Tizza shishib qolsa", "Yura olmasangiz", "Travmadan keyin"],
        "dori": "Ibuprofen, Voltaren gel"
    },
    "osteoxondroz": {
        "name": "Osteoxondroz",
        "ehtimol": ["Bo'yin osteoxondrozi", "Bel osteoxondrozi"],
        "shifokor": "Nevropatolog yoki Ortoped",
        "uyda": "Massaj, issiq kompres, to'g'ri o'tiring, yostiq balandligi to'g'ri bo'lsin",
        "xavfli": ["Qo'l-oyoq uvishsa", "Siydik nazorat bo'lmasa"],
        "dori": "Ibuprofen, Voltaren gel, B vitamini"
    },
    "suyak sinishi shubhasi": {
        "name": "Suyak sinishi (shubhali)",
        "ehtimol": ["Suyak sinishi", "Darz ketishi"],
        "shifokor": "Travmatolog — TEZDA!",
        "uyda": "Qadam qo'ymang, shinaga olib qo'ying, muzlatib qo'ying",
        "xavfli": ["Har doim shifoxonaga boring — rentgen kerak!"],
        "dori": "Ibuprofen og'riq uchun, lekin rentgensiz davo qilmang"
    },
    "mushak og'riq": {
        "name": "Mushak og'rig'i (Miyalgia)",
        "ehtimol": ["Jismoniy zo'riqish", "Gripp", "Fibromiyalgiya"],
        "shifokor": "Terapevt",
        "uyda": "Issiq hammom, massaj, dam oling",
        "xavfli": ["Isitma bilan mushak og'risa", "Zaiflik kuchli bo'lsa"],
        "dori": "Ibuprofen 400mg, Voltaren gel"
    },

    # ═══════════════════ TERISKIN ═══════════════════
    "teriskin": {
        "name": "Teri qichishi",
        "ehtimol": ["Allergiya", "Ekzema", "Psoriaz", "Qo'ziqorin infektsiyasi"],
        "shifokor": "Dermatolog",
        "uyda": "Sovuq kompres, allergen mahsulotlardan saqlaning, paxta kiyim kiyining",
        "xavfli": ["Butun tana shishsa — 103! (anafilaksiya)", "Nafas qiynalsa"],
        "dori": "Suprastin, Loratadin (allergiya uchun), Fenistil gel"
    },
    "toshma": {
        "name": "Teri toshmasi",
        "ehtimol": ["Allergiya", "Qizilcha", "Suv chechak", "Ekzema", "Dermatit"],
        "shifokor": "Dermatolog",
        "uyda": "Allergendan uzoqlashing, qashimang, paxta kiyim kiyining",
        "xavfli": ["Isitma bilan toshma", "Toshma tez tarqalsa", "Nafas qiynalsa — 103!"],
        "dori": "Loratadin, Fenistil gel — shifokor ko'rigisiz boshqa dori ichmang"
    },
    "yara": {
        "name": "Teri yarasi",
        "ehtimol": ["Bakterial infektsiya", "Trofik yara", "Diabetik yara"],
        "shifokor": "Jarroh yoki Dermatolog",
        "uyda": "Yuvish, zararsizlantirish, steril bog'lam",
        "xavfli": ["Ira paydo bo'lsa", "Qizarish tarqalsa", "Isitma bilan"],
        "dori": "Vodorodni peroksid, Betadin, Levomekol"
    },
    "akne": {
        "name": "Akne (Toshmalar)",
        "ehtimol": ["Gormonal akne", "Bakterial akne"],
        "shifokor": "Dermatolog",
        "uyda": "Yuzni tez-tez yuvish, qishqilmang, yog'li ovqat kamaytiring",
        "xavfli": ["Katta yiringli toshmalarda shifokorga boring"],
        "dori": "Baziron gel, Zinerit — dermatolog tavsiyasi bilan"
    },
    "soch to'kilishi": {
        "name": "Soch to'kilishi (Alopetsiya)",
        "ehtimol": ["Gormonal buzilish", "Stres", "Temir yetishmovchiligi", "Qalqonsimon bez"],
        "shifokor": "Dermatolog yoki Trixolog",
        "uyda": "Soch masaji, to'g'ri ovqatlanish, vitaminlar",
        "xavfli": ["To'satdan ko'p to'kilsa", "Doira shaklida to'kilsa"],
        "dori": "Minoksidil, vitaminlar — shifokor tavsiyasi bilan"
    },

    # ═══════════════════ KO'Z ═══════════════════
    "ko'z og'riq": {
        "name": "Ko'z og'rig'i",
        "ehtimol": ["Konjunktivit", "Glaukoma", "Ko'z bosimligi", "Katarakta"],
        "shifokor": "Oftalmolog",
        "uyda": "Ko'zni uqalamang, qorong'uda dam bering, ekrandan uzoqlashing",
        "xavfli": ["Ko'rish to'satdan yomonlashsa", "Kuchli og'riq va ko'rish buzilsa — tezda!"],
        "dori": "Shifokor ko'rigisiz ko'z tomizg'i ishlating"
    },
    "ko'z qizarishi": {
        "name": "Ko'z qizarishi",
        "ehtimol": ["Konjunktivit", "Allergiya", "Quruq ko'z", "Charchoq"],
        "shifokor": "Oftalmolog",
        "uyda": "Ko'zni yuvish, ekrandan dam oling, qorong'u xona",
        "xavfli": ["Ko'rish yomonlashsa", "Kuchli og'riq bilan", "Yiring chiqsa"],
        "dori": "Vizin (ko'z tomizg'i), Artificial tears"
    },
    "ko'rish yomonlashishi": {
        "name": "Ko'rish yomonlashishi",
        "ehtimol": ["Miopiya", "Gipermetropiya", "Katarakta", "Glaukoma"],
        "shifokor": "Oftalmolog",
        "uyda": "Ko'z mashqlari qiling, ekran vaqtini kamaytiring",
        "xavfli": ["To'satdan ko'rish yo'qolsa — 103!", "Ko'z oldida parcha-parcha ko'rinsa"],
        "dori": "Shifokor ko'rigisiz dori ishlating"
    },

    # ═══════════════════ QULOQ ═══════════════════
    "quloq og'riq": {
        "name": "Quloq og'rig'i",
        "ehtimol": ["Otit", "Quloq tiqilishi", "ARVI asoratlari"],
        "shifokor": "LOR",
        "uyda": "Quloqqa issiq qo'ying (agar teshik bo'lmasa), og'riq qoldiruvchi iching",
        "xavfli": ["Isitma bilan quloq og'risa", "Quloqdan yiring chiqsa", "Eshitish kamaysa"],
        "dori": "Otipax tomizg'i, Paracetamol — shifokor ko'rigisiz boshqa dori ichmang"
    },
    "quloq bitishi": {
        "name": "Quloq bitishi",
        "ehtimol": ["Quloq plug'i", "ARVI", "Otit"],
        "shifokor": "LOR",
        "uyda": "Aqualor quloq uchun yoki iliq suv bilan quloq yuvish",
        "xavfli": ["Og'riq bilan birga bo'lsa", "Yiring chiqsa"],
        "dori": "A-cerumen (quloq tomizg'i)"
    },

    # ═══════════════════ ASAB TIZIMI ═══════════════════
    "uyqu buzilishi": {
        "name": "Uyqu buzilishi (Bezsonnitsa)",
        "ehtimol": ["Stress", "Depressiya", "Qalqonsimon bez", "Kofein ko'p ichish"],
        "shifokor": "Nevropatolog yoki Psixiatr",
        "uyda": "Bir vaqtda yoting, ekrandan saqlaning, iliq hammom, limon balzami choy",
        "xavfli": ["1 oydan ko'p davom etsa shifokorga boring"],
        "dori": "Melatonin 3mg, Valerian — shifokor tavsiyasi bilan"
    },
    "stress": {
        "name": "Stress va asabiylik",
        "ehtimol": ["Stress", "Nerv tizimi charchashi", "Trevoga buzilishi"],
        "shifokor": "Psixolog yoki Nevropatolog",
        "uyda": "Nafas mashqlari, yurish, sport, meditatsiya, dam olish",
        "xavfli": ["O'ziga zarar berish fikri bo'lsa — darhol yordam so'rang!"],
        "dori": "Valerian, Novopassit — shifokor tavsiyasi bilan"
    },
    "epilepsiya": {
        "name": "Epileptik tutqanoq (shubhali)",
        "ehtimol": ["Epilepsiya"],
        "shifokor": "Nevropatolog — TEZDA!",
        "uyda": "Bemorni yonga yotqizing, boshini ushlab turing, og'ziga hech narsa soling",
        "xavfli": ["5 daqiqadan ko'p davom etsa — 103!"],
        "dori": "Shifokor ko'rigisiz dori ichmang!"
    },
    "hushdan ketish": {
        "name": "Hushdan ketish (Obmoroki)",
        "ehtimol": ["Qon bosimi pastligi", "Qon kamayishi", "Yurak muammosi", "Issiqlik urishi"],
        "shifokor": "Terapevt yoki Kardiolog",
        "uyda": "Gorizontal yotqizing, oyoqlarni ko'taring, havo bering",
        "xavfli": ["Tez-tez takrorlansa", "Ko'krak og'rig'i bilan", "Uzoq hushsiz qolsa — 103!"],
        "dori": "Ammiak (hidlating)"
    },
    "qo'l-oyoq uvishishi": {
        "name": "Qo'l-oyoq uvishishi",
        "ehtimol": ["Osteoxondroz", "Qon aylanishi buzilishi", "Diabet", "Nevrit"],
        "shifokor": "Nevropatolog",
        "uyda": "Massaj qiling, harakat qiling, noto'g'ri o'tirishdan saqlaning",
        "xavfli": ["Bir tomonda to'satdan uvishsa — insult bo'lishi mumkin — 103!"],
        "dori": "B vitamini, Milgamma — shifokor tavsiyasi bilan"
    },
    "insult belgilari": {
        "name": "Insult belgilari",
        "ehtimol": ["Insult (Insult)"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "Bemorni yotqizing, bosh baland, hech narsa ichmang",
        "xavfli": ["Bir tomonda zaiflik", "Nutq buzilishi", "Og'iz qiyshayishi — BU INSULT!"],
        "dori": "HECH NARSA ICHMANG — tez yordam chaqiring!"
    },

    # ═══════════════════ ENDOKRIN ═══════════════════
    "qandli diabet": {
        "name": "Qandli diabet belgilari",
        "ehtimol": ["Diabet 1-tur", "Diabet 2-tur", "Prediabet"],
        "shifokor": "Endokrinolog",
        "uyda": "Shakar kamroq iste'mol qiling, harakat qiling, vazn nazorat qiling",
        "xavfli": ["Qon qandi juda past (gipoglikemiya) — tez shirinlik iching!", "Hushdan ketsa — 103!"],
        "dori": "Insulin yoki tabletkalar — FAQAT shifokor tavsiyasi bilan"
    },
    "qalqonsimon bez": {
        "name": "Qalqonsimon bez muammosi",
        "ehtimol": ["Gipotireoz", "Gipertireoz", "Zob"],
        "shifokor": "Endokrinolog",
        "uyda": "Yod bilan mahsulot iste'mol qiling, stressdan saqlaning",
        "xavfli": ["Bo'yin shishsa", "Yurak tez ursa + ko'z chiqib ketsa"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "semizlik": {
        "name": "Ortiqcha vazn / Semizlik",
        "ehtimol": ["Alimentar semizlik", "Gormonal buzilish", "Diabet"],
        "shifokor": "Endokrinolog yoki Terapevt",
        "uyda": "Kaloriyani kamaytiring, sport qiling, ko'p suv iching",
        "xavfli": ["Nafas qiynalsa", "Ko'krak og'risa", "Oyoq shishsa"],
        "dori": "Shifokor ko'rigisiz oziqtiruvchi dori ichmang!"
    },

    # ═══════════════════ QONNING ═══════════════════
    "kamqonlik": {
        "name": "Kamqonlik (Anemiya)",
        "ehtimol": ["Temir yetishmovchiligi anemiyasi", "B12 yetishmovchiligi", "Qon yo'qotish"],
        "shifokor": "Terapevt yoki Gematolog",
        "uyda": "Temir boy ovqat (jigar, grenade, olmа), dam oling",
        "xavfli": ["Hushdan ketsangiz", "Yurak tez ursa", "Nafas qiynalsa"],
        "dori": "Ferrum Lek, Sorbifer — shifokor tavsiyasi bilan"
    },

    # ═══════════════════ ALLERGIYA ═══════════════════
    "allergiya": {
        "name": "Allergiya",
        "ehtimol": ["Oziq-ovqat allergiyasi", "Gard allergiyasi", "Teri allergiyasi"],
        "shifokor": "Allergolog",
        "uyda": "Allergendan uzoqlashing, antihistaminik iching",
        "xavfli": ["Nafas qiynalsa — 103! (anafilaksiya)", "Yuz shishsa", "Tomoq shishsa"],
        "dori": "Loratadin, Suprastin, Cetrizin"
    },
    "anafilaksiya": {
        "name": "Anafilaktik shok",
        "ehtimol": ["Og'ir allergik reaktsiya"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "Adrenaliní yubing (agar bo'lsa), yotqizing, oyoqlarni ko'taring",
        "xavfli": ["BU HAYOTga XAVFLI — DARHOL 103!"],
        "dori": "Adrenalin — tez yordam kelguncha"
    },

    # ═══════════════════ AYOLLAR SOGLIGI ═══════════════════
    "hayz og'riq": {
        "name": "Hayz og'rig'i (Dismenorea)",
        "ehtimol": ["Birlamchi dismenorea", "Endometrioz", "Mioma"],
        "shifokor": "Ginekolog",
        "uyda": "Issiq yostiq qorin pastiga, dam oling, No-shpa",
        "xavfli": ["Juda kuchli og'riq", "Ko'p qon ketsa", "Isitma bilan og'riq"],
        "dori": "Ibuprofen 400mg, No-shpa"
    },
    "hayz kechikishi": {
        "name": "Hayz kechikishi",
        "ehtimol": ["Homiladorlik", "Stress", "Gormonal buzilish", "PKOY"],
        "shifokor": "Ginekolog",
        "uyda": "Homiladorlik testini qiling",
        "xavfli": ["3 oydan ko'p kechiksa shifokorga boring"],
        "dori": "Shifokor ko'rigisiz gormonal dori ichmang!"
    },
    "ko'krak og'riq ayol": {
        "name": "Ko'krak bezi og'rig'i",
        "ehtimol": ["Mastodinia", "Mastit", "Ko'krak bezi tuzilishi"],
        "shifokor": "Mammolog yoki Ginekolog",
        "uyda": "Qo'llab-quvvatlash simsiz kiyim kiyish",
        "xavfli": ["Tugma sezilsa", "Qizarish + isitma bilan (mastit)", "Nipledan ajralma chiqsa"],
        "dori": "Shifokor ko'rigisiz dori ichmang!"
    },

    # ═══════════════════ ERKAKLAR SOGLIGI ═══════════════════
    "prostata": {
        "name": "Prostata muammosi",
        "ehtimol": ["Prostata adenomasi", "Prostatit"],
        "shifokor": "Urolog",
        "uyda": "Ko'p suv iching, sovuqdan saqlaning, spirtdan saqlaning",
        "xavfli": ["Siydik umuman bo'lmasa — 103!", "Isitma + bel og'riq"],
        "dori": "Shifokor ko'rigisiz dori ichmang!"
    },

    # ═══════════════════ BOLALAR ═══════════════════
    "bola isitmasi": {
        "name": "Bola isitmasi",
        "ehtimol": ["ARVI", "Tish chiqishi", "Quloq yallig'lanishi"],
        "shifokor": "Pediatr",
        "uyda": "Ko'p suv bering, kiyimini yechib artib qo'ying",
        "xavfli": ["38.5 dan yuqori bo'lsa dori bering", "Tortishish bo'lsa — 103!", "3 oydan kichik bolada har qanday isitma — 103!"],
        "dori": "Paracetamol (bolalar uchun), Nurofen — yoshga qarab"
    },
    "bola yo'tali": {
        "name": "Bola yo'tali",
        "ehtimol": ["ARVI", "Bronxit", "Pertussis (ko'k yo'tal)"],
        "shifokor": "Pediatr",
        "uyda": "Ko'p suv bering, havo namlantirilgan bo'lsin, ko'krak qafasini massaj qiling",
        "xavfli": ["Nafas qiynalsa", "Lablar ko'karsa — 103!", "Isitma yuqori bo'lsa"],
        "dori": "Lazolvan bolalar uchun — shifokor tavsiyasi bilan"
    },

    # ═══════════════════ RUHIY SOGLIQ ═══════════════════
    "depressiya": {
        "name": "Depressiya belgilari",
        "ehtimol": ["Klinik depressiya", "Reaktiv depressiya", "Gipotireoz"],
        "shifokor": "Psixiatr yoki Psixolog",
        "uyda": "Sport, yorug'lik, aloqa, rejim, psixolog bilan suhbat",
        "xavfli": ["O'ziga zarar berish fikri bo'lsa — DARHOL yordam so'rang! 182 (ishonch telefoni)"],
        "dori": "Antidepressantlar FAQAT psixiatr tavsiyasi bilan"
    },
    "trevoga": {
        "name": "Trevoga (Qo'rquv hissi)",
        "ehtimol": ["Trevoga buzilishi", "Panik ataka", "Stress"],
        "shifokor": "Psixolog yoki Psixiatr",
        "uyda": "Nafas mashqlari (4-7-8 usuli), meditatsiya, sport",
        "xavfli": ["Panik ataka chastotasi oshsa", "Uydan chiqa olmasangiz"],
        "dori": "Valerian, Afobazol — shifokor tavsiyasi bilan"
    },
    "panik ataka": {
        "name": "Panik ataka",
        "ehtimol": ["Panik buzilish"],
        "shifokor": "Psixiatr yoki Psixolog",
        "uyda": "Chuqur nafas oling (burundan 4 hisob — ushlab 4 hisob — og'izdan 8 hisob), o'tirib oling",
        "xavfli": ["Har kuni bo'lsa shifokorga boring"],
        "dori": "Shifokor ko'rigisiz dori ichmang!"
    },

    # ═══════════════════ TISH ═══════════════════
    "tish og'riq": {
        "name": "Tish og'rig'i",
        "ehtimol": ["Karies", "Pulpit", "Periodontit", "Doniqlik"],
        "shifokor": "Stomatolog",
        "uyda": "Tuzli suv bilan chayish, sovuq/issiq ovqatdan saqlaning",
        "xavfli": ["Yuz shishsa", "Isitma bilan og'riq", "Yutuv qiyin bo'lsa"],
        "dori": "Ibuprofen 400mg (vaqtincha), Ketanov — tezda stomatologga boring"
    },
    "tish milki qon ketishi": {
        "name": "Tish milki qon ketishi",
        "ehtimol": ["Gingivit", "Parodontit", "Vitamin yetishmovchiligi"],
        "shifokor": "Stomatolog",
        "uyda": "Yumshoq cho'tka ishlating, tuzli suv bilan chayish",
        "xavfli": ["Ko'p qon ketsa", "Tishlar sallanca bo'lsa"],
        "dori": "Xolisal gel, Metrogil denta"
    },

    # ═══════════════════ TRAVMA ═══════════════════
    "kuyish": {
        "name": "Kuyish",
        "ehtimol": ["1-daraja kuyish", "2-daraja kuyish", "3-daraja kuyish"],
        "shifokor": "Jarroh yoki Travmatolog",
        "uyda": "Sovuq suv ostida 10-20 daqiqa ushlab turing, muz qo'ymang, moy qo'ymang!",
        "xavfli": ["Katta joy kuysa — 103!", "Yuz, qo'l, jinsiy organlar kuysa", "3-daraja kuyish"],
        "dori": "Panthenol spray, steril bog'lam"
    },
    "jarohat": {
        "name": "Jarohat (Pora yara)",
        "ehtimol": ["Kesik", "Tirnalish", "Ezilish"],
        "shifokor": "Jarroh (chuqur yaralar uchun)",
        "uyda": "Qon to'xtatish (bosib turing), yuvish, zararsizlantirish, bog'lash",
        "xavfli": ["Qon to'xtamasa — 103!", "Chuqur kesik — tikish kerak", "Ifloslangan yara"],
        "dori": "Vodorodni peroksid, Betadin, Levomekol"
    },
    "chiqish": {
        "name": "Chiqish (Vıvıx)",
        "ehtimol": ["Bo'g'im chiqishi"],
        "shifokor": "Travmatolog — TEZDA!",
        "uyda": "Harakatlantirmang, muzlatib qo'ying, shifokorga boring",
        "xavfli": ["O'zingiz joyiga qaytarmang — zarar yetkazilishi mumkin!"],
        "dori": "Ibuprofen og'riq uchun"
    },
    "chayilish": {
        "name": "Bo'g'im chayilishi (Rastyazhenie)",
        "ehtimol": ["Ligament chayilishi", "Yirtilishi"],
        "shifokor": "Travmatolog",
        "uyda": "R.I.C.E: Dam oling, Muz, Compress, Oyoqni ko'taring",
        "xavfli": ["Shishish juda katta bo'lsa", "Yura olmasangiz — rentgen kerak"],
        "dori": "Ibuprofen, Voltaren gel, elastik bandaj"
    },
    "issiqlik urishi": {
        "name": "Issiqlik / Quyosh urishi",
        "ehtimol": ["Issiqlik urishi", "Quyosh urishi"],
        "shifokor": "Terapevt yoki Tez yordam",
        "uyda": "Salqin joyga olib kiring, kiyimini yechib artib qo'ying, sovuq suv bering",
        "xavfli": ["Hushdan ketsangiz — 103!", "Isitma 40 dan yuqori — 103!"],
        "dori": "Sovuq suv, Regidron"
    },

    # ═══════════════════ YUQUMLI KASALLIKLAR ═══════════════════
    "covid": {
        "name": "COVID-19 belgilari",
        "ehtimol": ["COVID-19", "ARVI", "Gripp"],
        "shifokor": "Terapevt",
        "uyda": "Izolyatsiya, ko'p suv, vitaminlar, harorat nazorati",
        "xavfli": ["Nafas qiynalsa — 103!", "Kislorod kamaysa", "Isitma 39 dan yuqori"],
        "dori": "Paracetamol, Vitaminlar — shifokor tavsiyasi bilan"
    },
    "ich terlashi": {
        "name": "Ko'p terlash",
        "ehtimol": ["Gipergiddroz", "Qalqonsimon bez", "Diabet", "Isitma"],
        "shifokor": "Terapevt yoki Endokrinolog",
        "uyda": "Paxta kiyim kiyining, terini quruq ushlab turing",
        "xavfli": ["Tunda ko'p terlash + vazn yo'qotish = shifokorga boring!"],
        "dori": "Dezodorant antiperspirant"
    },
    "charchoq": {
        "name": "Doimiy charchoq",
        "ehtimol": ["Surunkali charchoq sindromi", "Kamqonlik", "Diabet", "Gipotireoz", "Depressiya"],
        "shifokor": "Terapevt",
        "uyda": "Uyqu rejimi, sport, to'g'ri ovqatlanish, vitaminlar",
        "xavfli": ["Vazn yo'qotish bilan charchoq", "Isitma bilan charchoq"],
        "dori": "Vitaminlar (B12, D), Temir — tahlildan keyin"
    },
    "vazn yo'qotish": {
        "name": "Tushunarsiz vazn yo'qotish",
        "ehtimol": ["Diabet", "Qalqonsimon bez", "Onkologiya", "Depressiya"],
        "shifokor": "Terapevt — TEZDA tahlil toping!",
        "uyda": "Ko'p kaloriyali ovqat yeng",
        "xavfli": ["1 oyda 5 kg dan ko'p yo'qotilsa — shifokorga!"],
        "dori": "Shifokor ko'rigisiz dori ichmang!"
    },

    # ═══════════════════ QOSHIMCHA ═══════════════════
    "tez charchash": {
        "name": "Tez charchash",
        "ehtimol": ["Kamqonlik", "Vitaminlar yetishmovchiligi", "Qalqonsimon bez", "Yurak"],
        "shifokor": "Terapevt",
        "uyda": "Ko'proq dam oling, to'g'ri ovqatlaning, vitaminlar iching",
        "xavfli": ["Nafas bilan charchoq", "Ko'krak og'riq bilan"],
        "dori": "Vitaminlar B, C, D, Temir"
    },
    "ishtaha yo'qligi": {
        "name": "Ishtaha yo'qligi",
        "ehtimol": ["Gastrit", "Depressiya", "Onkologiya", "Infektsiya"],
        "shifokor": "Terapevt",
        "uyda": "Kichik porsiyada yeng, mazali ovqat pishiring",
        "xavfli": ["Vazn yo'qotish bilan ishtaha yo'qligi — tezda shifokorga!"],
        "dori": "Shifokor ko'rigisiz dori ichmang!"
    },
    "og'iz yomon hid": {
        "name": "Og'izdan yomon hid (Galitoz)",
        "ehtimol": ["Tish muammolari", "Oshqozon kasalligi", "Tomoq kasalligi"],
        "shifokor": "Stomatolog yoki Gastroenterolog",
        "uyda": "Tishlarni to'g'ri tozalang, til tozalang, ko'p suv iching",
        "xavfli": ["Keskin o'zgarsa (diabet, jigar muammosi)"],
        "dori": "Listerin og'iz yuvish vositasi"
    },
    "tana harorati past": {
        "name": "Tana harorati past (35 dan past)",
        "ehtimol": ["Gipotermiya", "Gipotireoz", "Qon bosimi pastligi"],
        "shifokor": "Terapevt",
        "uyda": "Iliq kiyim, issiq ichimlik, harakat qiling",
        "xavfli": ["34 dan past — 103!", "Hushsiz bo'lsa"],
        "dori": "Issiq choy, harakatlanish"
    },
    "oyoq kramp": {
        "name": "Oyoq mushaklari kramp",
        "ehtimol": ["Magniy yetishmovchiligi", "Qon aylanishi buzilishi", "Charchoq"],
        "shifokor": "Terapevt yoki Nevropatolog",
        "uyda": "Oyoqni cho'zing, massaj qiling, issiq hammom",
        "xavfli": ["Har kecha takrorlansa", "Kun davomida ham bo'lsa"],
        "dori": "Magniy B6, Asparkam"
    },
    "burnidan qon ketish": {
        "name": "Burnidan qon ketish",
        "ehtimol": ["Qon tomir mo'rtligi", "Qon bosimi yuqori", "Quruq havo"],
        "shifokor": "LOR yoki Terapevt",
        "uyda": "Boshni oldinga eging (orqaga emas!), burunni 10 daqiqa qisilgan ushlab turing",
        "xavfli": ["To'xtamasa — 103!", "Qon bosimi yuqori bo'lsa"],
        "dori": "Vodorodni peroksid — paxta bilan"
    },
}

# ═══════════════════ QOSHIMCHA 111 TA ═══════════════════
DISEASES_DB.update({
    "gemorroy": {
        "name": "Gemorroy",
        "ehtimol": ["Ichki gemorroy", "Tashqi gemorroy"],
        "shifokor": "Proktolog yoki Jarroh",
        "uyda": "Ko'p suv iching, tolali ovqat yeng, uzoq o'tirmaslik",
        "xavfli": ["Kuchli qon ketsa", "Kuchli og'riq bilan shish"],
        "dori": "Relif, Proktozan — shifokor tavsiyasi bilan"
    },
    "varikoz": {
        "name": "Varikoz (Kengaygan venalar)",
        "ehtimol": ["Oyoq venalari varikozi"],
        "shifokor": "Flebolог yoki Jarroh",
        "uyda": "Oyoqlarni ko'taring, kompressiya paypoq kiyish, ko'p yuring",
        "xavfli": ["Vena qizarsa + og'risa (tromboflebit)", "Yara paydo bo'lsa"],
        "dori": "Troxevazin gel, Detralex — shifokor tavsiyasi bilan"
    },
    "tromboz": {
        "name": "Tromboz (shubhali)",
        "ehtimol": ["Venoz tromboz", "O'pka tromboemboliyasi"],
        "shifokor": "DARHOL shifokorga! — 103",
        "uyda": "Oyoqni harakatlantirmang",
        "xavfli": ["Nafas qiynalsa + oyoq og'risa — BU XAVFLI — 103!"],
        "dori": "Hech narsa ichmang — tez yordam!"
    },
    "podagra": {
        "name": "Podagra",
        "ehtimol": ["Podagra (siydik kislota ortiqcha)"],
        "shifokor": "Revmatolog",
        "uyda": "Ko'p suv iching, go'sht-baliq kamaytiring, alkogoldan saqlaning",
        "xavfli": ["Isitma bilan bo'g'im og'risa"],
        "dori": "Ibuprofen, Colchicine — shifokor tavsiyasi bilan"
    },
    "revmatizm": {
        "name": "Revmatizm",
        "ehtimol": ["Revmatoid artrit", "Revmatizm"],
        "shifokor": "Revmatolog",
        "uyda": "Dam oling, issiq kompres, stressdan saqlaning",
        "xavfli": ["Ko'p bo'g'im og'risa + isitma + yurak og'risa"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "osteoporoz": {
        "name": "Osteoporoz (suyak mo'rtligi)",
        "ehtimol": ["Osteoporoz"],
        "shifokor": "Ortoped yoki Endokrinolog",
        "uyda": "Sut mahsulotlari, D vitamini, ehtiyot bo'lish",
        "xavfli": ["Yiqilganda suyak sinsa"],
        "dori": "Kaltsiy + D vitamini — shifokor tavsiyasi bilan"
    },
    "pankreatit": {
        "name": "Pankreatit (oshqozon osti bezi)",
        "ehtimol": ["O'tkir pankreatit", "Surunkali pankreatit"],
        "shifokor": "Gastroenterolog — TEZDA!",
        "uyda": "Ovqat yemang (1-2 kun), faqat suv, dam oling",
        "xavfli": ["Kuchli qorin og'rig'i — 103!", "Qayt + isitma bilan"],
        "dori": "No-shpa, Omeprazol — lekin shifokor ko'rigisiz davo qilmang"
    },
    "gepatit": {
        "name": "Gepatit",
        "ehtimol": ["Gepatit A", "Gepatit B", "Gepatit C"],
        "shifokor": "Infektsionist yoki Gepatolog",
        "uyda": "Dam oling, yog'li ovqatdan saqlaning, alkogoldan saqlaning",
        "xavfli": ["Ko'z sariqsa", "Qorin o'ng yuqorisida og'riq"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "sirroz": {
        "name": "Jigar sirozi",
        "ehtimol": ["Jigar sirozi"],
        "shifokor": "Gastroenterolog yoki Gepatolog",
        "uyda": "Alkogolsiz, yog'lisiz ovqatlanish, dam olish",
        "xavfli": ["Qorin kattalashsa", "Qon qusish"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "pielonefrit": {
        "name": "Pielonefrit (buyrak infektsiyasi)",
        "ehtimol": ["O'tkir pielonefrit"],
        "shifokor": "Urolog yoki Nefrologik",
        "uyda": "Ko'p suv iching, iliq bo'ling",
        "xavfli": ["Isitma + bel og'riq + siydik yomonlashsa"],
        "dori": "Antibiotik — FAQAT shifokor tavsiyasi bilan"
    },
    "buyrak toshi": {
        "name": "Buyrak toshi (Mochekamennaya)",
        "ehtimol": ["Urat toshlar", "Oksalat toshlar"],
        "shifokor": "Urolog",
        "uyda": "Ko'p suv iching (2-3 litr), harakat qiling",
        "xavfli": ["Kuchli kolik og'riq — tez yordam!", "Qon bilan siydik"],
        "dori": "No-shpa (spazm), Ko'p suv"
    },
    "uretra yallig'lanish": {
        "name": "Uretra yallig'lanishi (Uretrit)",
        "ehtimol": ["Bakterial uretrit", "JKST infektsiyasi"],
        "shifokor": "Urolog",
        "uyda": "Ko'p suv iching, sovuqdan saqlaning",
        "xavfli": ["Yiring bilan siydik", "Isitma bilan"],
        "dori": "Antibiotik — FAQAT shifokor tavsiyasi bilan"
    },
    "endometrioz": {
        "name": "Endometrioz",
        "ehtimol": ["Endometrioz"],
        "shifokor": "Ginekolog",
        "uyda": "Issiq (hayz vaqtida), dam oling",
        "xavfli": ["Juda kuchli og'riq", "Homilador bo'lolmaslik"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "tuxumdon kistasi": {
        "name": "Tuxumdon kistasi (shubhali)",
        "ehtimol": ["Funksional kista", "Endometrioid kista"],
        "shifokor": "Ginekolog",
        "uyda": "Og'ir ko'tarmang, stress kamroq",
        "xavfli": ["Kuchli to'satdan og'riq — kista yorilib ketishi mumkin — 103!"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "mioma": {
        "name": "Bachadon miomasi",
        "ehtimol": ["Bachadon miomasi"],
        "shifokor": "Ginekolog",
        "uyda": "Muntazam tekshiruv",
        "xavfli": ["Ko'p qon ketsa", "Qorin kattalashsa"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "vaginit": {
        "name": "Vaginit (qin yallig'lanishi)",
        "ehtimol": ["Bakterial vaginoz", "Kandidoz", "Trixomoniaz"],
        "shifokor": "Ginekolog",
        "uyda": "Gigiena saqlang, paxta ichki kiyim, sovunli yuvishdan saqlaning",
        "xavfli": ["Isitma bilan ajralma", "Qorin og'riq bilan"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "impotentsiya": {
        "name": "Jinsiy zaiflik (Erkaklar)",
        "ehtimol": ["Psixogen", "Gormonal", "Qon tomir", "Diabet"],
        "shifokor": "Androlog yoki Urolog",
        "uyda": "Sport, to'g'ri ovqat, stressdan saqlaning, sigaret qoldiring",
        "xavfli": ["Diabet + jinsiy zaiflik — endokrinologga boring"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "spermatozoid muammosi": {
        "name": "Erkak bepushtligi",
        "ehtimol": ["Oligospermiya", "Varikotsele", "Gormonal"],
        "shifokor": "Androlog",
        "uyda": "Issiqdan saqlaning, alkogol yo'q, sport",
        "xavfli": ["Ko'rinis yo'q, lekin tahlil kerak"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "qizilcha": {
        "name": "Qizilcha (Krasnukha)",
        "ehtimol": ["Qizilcha virusi"],
        "shifokor": "Infektsionist",
        "uyda": "Izolyatsiya, dam olish, ko'p suv",
        "xavfli": ["Homilador ayollarda — DARHOL shifokorga!"],
        "dori": "Paracetamol, ko'p suv"
    },
    "suv chechak": {
        "name": "Suv chechak (Vetryanka)",
        "ehtimol": ["Varicella-zoster virus"],
        "shifokor": "Infektsionist",
        "uyda": "Izolyatsiya, qashimang, Zelenka sur'ing",
        "xavfli": ["Kattalar uchun og'irroq — shifokorga boring", "Nafas qiynalsa"],
        "dori": "Calamine lotion, Paracetamol, Acyclovir — shifokor tavsiyasi"
    },
    "qoqim": {
        "name": "Qoqim (Koklush)",
        "ehtimol": ["Bordetella pertussis"],
        "shifokor": "Infektsionist — TEZDA!",
        "uyda": "Izolyatsiya, havo yangilash",
        "xavfli": ["Bolalarda — JUDA XAVFLI — 103!"],
        "dori": "Antibiotik — faqat shifokor tavsiyasi bilan"
    },
    "qizamiq": {
        "name": "Qizamiq (Kor')",
        "ehtimol": ["Qizamiq virusi"],
        "shifokor": "Infektsionist",
        "uyda": "Izolyatsiya, yorug'likdan ko'z saqlash, ko'p suv",
        "xavfli": ["Pnevmoniya asorati bo'lishi mumkin"],
        "dori": "Paracetamol, Vitaminlar"
    },
    "brutselloz": {
        "name": "Brutselloz",
        "ehtimol": ["Brucella bakteriyasi"],
        "shifokor": "Infektsionist",
        "uyda": "Dam oling",
        "xavfli": ["Doimiy isitma + bo'g'im og'riq + terlash"],
        "dori": "Antibiotik — FAQAT shifokor tavsiyasi bilan"
    },
    "sil kasalligi": {
        "name": "Sil kasalligi (Tuberkulez) shubhasi",
        "ehtimol": ["O'pka sili"],
        "shifokor": "Ftiziatr — TEZDA!",
        "uyda": "Izolyatsiya, dam oling",
        "xavfli": ["3 haftadan ko'p yo'tal + vazn yo'qotish + terlash — shifokorga!"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "zaxm": {
        "name": "Zaxm (Sifilis) shubhasi",
        "ehtimol": ["Treponema pallidum"],
        "shifokor": "Dermatovenerolog — TEZDA!",
        "uyda": "Jinsiy aloqadan saqlaning",
        "xavfli": ["Davolanmasa og'ir asoratlar"],
        "dori": "Penitsillin — FAQAT shifokor tavsiyasi bilan"
    },
    "gonoreya": {
        "name": "Gonoreya shubhasi",
        "ehtimol": ["Neisseria gonorrhoeae"],
        "shifokor": "Dermatovenerolog",
        "uyda": "Jinsiy aloqadan saqlaning",
        "xavfli": ["Davolanmasa bepushtlik"],
        "dori": "Antibiotik — FAQAT shifokor tavsiyasi bilan"
    },
    "dizenteriya": {
        "name": "Dizenteriya",
        "ehtimol": ["Shigella bakteriyasi"],
        "shifokor": "Infektsionist",
        "uyda": "Ko'p suv, Regidron, izolyatsiya",
        "xavfli": ["Qon bilan najas", "Bolalarda suvsizlik — 103!"],
        "dori": "Nifuroxazid, Regidron — shifokor tavsiyasi bilan"
    },
    "gijja": {
        "name": "Gijja (Parazitlar)",
        "ehtimol": ["Askaridoz", "Enterobioz", "Lyamblioz"],
        "shifokor": "Infektsionist yoki Terapevt",
        "uyda": "Gigiena saqlang, qo'llarni yuvish",
        "xavfli": ["Bolalarda qorin og'riq + ishtaha yo'qligi"],
        "dori": "Pyrantel, Mebendazol — shifokor tavsiyasi bilan"
    },
    "lyamblioz": {
        "name": "Lyamblioz",
        "ehtimol": ["Giardia lamblia"],
        "shifokor": "Infektsionist",
        "uyda": "Gigiena, suv qaynatib ichish",
        "xavfli": ["Uzoq ich ketish + vazn yo'qotish"],
        "dori": "Metronidazol — shifokor tavsiyasi bilan"
    },
    "toksoplazmoz": {
        "name": "Toksoplazmoz",
        "ehtimol": ["Toxoplasma gondii"],
        "shifokor": "Infektsionist",
        "uyda": "Mushuklardan uzoqroq, xom go'sht emang",
        "xavfli": ["Homiladorlarda — DARHOL shifokorga!"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "ekzema": {
        "name": "Ekzema",
        "ehtimol": ["Atopik ekzema", "Kontakt dermatit"],
        "shifokor": "Dermatolog",
        "uyda": "Nam saqlash, allergendan saqlaning, qashimang",
        "xavfli": ["Yiringlasa", "Katta joy qoplasa"],
        "dori": "Moisturizer, Hydrocortisone krem — shifokor tavsiyasi bilan"
    },
    "psoriaz": {
        "name": "Psoriaz",
        "ehtimol": ["Psoriaz"],
        "shifokor": "Dermatolog",
        "uyda": "Teri namligini saqlang, stress kamaytiring, quyosh (oz miqdorda)",
        "xavfli": ["Bo'g'imlarga tarqalsa (psoriaz artrit)"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "rozatsea": {
        "name": "Rozatsea (yuz qizarishi)",
        "ehtimol": ["Rozatsea"],
        "shifokor": "Dermatolog",
        "uyda": "Quyoshdan saqlaning, achchiq ovqat kamaytiring, alkogolsiz",
        "xavfli": ["Ko'z zararlansa (okular rozatsea)"],
        "dori": "Metronidazol gel — shifokor tavsiyasi bilan"
    },
    "vitiligo": {
        "name": "Vitiligo",
        "ehtimol": ["Vitiligo (autoimmun)"],
        "shifokor": "Dermatolog",
        "uyda": "Quyoshdan saqlaning",
        "xavfli": ["Asosan estetik muammo, lekin autoimmun tekshiruv kerak"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "furunkulez": {
        "name": "Chivin (Furunkulez)",
        "ehtimol": ["Stafilokokk infektsiyasi"],
        "shifokor": "Jarroh yoki Dermatolog",
        "uyda": "Issiq kompres, siqmang!",
        "xavfli": ["Yuzda furunkel — SIQMANG, xavfli!", "Isitma bilan"],
        "dori": "Levomekol, Ichishiga antibiotik — faqat shifokor"
    },
    "gipertiroidizm": {
        "name": "Gipertiroidizm (qalqonsimon bez faolligi ortishi)",
        "ehtimol": ["Graves kasalligi", "Toksik zob"],
        "shifokor": "Endokrinolog",
        "uyda": "Stressdan saqlaning, dam oling",
        "xavfli": ["Yurak tez urishi + ko'z chiqishi + vazn yo'qotish"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "gipotiroidizm": {
        "name": "Gipotiroidizm (qalqonsimon bez yetishmovchiligi)",
        "ehtimol": ["Hashimoto tiroiditi"],
        "shifokor": "Endokrinolog",
        "uyda": "Yod bilan mahsulotlar iste'mol qiling",
        "xavfli": ["Charchoq + vazn ortishi + sovuq sezish + depressiya"],
        "dori": "L-tiroksin — FAQAT shifokor tavsiyasi bilan"
    },
    "addison kasalligi": {
        "name": "Buyrak usti bezi yetishmovchiligi",
        "ehtimol": ["Addison kasalligi"],
        "shifokor": "Endokrinolog — TEZDA!",
        "uyda": "Tuz ko'proq iste'mol qiling, stressdan saqlaning",
        "xavfli": ["To'satdan zaiflik + qorin og'riq + past bosim — 103!"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "kushinga sindromi": {
        "name": "Kushing sindromi",
        "ehtimol": ["Giperkortitsizm"],
        "shifokor": "Endokrinolog",
        "uyda": "Shifokor kuzatuvi muhim",
        "xavfli": ["Yuz dumaloqlashishi + qorin semizligi + qon bosimi + qand"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "miokard infarkti": {
        "name": "Miokard infarkti (yurak tutishi)",
        "ehtimol": ["O'tkir miokard infarkti"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "Yotqizing, kiyimni bo'shating, Aspirin 325mg bering, 103 chaqiring",
        "xavfli": ["Ko'krak g'ishtday bosishi + chap qo'lga tarqalishi = INFARKT — 103!"],
        "dori": "Aspirin 325mg — tez yordam kelguncha"
    },
    "stenokardiya": {
        "name": "Stenokardiya (Stend og'rig'i)",
        "ehtimol": ["Barqaror stenokardiya", "Nobarqaror stenokardiya"],
        "shifokor": "Kardiolog",
        "uyda": "Dam oling, Nitroglitserin (shifokor tavsiyasi bo'lsa)",
        "xavfli": ["Nitroglitserin yordam bermasa — 103!", "Birinchi marta bo'lsa — tezda shifokor"],
        "dori": "Nitroglitserin — FAQAT shifokor tavsiyasi bilan"
    },
    "aritmiya": {
        "name": "Yurak aritmiyasi",
        "ehtimol": ["Fibrillyatsiya", "Ekstrasistoliya", "Blokada"],
        "shifokor": "Kardiolog",
        "uyda": "Tinch o'tiring, chuqur nafas oling, kofeindan saqlaning",
        "xavfli": ["Hushdan ketsangiz — 103!", "Ko'krak og'rig'i bilan aritmiya"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "yurak yetishmovchiligi": {
        "name": "Yurak yetishmovchiligi",
        "ehtimol": ["Surunkali yurak yetishmovchiligi"],
        "shifokor": "Kardiolog",
        "uyda": "Tuz kamaytiring, suyuqlik nazorat qiling, og'ir ish qilmang",
        "xavfli": ["Nafas qiynalsa yotganda", "Oyoq juda shishsa — tezda shifokor"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "perikardít": {
        "name": "Perikardít (yurak parda yallig'lanishi)",
        "ehtimol": ["Viral perikardít"],
        "shifokor": "Kardiolog — TEZDA!",
        "uyda": "Dam oling",
        "xavfli": ["Ko'krak og'rig'i + isitma + nafas qiynalsa"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "o'pka emboliyasi": {
        "name": "O'pka emboliyasi (shubhali)",
        "ehtimol": ["O'pka tromboemboliyasi"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "Tik o'tiring, deraza oching, 103 chaqiring",
        "xavfli": ["To'satdan nafas qiynalish + ko'krak og'rig'i + oyoq og'rig'i — 103!"],
        "dori": "HECH NARSA ICHMANG — tez yordam!"
    },
    "aorta anevrizmasi": {
        "name": "Aorta anevrizmasi (shubhali)",
        "ehtimol": ["Aorta anevrizmasi"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "Yotqizing, 103 chaqiring",
        "xavfli": ["Qorin/bel/ko'krakda portlovchi og'riq — 103!"],
        "dori": "HECH NARSA ICHMANG — tez yordam!"
    },
    "diabet 1": {
        "name": "Diabet 1-tur",
        "ehtimol": ["Insulin-baquvvat diabet"],
        "shifokor": "Endokrinolog",
        "uyda": "Qon qandini nazorat qiling, insulin rejimiga amal qiling",
        "xavfli": ["Gipoglikemiya (qand pastligi) — tez shirinlik!", "Ketоatsidoz — 103!"],
        "dori": "Insulin — FAQAT shifokor tavsiyasi bilan"
    },
    "diabet 2": {
        "name": "Diabet 2-tur",
        "ehtimol": ["Insulin-qarshilik diabet"],
        "shifokor": "Endokrinolog",
        "uyda": "Parhez, sport, vazn kamaytirish, qand nazorati",
        "xavfli": ["Ko'p siydik + ko'p suv + vazn yo'qotish"],
        "dori": "Metformin — FAQAT shifokor tavsiyasi bilan"
    },
    "gipoglikemiya": {
        "name": "Qon qandi pastligi (Gipoglikemiya)",
        "ehtimol": ["Diabet, ko'p insulin", "Og'ir dietа"],
        "shifokor": "Endokrinolog",
        "uyda": "TEZDA shirinlik iching (shakar, sharbat, konfet)",
        "xavfli": ["Hushdan ketsa — 103!", "Diabetiklarda tez-tez bo'lsa"],
        "dori": "Glukoza gel, tez shirinlik"
    },
    "neyropatiya": {
        "name": "Neyropatiya (asab shikastlanishi)",
        "ehtimol": ["Diabetik neyropatiya", "Alkogol neyropatiyasi"],
        "shifokor": "Nevropatolog",
        "uyda": "Qandni nazorat qiling, alkogol yo'q, vitaminlar",
        "xavfli": ["Oyoq yarasi (diabetda) — tezda shifokor!"],
        "dori": "B vitamini, Milgamma — shifokor tavsiyasi bilan"
    },
    "parkinson": {
        "name": "Parkinson kasalligi belgilari",
        "ehtimol": ["Parkinson kasalligi"],
        "shifokor": "Nevropatolog",
        "uyda": "Mashqlar, balans mashqlari, yiqilmaslik",
        "xavfli": ["Qo'l titrab + yurish qiyinlashsa + ifoda yo'qolsa"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "alzheimer": {
        "name": "Alzheimer kasalligi belgilari",
        "ehtimol": ["Alzheimer dementsiyasi"],
        "shifokor": "Nevropatolog yoki Geriator",
        "uyda": "Aqliy faollik, ijtimoiy aloqalar, to'g'ri ovqat",
        "xavfli": ["Xotira yo'qolsa + adashish + o'zini yo'qotish"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "ms kasalligi": {
        "name": "Ko'p skleroz (MS) shubhasi",
        "ehtimol": ["Ko'p skleroz"],
        "shifokor": "Nevropatolog",
        "uyda": "Stress kam, issiqdan saqlaning",
        "xavfli": ["Ko'rish buzilishi + uvishish + zaiflik — shifokorga"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "meningit": {
        "name": "Meningit (shubhali)",
        "ehtimol": ["Bakterial meningit", "Viral meningit"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "Yotqizing, 103 chaqiring",
        "xavfli": ["Kuchli bosh og'riq + bo'yin qotishi + isitma + nur toqatsizligi — 103!"],
        "dori": "HECH NARSA ICHMANG — tez yordam!"
    },
    "ensefalit": {
        "name": "Ensefalit (shubhali)",
        "ehtimol": ["Viral ensefalit"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "103 chaqiring",
        "xavfli": ["Isitma + hushsizlik + tortishish — 103!"],
        "dori": "HECH NARSA ICHMANG — tez yordam!"
    },
    "rак belgilari": {
        "name": "Onkologiya (saraton) shubhasi",
        "ehtimol": ["Turli xil saraton kasalliklari"],
        "shifokor": "Onkolog — TEZDA tahlil va tekshiruv!",
        "uyda": "Muntazam tekshiruv qilish",
        "xavfli": ["Tushunarsiz vazn yo'qotish + charchoq + qon ketish — shifokorga!"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "limfoma": {
        "name": "Limfa tugunlari kattalashishi",
        "ehtimol": ["Infektsiya", "Limfoma", "Leykemiya"],
        "shifokor": "Terapevt yoki Gematolog",
        "uyda": "Tekshiruv o'tkazing",
        "xavfli": ["Og'riqsiz kattalashsa + isitma + terlash + vazn yo'qotish"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "leykemiya": {
        "name": "Leykemiya (qon saratoni) shubhasi",
        "ehtimol": ["O'tkir leykemiya", "Surunkali leykemiya"],
        "shifokor": "Gematolog — TEZDA!",
        "uyda": "Infektsiyadan saqlaning",
        "xavfli": ["Charchoq + qon ketish + ko'p infektsiya + isitma"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "qorin parda yallig": {
        "name": "Qorin parda yallig'lanishi (Peritonit)",
        "ehtimol": ["Peritonit"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "Yotqizing, 103 chaqiring, hech narsa ichmang",
        "xavfli": ["Qorin qotib qolsa + kuchli og'riq + isitma — 103!"],
        "dori": "HECH NARSA ICHMANG — operatsiya kerak!"
    },
    "diafragma churrasi": {
        "name": "Qo'zg'aluvchan ichak sindromi (IBS)",
        "ehtimol": ["IBS"],
        "shifokor": "Gastroenterolog",
        "uyda": "Stressdan saqlaning, ovqat kundaligi yozing, tolali ovqat",
        "xavfli": ["Qon bilan najas", "Vazn yo'qotish bilan qorin og'riq"],
        "dori": "Mebeverin, Smekta — shifokor tavsiyasi bilan"
    },
    "laktozа intoleransi": {
        "name": "Laktoza murosasizligi",
        "ehtimol": ["Laktaza yetishmovchiligi"],
        "shifokor": "Gastroenterolog",
        "uyda": "Sut mahsulotlarini kamaytiring, laktaza preparatlar",
        "xavfli": ["Har safar sut ichganda ich ketsa"],
        "dori": "Laktaza fermenti — dorixonada sotiladi"
    },
    "tsoeliakiya": {
        "name": "Tsoeliakiya (gluten murosasizligi)",
        "ehtimol": ["Tsoeliakiya"],
        "shifokor": "Gastroenterolog",
        "uyda": "Gluten yo'q diet (bug'doy, arpa, javdar yemang)",
        "xavfli": ["Doimiy ich ketish + vazn yo'qotish + kamqonlik"],
        "dori": "Faqat gluten-free diet — dori kerak emas"
    },
    "skarlatin": {
        "name": "Skarlatina",
        "ehtimol": ["Streptokokk infektsiyasi"],
        "shifokor": "Infektsionist yoki Pediatr",
        "uyda": "Izolyatsiya, ko'p suv, yumshoq ovqat",
        "xavfli": ["Isitma + tomoq og'riq + qizil toshma — shifokorga!"],
        "dori": "Antibiotik — FAQAT shifokor tavsiyasi bilan"
    },
    "difteriya": {
        "name": "Difteriya shubhasi",
        "ehtimol": ["Corynebacterium diphtheriae"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "Izolyatsiya, 103 chaqiring",
        "xavfli": ["Tomoqda oq parda + nafas qiynalsa — 103!"],
        "dori": "HECH NARSA ICHMANG — tez yordam!"
    },
    "botulizm": {
        "name": "Botulizm shubhasi",
        "ehtimol": ["Clostridium botulinum toksin"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "103 chaqiring",
        "xavfli": ["Konsерva yegandan keyin ko'rish buzilsa + zaiflik — 103!"],
        "dori": "HECH NARSA ICHMANG — tez yordam!"
    },
    "quturish": {
        "name": "It/hayvon tishlashi",
        "ehtimol": ["Quturish (rabies) xavfi"],
        "shifokor": "DARHOL tez yordam — emlash kerak!",
        "uyda": "Yarani yuvish (15 min sovun bilan), tezda shifoxonaga",
        "xavfli": ["Har qanday hayvon tishlaganda — TEZDA EMLASH KERAK!"],
        "dori": "Rabies vaktsinasi — shifoxonada"
    },
    "ilon chaqqanda": {
        "name": "Ilon chaqishi",
        "ehtimol": ["Zaharli ilon chaqishi"],
        "shifokor": "DARHOL 103 ga qo'ng'iroq qiling!",
        "uyda": "Tinch turing, bezovta qilmang, ziqqoliq bog'lamang, 103 chaqiring",
        "xavfli": ["Har qanday ilon chaqishi — DARHOL 103!"],
        "dori": "Zardob — faqat shifoxonada"
    },
    "chayoncha chaqqanda": {
        "name": "Chayoncha chaqishi / Ari chaqqanda",
        "ehtimol": ["Zahar reaktsiyasi", "Allergik reaktsiya"],
        "shifokor": "Tez yordam",
        "uyda": "Nish chiqaring, sovuq kompres, antihistaminik iching",
        "xavfli": ["Nafas qiynalsa + yuz shishsa — ANAFILAKSIYA — 103!"],
        "dori": "Suprastin, Adrenalin (og'ir allergiyada) — 103"
    },
    "gipertenziv kriz": {
        "name": "Gipertenziv kriz",
        "ehtimol": ["Qon bosimi keskin ko'tarilishi"],
        "shifokor": "DARHOL tez yordam chaqiring — 103!",
        "uyda": "Tinch yotqizing, Kaptoril berish (agar mavjud bo'lsa), 103 chaqiring",
        "xavfli": ["200/120 dan yuqori — 103!", "Ko'rish buzilsa + og'riq — 103!"],
        "dori": "Kaptoril — lekin 103 ham chaqiring"
    },
    "tаyanch-harakat": {
        "name": "Umurtqa pog'onasi og'rig'i",
        "ehtimol": ["Osteoxondroz", "Grija", "Skolioz"],
        "shifokor": "Nevropatolog yoki Ortoped",
        "uyda": "To'g'ri o'tiring, kuch bajarmang, massaj, LFK",
        "xavfli": ["Oyoqqa tarqaluvchi og'riq", "Siydik/najas nazorat yo'qolsa — 103!"],
        "dori": "Ibuprofen, Voltaren gel"
    },
    "skolioz": {
        "name": "Skolioz (umurtqa qiyshayishi)",
        "ehtimol": ["Idiopatik skolioz"],
        "shifokor": "Ortoped",
        "uyda": "To'g'ri o'tiring, maxsus mashqlar qiling",
        "xavfli": ["30 darajadan ko'p qiyshayish"],
        "dori": "LFK, korsеt — shifokor tavsiyasi bilan"
    },
    "ploskostopie": {
        "name": "Tekis oyoq (Ploskostopie)",
        "ehtimol": ["Oyoq kamar pasayishi"],
        "shifokor": "Ortoped",
        "uyda": "Maxsus taglik kiyish, oyoq mashqlari",
        "xavfli": ["Kuchli og'riq + tizza/bel og'riq"],
        "dori": "Ortopedik tagliklar"
    },
    "qovuq shamollashi": {
        "name": "O'pka qovuqchasi (plevrit)",
        "ehtimol": ["Plevrit"],
        "shifokor": "Pulmonolog yoki Terapevt",
        "uyda": "Dam oling",
        "xavfli": ["Nafas olishda keskin og'riq + isitma"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "ftiziatrik": {
        "name": "Sarkoidoz",
        "ehtimol": ["Sarkoidoz"],
        "shifokor": "Pulmonolog yoki Terapevt",
        "uyda": "Dam oling, sigaret qoldiring",
        "xavfli": ["Yo'tal + nafas qiynalish + charchoq + ko'z muammolari"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "uremiya": {
        "name": "Buyrak yetishmovchiligi (shubhali)",
        "ehtimol": ["Surunkali buyrak yetishmovchiligi"],
        "shifokor": "Nefrologik — TEZDA!",
        "uyda": "Suyuqlik va tuz nazorat",
        "xavfli": ["Siydik yo'qligi + shish + zaiflik + ko'ngil aynish"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "erektil disfunktsiya": {
        "name": "Jinsiy buzilish",
        "ehtimol": ["Psixogen", "Vascular", "Gormonal", "Diabetik"],
        "shifokor": "Androlog yoki Seksolog",
        "uyda": "Sport, to'g'ri ovqat, stress kamaytirish, alkogol yo'q",
        "xavfli": ["Diabet bilan birga bo'lsa — endokrinologga ham boring"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "menopauza": {
        "name": "Menopauza belgilari",
        "ehtimol": ["Menopauza", "Perimenopauza"],
        "shifokor": "Ginekolog yoki Endokrinolog",
        "uyda": "Sport, to'g'ri ovqatlanish, fitoestrogenlar",
        "xavfli": ["Qon ketish menopauzadan keyin — TEZDA shifokorga!"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "osteoartrit": {
        "name": "Osteoartrit (bo'g'im yeyilishi)",
        "ehtimol": ["Osteoartrit"],
        "shifokor": "Revmatolog yoki Ortoped",
        "uyda": "Vazn kamaytirish, suv aerobikasi, issiq/sovuq kompres",
        "xavfli": ["Yura olmasa", "Bo'g'im shishib qolsa"],
        "dori": "Glukozamin, Xondroitin — shifokor tavsiyasi bilan"
    },
    "fibromialgiya": {
        "name": "Fibromialgiya",
        "ehtimol": ["Fibromialgiya sindromi"],
        "shifokor": "Nevropatolog yoki Revmatolog",
        "uyda": "Engil sport, uyqu rejimi, stress kamaytirish",
        "xavfli": ["Butun tana og'rig'i + uyqu buzilishi + charchoq"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "fenilketonuriya": {
        "name": "Metabolik buzilish (shubhali)",
        "ehtimol": ["Metabolik kasalliklar"],
        "shifokor": "Endokrinolog",
        "uyda": "Tahlil natijalariga qarab harakat qiling",
        "xavfli": ["Bolalarda rivojlanish kechikishi"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "ko'z bosimligi": {
        "name": "Glaukoma (ko'z bosimi)",
        "ehtimol": ["Birlamchi glaukoma"],
        "shifokor": "Oftalmolog",
        "uyda": "Qorong'uda uzoq o'tirmaslik, stress kamaytirish",
        "xavfli": ["Ko'rish doirasi toraysa", "Ko'z og'riq + ko'ngil aynish + ko'rish buzilishi — tezda!"],
        "dori": "Ko'z tomizg'i — FAQAT shifokor tavsiyasi bilan"
    },
    "katarakta": {
        "name": "Katarakta",
        "ehtimol": ["Ko'z gavhagi loyqalanishi"],
        "shifokor": "Oftalmolog",
        "uyda": "Quyosh ko'zoynagi kiyish, yaxshi yoritish",
        "xavfli": ["Ko'rish juda yomonlashsa — operatsiya kerak"],
        "dori": "Kataxrom tomizg'i (faqat sekinlashtiradi) — operatsiya kerak"
    },
    "konyunktivit": {
        "name": "Ko'z yallig'lanishi (Konjunktivit)",
        "ehtimol": ["Bakterial", "Viral", "Allergik konjunktivit"],
        "shifokor": "Oftalmolog",
        "uyda": "Ko'zni yuvish, qo'l gigienasi, sochiq almashtirish",
        "xavfli": ["Ko'rish yomonlashsa", "Kuchli og'riq bilan"],
        "dori": "Albucid tomizg'i (bakterial), Vizin — shifokor tavsiyasi bilan"
    },
    "strabizm": {
        "name": "Ko'z qisiqlik (Kosoglaziye)",
        "ehtimol": ["Paralitik", "Funksional strabizm"],
        "shifokor": "Oftalmolog",
        "uyda": "Ko'z mashqlari (shifokor tavsiyasi bilan)",
        "xavfli": ["Bolalarda — tezda shifokorga! Lazif ko'z rivojlanmasligi mumkin"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "gemofilia": {
        "name": "Qon to'xtamaslik (shubhali)",
        "ehtimol": ["Gemofilia", "Trombotsitopeniya", "Vitamin K yetishmovchiligi"],
        "shifokor": "Gematolog",
        "uyda": "Jarohatdan saqlaning",
        "xavfli": ["Mayda jarohатdan ko'p qon ketsa — shifokorga!"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "anemiya aplastik": {
        "name": "Aplastik anemiya (shubhali)",
        "ehtimol": ["Aplastik anemiya"],
        "shifokor": "Gematolog — TEZDA!",
        "uyda": "Infektsiyadan saqlaning",
        "xavfli": ["Charchoq + qon ketish + tez-tez infektsiya"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
    "splenomegaliya": {
        "name": "Taloq kattalashishi",
        "ehtimol": ["Infektsiya", "Qon kasalligi", "Jigar kasalligi"],
        "shifokor": "Terapevt yoki Gematolog",
        "uyda": "Kontakt sport qilmang (taloq yorilishi xavfi)",
        "xavfli": ["Chap qorin og'rig'i + isitma + charchoq"],
        "dori": "Faqat shifokor tavsiyasi bilan"
    },
})


# ═══════════════════════════════════════════════
#  KASALLIK QIDIRISH FUNKSIYASI (AI siz ishlaydi)
# ═══════════════════════════════════════════════
def analyze_symptoms(text: str, lang: str) -> str:
    """Simptom matni bo'yicha kasalliklarni qidiradi"""
    text_lower = text.lower()
    
    found = []
    for key, disease in DISEASES_DB.items():
        # Kalit so'z bo'yicha qidirish
        if key in text_lower:
            found.append(disease)
            continue
        # Kasallik nomida qidirish
        if any(word in text_lower for word in key.split()):
            found.append(disease)

    if not found:
        # Umumiy maslahat
        if lang == "uz":
            return (
                "🔍 Aniq kasallik topilmadi.\n\n"
                "💡 *Maslahat:*\n"
                "• Simptomlarni batafsilroq yozing\n"
                "• Masalan: 'bosh og\'riq', 'isitma', 'qorin og\'riq'\n"
                "• Yoki terapevtga murojaat qiling\n\n"
                "🚨 Jiddiy holatlarda: *103*"
            )
        else:
            return (
                "🔍 Точный диагноз не найден.\n\n"
                "💡 *Совет:*\n"
                "• Опишите симптомы подробнее\n"
                "• Например: 'головная боль', 'температура'\n"
                "• Или обратитесь к терапевту\n\n"
                "🚨 При серьёзных случаях: *103*"
            )

    # Topilgan kasalliklarni ko'rsatish
    result = []
    for d in found[:3]:  # Eng ko'pi 3 ta
        if lang == "uz":
            xavfli_text = "\n".join([f"  ⛔ {x}" for x in d["xavfli"]])
            result.append(
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🏥 *{d['name']}*\n\n"
                f"📋 *Ehtimoliy sabablar:*\n" +
                "\n".join([f"  • {e}" for e in d["ehtimol"]]) +
                f"\n\n👨‍⚕️ *Shifokor:* {d['shifokor']}\n\n"
                f"🏠 *Uyda nima qilish:*\n  {d['uyda']}\n\n"
                f"💊 *Dori:* {d.get('dori', 'Shifokor tavsiyasi bilan')}\n\n"
                f"⚠️ *Xavfli belgilar:*\n{xavfli_text}"
            )
        else:
            xavfli_text = "\n".join([f"  ⛔ {x}" for x in d["xavfli"]])
            result.append(
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🏥 *{d['name']}*\n\n"
                f"📋 *Возможные причины:*\n" +
                "\n".join([f"  • {e}" for e in d["ehtimol"]]) +
                f"\n\n👨‍⚕️ *Врач:* {d['shifokor']}\n\n"
                f"🏠 *Дома:*\n  {d['uyda']}\n\n"
                f"💊 *Лекарство:* {d.get('dori', 'По назначению врача')}\n\n"
                f"⚠️ *Опасные признаки:*\n{xavfli_text}"
            )
    
    header = f"🔍 *{len(found)} ta natija topildi:*\n\n" if lang == "uz" else f"🔍 *Найдено {len(found)} результатов:*\n\n"
    footer = "\n\n━━━━━━━━━━━━━━━━━━\n⚠️ _Bu ma\'lumot yo\'naltiruvchi. Shifokor ko\'rigisiz dori ichmang!_" if lang == "uz" else "\n\n━━━━━━━━━━━━━━━━━━\n⚠️ _Информация ориентировочная. Не принимайте лекарства без врача!_"
    
    return header + "\n\n".join(result) + footer


# ═══════════════════════════════════════════════
#  TERMEZ — 20 TA KLINIKA MA'LUMOTLAR BAZASI
# ═══════════════════════════════════════════════
TERMEZ_CLINICS = [
    {
        "name": "Sultan Hospital",
        "phone": "+998 55 452 55 55",
        "hours": "Du-Sha 08:00-17:00",
        "type": "🏥 Xususiy klinika",
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
        "type": "🏥 Xususiy klinika",
        "lat": 37.2265721,
        "lon": 67.2680984,
    },
    {
        "name": "Sanatrix Klinika (LOR)",
        "phone": "—",
        "hours": "24/7 🕐",
        "type": "🏥 LOR mutaxassisi",
        "lat": 37.2397997,
        "lon": 67.2933794,
    },
    {
        "name": "Dental Service Termez",
        "phone": "+998 90 247 52 36",
        "hours": "Du-Sha 09:00-19:00",
        "type": "🦷 Stomatologiya",
        "lat": 37.2428755,
        "lon": 67.2995179,
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
        "name": "Respublika Tez Tibbiy Yordam Markazi",
        "phone": "103",
        "hours": "24/7 🚨",
        "type": "🚑 Tez yordam",
        "lat": 37.2334540,
        "lon": 67.2905916,
    },
    {
        "name": "Respublika Shoshilinch Tibbiy Yordam",
        "phone": "103",
        "hours": "24/7 🚨",
        "type": "🚑 Shoshilinch yordam",
        "lat": 37.2330125,
        "lon": 67.2918097,
    },
    {
        "name": "Termiz 1-Sonli Oilaviy Poliklinika",
        "phone": "+998 91 585 26 27",
        "hours": "Du-Sha 08:00-18:00",
        "type": "🏛 Davlat poliklinikasi",
        "lat": 37.2372155,
        "lon": 67.3026849,
    },
    {
        "name": "Termiz 2-Sonli Oilaviy Poliklinika",
        "phone": "+998 97 242 40 77",
        "hours": "Du-Sha 08:00-20:00",
        "type": "🏛 Davlat poliklinikasi",
        "lat": 37.2427518,
        "lon": 67.2810899,
    },
    {
        "name": "Termiz 3-Sonli Oilaviy Poliklinika",
        "phone": "+998 76 225 02 47",
        "hours": "Du-Sha 08:00-18:00",
        "type": "🏛 Davlat poliklinikasi",
        "lat": 37.2397837,
        "lon": 67.2921241,
    },
    {
        "name": "Viloyat Bolalar Shifoxonasi",
        "phone": "—",
        "hours": "24/7",
        "type": "👶 Bolalar shifoxonasi",
        "lat": 37.2432319,
        "lon": 67.2761918,
    },
    {
        "name": "Termiz Temir Yo'l Shifoxonasi",
        "phone": "—",
        "hours": "Du-Ju 08:00-15:00",
        "type": "🏛 Shifoxona",
        "lat": 37.2451077,
        "lon": 67.2802299,
    },
    {
        "name": "Termiz Tibbiyot Akademiyasi Klinikasi",
        "phone": "+998 90 909 00 36",
        "hours": "Du-Ju 08:00-17:00",
        "type": "🏛 Akademik klinika",
        "lat": 37.2199468,
        "lon": 67.2850951,
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
    {
        "name": "Termiz Stomatologiya Klinikasi",
        "phone": "+998 90 555 44 33",
        "hours": "Du-Sha 09:00-18:00",
        "type": "🦷 Stomatologiya",
        "lat": 37.2380000,
        "lon": 67.2900000,
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
    """Lokal kasallik bazasidan javob beradi — internet kerak emas!"""
    symptom = prompt
    for prefix in ["Bemor alomatlari: ", "Simptomlar: ", "Savol: ", "Вопрос: ", "Симптомы: "]:
        if prefix in prompt:
            symptom = prompt.split(prefix)[-1].split("\n")[0].strip()
            break

    result = analyze_symptoms(symptom, lang)

    if result:
        if lang == "uz":
            lines = ["🔍 *Tahlil natijalari:*\n",
                     "🤒 *Ehtimoliy kasalliklar:*"]
            for d in result["ehtimoliy"]:
                lines.append(f"  • {d}")
            lines.append(f"\n👨‍⚕️ *Qaysi shifokor:*  {result['shifokor']}")
            lines.append(f"\n🏠 *Uyda nima qilish:*  {result['uy']}")
            if result["xavfli"]:
                lines.append("\n⚠️ *Xavfli belgilar:*")
                for x in result["xavfli"]:
                    lines.append(f"  🚨 {x}")
            lines.append("\n\n⚠️ _Men shifokor emasman. Faqat yo'naltiruvchi ma'lumot!_")
            return "\n".join(lines)
        else:
            lines = ["🔍 *Результаты анализа:*\n",
                     "🤒 *Возможные заболевания:*"]
            for d in result["ehtimoliy"]:
                lines.append(f"  • {d}")
            lines.append(f"\n👨‍⚕️ *К какому врачу:*  {result['shifokor']}")
            lines.append(f"\n🏠 *Что делать дома:*  {result['uy']}")
            if result["xavfli"]:
                lines.append("\n⚠️ *Опасные симптомы:*")
                for x in result["xavfli"]:
                    lines.append(f"  🚨 {x}")
            lines.append("\n\n⚠️ _Я не врач. Только ориентировочная информация!_")
            return "\n".join(lines)
    else:
        if lang == "uz":
            return ("😕 Bu simptom bazamda yo'q.\n\n"
                    "Quyidagilarni sinab ko'ring:\n"
                    "• bosh og'riq  • isitma  • yo'tal\n"
                    "• tomoq og'rishi  • qorin og'rishi\n"
                    "• bel og'rishi  • nafas qisishi\n\n"
                    "👨‍⚕️ Yoki to'g'ridan shifokorga murojaat qiling!")
        else:
            return ("😕 Этого симптома нет в базе.\n\n"
                    "Попробуйте написать:\n"
                    "• головная боль  • температура  • кашель\n"
                    "• боль в горле  • боль в животе\n"
                    "• боль в пояснице  • одышка\n\n"
                    "👨‍⚕️ Или обратитесь к врачу напрямую!")


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
