import streamlit as st
import os
import pandas as pd
from PIL import Image, ImageEnhance
from openai import OpenAI
from supabase import create_client

# ==========================================
# 1. إعدادات النظام وقراءة الـ Secrets
# ==========================================
st.set_page_config(page_title="TASSAOUT OMEGA OS - SUPER AI AGENT", page_icon="👑", layout="wide")

# قراءة مفاتيح الاتصال من الـ Secrets بأمان
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
except KeyError as e:
    st.error(f"خطأ: المفتاح التالي غير موجود في إعدادات Streamlit Secrets: {e}")
    st.stop()

# تهيئة العملاء
client = OpenAI(api_key=openai_api_key)
supabase = create_client(supabase_url, supabase_key)

# تهيئة الذاكرة المؤقتة للتطبيق
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك يا عامر. أنا وكيلك الذكي الخارق (Super Multidomain Agent). جاهز لإدارة العروض، توليد الصور بالذكاء الاصطناعي، وتحليل البيانات معك الآن!"}
    ]

# ==========================================
# 2. القائمة الجانبية للتحكم الشامل
# ==========================================
st.sidebar.title("👑 لوحة تحكم OMEGA OS")
app_mode = st.sidebar.radio("اختر الوحدة الذكية:", [
    "💬 الوكيل الذكي الفائق (Multi-Domain AI)", 
    "✨ استوديو توليد الصور والمعالجة", 
    "📋 إدارة وعرض صفقات Tassaout"
])

# ==========================================
# 3. الوحدة الأولى: الوكيل الذكي الفائق
# ==========================================
if app_mode == "💬 الوكيل الذكي الفائق (Multi-Domain AI)":
    st.title("🤖 الوكيل الذكي المتعدد القطاعات (Super AI Agent)")
    st.write("تفاعل مع الوكيل لصياغة المحتوى، تحليل السوق، وكتابة إعلانات تسويقية احترافية لعقاراتك وخدماتك.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if user_prompt := st.chat_input("اطرح سؤالك أو اكتب البرومبت للوكيل الذكي..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)

        # استدعاء نموذج OpenAI لتوليد الرد الاحترافي
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي ومحترف لإدارة العقارات والمشاريع الرقمية لعامر في قلعة السراغنة ومراكش."},
                    {"role": "user", "content": user_prompt}
                ]
            )
            agent_reply = response.choices[0].message.content
        except Exception as e:
            agent_reply = f"عذراً، حدث خطأ أثناء الاتصال بنظام الذكاء الاصطناعي: {e}"

        st.session_state.messages.append({"role": "assistant", "content": agent_reply})
        with st.chat_message("assistant"):
            st.write(agent_reply)

# ==========================================
# 4. الوحدة الثانية: استوديو توليد ومعالجة الصور بلا حدود
# ==========================================
elif app_mode == "✨ استوديو توليد الصور والمعالجة":
    st.title("🎨 استوديو الرؤية بالذكاء الاصطناعي (AI Visual Studio)")
    
    tab1, tab2 = st.tabs(["✨ توليد بالبرومبت (DALL-E 3)", "🛠️ معالجة وتحسين الصور المرفوعة"])

    with tab1:
        st.subheader("توليد صور واقعية للعقارات، السيارات والمشاريع")
        image_prompt = st.text_input("صف المشهد بدقة:", placeholder="مثال: فيلا فخمة بقلعة السراغنة، تصوير معماري احترافي، إضاءة طبيعية، 8k...")
        
        if st.button("🚀 توليد الصورة الفعلية الآن"):
            with st.spinner("جاري التواصل مع محرك الذكاء الاصطناعي للرسم..."):
                try:
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=f"Professional architectural photography of {image_prompt}, luxury style, high resolution, photorealistic --ar 16:9",
                        n=1,
                        size="1024x1024"
                    )
                    img_url = response.data[0].url
                    st.image(img_url, caption="الصورة المولدة بالذكاء الاصطناعي", use_container_width=True)
                    st.success("تم التوليد بنجاح!")
                except Exception as e:
                    st.error(f"خطأ أثناء التوليد: {e}")

    with tab2:
        st.subheader("تحسين ورفع الصور الحالية")
        uploaded_image = st.file_uploader("اختر صورة لتحسينها:", type=["jpg", "png", "jpeg"])
        
        if uploaded_image is not None:
            img = Image.open(uploaded_image)
            st.image(img, caption="الصورة الأصلية", use_container_width=True)
            if st.button("✨ تطبيق التحسين الذكي للألوان والحدة"):
                enhancer = ImageEnhance.Sharpness(img)
                processed_img = enhancer.enhance(2.1)
                st.image(processed_img, caption="الصورة بعد المعالجة الاحترافية", use_container_width=True)
                st.success("تمت معالجة الصورة بنجاح!")

# ==========================================
# 5. الوحدة الثالثة: إدارة وعرض صفقات Tassaout (Supabase)
# ==========================================
elif app_mode == "📋 إدارة وعرض صفقات Tassaout":
    st.title("📋 إدارة المحتوى والعروض والصفقات (Supabase)")
    
    with st.expander("➕ إضافة عرض أو صفقة جديدة للقاعدة", expanded=False):
        with st.form("add_listing"):
            t_title = st.text_input("عنوان الصفقة / العرض:")
            t_city = st.selectbox("المدينة:", ["قلعة السراغنة", "مراكش", "الدار البيضاء", "أكادير"])
            t_type = st.selectbox("القطاع:", ["عقار", "سيارات", "فلاحة", "مواد إنشائية"])
            t_desc = st.text_area("وصف تفصيلي:")
            submitted = st.form_submit_button("حفظ وإضافة العرض")
            
            if submitted:
                if t_title and t_desc:
                    try:
                        # إرسال البيانات إلى جدول properties في Supabase
                        data = supabase.table("properties").insert({
                            "title": t_title,
                            "city": t_city,
                            "type": t_type,
                            "description": t_desc
                        }).execute()
                        st.success("تمت إضافة العرض بنجاح إلى قاعدة البيانات!")
                    except Exception as e:
                        st.error(f"خطأ في الإضافة لقاعدة البيانات: {e}")
                else:
                    st.warning("المرجو ملء العنوان والوصف.")

    st.markdown("---")
    st.subheader("📌 العروض والصفقات المسجلة حالياً:")
    
    try:
        response = supabase.table("properties").select("*").execute()
        listings = response.data
        if listings:
            df = pd.DataFrame(listings)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("لا توجد عروض مسجلة حالياً في قاعدة البيانات.")
    except Exception as e:
        st.warning(f"جاري إعداد الجدول في Supabase... (تأكد من إنشاء جدول 'properties'): {e}")
