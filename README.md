# AI FactGuard MVP v0.2

نسخة أولية حقيقية منطقياً: واجهة Streamlit + OpenAI Responses API + Web Search + SQLite.

## التشغيل
1. ثبّت Python 3.11 أو أحدث.
2. داخل المجلد:
   `python -m venv .venv`
3. Windows:
   `.venv\Scripts\activate`
4. ثم:
   `pip install -r requirements.txt`
5. انسخ `.env.example` إلى `.env` وضع مفتاح OpenAI API.
6. شغّل:
   `streamlit run app.py`

## مهم
هذه ليست منصة تحقق نهائية. الهدف أن يرى المستخدم الادعاء والأدلة والمصادر وملخص سبب التقييم، مع الإقرار بعدم اليقين. الادعاءات السياسية والانتخابية والأزمات والصحة والسلامة تحتاج تحفظاً ومراجعة بشرية.
