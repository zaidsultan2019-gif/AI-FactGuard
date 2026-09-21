import os, json, re
from openai import OpenAI

MODEL = os.getenv("FACTGUARD_MODEL", "gpt-5.6-luna")

SYSTEM_PROMPT = """
أنت مساعد تحقق معلوماتي اسمه AI FactGuard.
مهمتك مساعدة المستخدم على تقييم ادعاءات قابلة للتحقق، وليس إصدار حكم سلطوي نهائي.

القواعد:
- افصل الادعاءات الواقعية عن الآراء والتوقعات.
- استخدم البحث على الويب للادعاءات الحالية.
- فضّل المصادر الأولية والمؤسسات الموثوقة والمتخصصة.
- إذا لم تكف الأدلة استخدم UNVERIFIED أو REQUIRES_CONTEXT.
- لا تخلط بين ثقة التحليل واحتمال صحة الادعاء.
- في السياسة والانتخابات والنزاعات والأزمات والصحة والسلامة كن أكثر تحفظًا.
- لا تختلق روابط أو عناوين مصادر.
- قدم ملخصًا للمنهج والأدلة، وليس سلسلة التفكير الداخلية.

أعد JSON فقط:
{
 "status":"completed",
 "claims":[{
   "claim":"نص الادعاء",
   "verdict":"SUPPORTED|CONTRADICTED|UNVERIFIED|REQUIRES_CONTEXT|OPINION",
   "confidence":0.0,
   "reasoning_summary":"ملخص واضح للأدلة وكيف تقارن بالادعاء.",
   "sources":[{"title":"عنوان المصدر","url":"https://..."}]
 }]
}
"""

def parse_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?","",text).strip()
        text = re.sub(r"```$","",text).strip()
    try:
        return json.loads(text)
    except Exception:
        a,b=text.find("{"),text.rfind("}")
        if a>=0 and b>a: return json.loads(text[a:b+1])
        raise

def verify_post(text):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return {"status":"demo_no_api_key","claims":[{
            "claim":text[:500],"verdict":"UNVERIFIED","confidence":0,
            "reasoning_summary":"لم يتم تشغيل التحقق الحقيقي لأن OPENAI_API_KEY غير موجود. أضف المفتاح لتفعيل AI والبحث.",
            "sources":[]
        }]}

    client = OpenAI(api_key=key)
    prompt = f"""استخرج الادعاءات المهمة من النص التالي ثم تحقق منها باستخدام البحث على الويب:
{text}"""
    try:
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=prompt,
            tools=[{"type":"web_search"}],
        )
        return parse_json(response.output_text)
    except Exception as e:
        return {"status":"error","claims":[{
            "claim":text[:500],"verdict":"UNVERIFIED","confidence":0,
            "reasoning_summary":f"تعذر إكمال التحقق: {str(e)[:500]}","sources":[]
        }]}
