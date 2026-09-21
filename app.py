import streamlit as st
from factguard import verify_post
from db import init_db, save_check, list_checks, save_appeal

st.set_page_config(page_title="AI FactGuard", page_icon="🛡️", layout="wide")
init_db()

st.markdown("""
<style>
.block-container { max-width: 1100px; }
.result { padding: 16px; border-radius: 12px; border: 1px solid #ddd; }
.small { color:#666; font-size:.9rem; }
</style>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None

st.sidebar.title("🛡️ AI FactGuard")
st.sidebar.caption("مساعد للتحقق قبل المشاركة")
page = st.sidebar.radio("القائمة", ["فحص منشور","النتيجة والأدلة","الاعتراض","سجل الفحوصات","حول المشروع"])

if page == "فحص منشور":
    st.title("فحص منشور قبل المشاركة")
    st.info("الذكاء الاصطناعي مساعد للتحقق، وليس حكمًا نهائيًا. ستظهر الأدلة والمصادر وملخص طريقة الوصول للنتيجة.")
    text = st.text_area("الصق النص أو الخبر هنا", height=220,
                        placeholder="اكتب الخبر أو المنشور الذي تريد التحقق منه...")
    if st.button("🔎 ابدأ التحقق", type="primary", use_container_width=True):
        if not text.strip():
            st.warning("أدخل نصًا أولًا.")
        else:
            with st.spinner("يتم استخراج الادعاءات والبحث عن الأدلة..."):
                result = verify_post(text)
            st.session_state.result = result
            save_check(text, result)
            st.success("اكتمل الفحص. افتح «النتيجة والأدلة».")
    st.subheader("كيف يعمل؟")
    cols = st.columns(4)
    for c, title, desc in zip(cols,
        ["استخراج الادعاءات","البحث عن الأدلة","مقارنة الأدلة","نتيجة شفافة"],
        ["فصل الكلام القابل للتحقق عن الرأي.","البحث عن مصادر مرتبطة بالادعاء.","مقارنة الأدلة المؤيدة والمعارضة.","شرح مختصر مع المصادر."]):
        c.subheader(title); c.caption(desc)

elif page == "النتيجة والأدلة":
    st.title("النتيجة والأدلة")
    result = st.session_state.result
    if not result:
        st.warning("لم يتم إجراء فحص بعد.")
    else:
        for i, claim in enumerate(result.get("claims", []), 1):
            st.markdown(f"### الادعاء {i}")
            st.markdown(f"**{claim.get('claim','')}**")
            st.markdown(f"**التقييم المساعد:** `{claim.get('verdict','UNVERIFIED')}`")
            conf = claim.get("confidence")
            if conf is not None:
                st.progress(min(max(float(conf),0),1))
                st.caption(f"ثقة المساعد في التحليل: {float(conf):.0%} — وليست احتمال صحة الادعاء.")
            st.markdown("**كيف وصل إلى النتيجة؟**")
            st.write(claim.get("reasoning_summary","لا يوجد شرح."))
            st.markdown("**الأدلة والمصادر:**")
            for s in claim.get("sources", []):
                url = s.get("url")
                title = s.get("title") or url or "مصدر"
                st.markdown(f"- [{title}]({url})" if url else f"- {title}")
            st.divider()
        st.warning("افتح المصادر وراجع الأدلة بنفسك، خصوصًا في السياسة والانتخابات والأزمات والصحة والسلامة.")

elif page == "الاعتراض":
    st.title("تقديم اعتراض")
    st.write("أرسل ملاحظتك إذا وجدت خطأ في النتيجة أو استخدامًا غير مناسب لمصدر.")
    text = st.text_area("ملاحظتك", height=180)
    if st.button("إرسال الاعتراض", type="primary"):
        if text.strip():
            save_appeal(text); st.success("تم تسجيل الاعتراض للمراجعة.")
        else:
            st.warning("اكتب ملاحظتك أولًا.")

elif page == "سجل الفحوصات":
    st.title("سجل الفحوصات")
    rows = list_checks()
    if not rows:
        st.info("لا توجد فحوصات محفوظة.")
    for row in rows:
        st.markdown(f"**{row['created_at']}**")
        st.caption(row["text"][:300])
        st.divider()

else:
    st.title("عن AI FactGuard")
    st.markdown("""
**AI FactGuard — حارس الحقيقة بالذكاء الاصطناعي**

يساعد المستخدم على التحقق قبل إعادة نشر المعلومات عبر استخراج الادعاءات،
البحث عن الأدلة، عرض المصادر، وشرح مختصر لطريقة الوصول إلى التقييم.

هذه نسخة MVP تقنية أولية وليست جهة إعلامية أو حكومية، ولا تعني تأييد أي شركة أو منصة للمشروع.
""")
