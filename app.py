import streamlit as st
import json
import os
import base64
import pandas as pd
from PIL import Image, ImageEnhance
from openai import OpenAI
from supabase import create_client

# ==========================================
# 1. إعدادات الهوية والبنية الأساسية
# ==========================================
st.set_page_config(page_title="TASSAOUT OMEGA OS", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #062314; color: #f8fafc; font-family: Tahoma, sans-serif; }
    .prop-card { padding: 20px; border-radius: 12px; border: 1px solid #22c55e; margin-bottom: 20px; background-color: #0f3d24; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .badge-cat { background-color: #22c55e; color: #000; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 8px; }
    .stButton>button { background-color: #22c55e; color: #000; font-weight: bold; border-radius: 8px; border: none; transition: 0.3s; width: 100%; }
    .stButton>button:hover { background-color: #16a34a; color: #fff; }
    .prompt-box { background-color: #03160b; border: 1px dashed #22c55e; padding: 12px; border-radius: 8px; color: #a3e635; font-size: 13px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# قراءة مفاتيح الاتصال
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    client = OpenAI(api_key=openai_api_key)
    supabase = create_client(supabase_url, supabase_key)
except Exception:
    client = None
    supabase = None

DATA_FILE = "tassaout_interactive_ads.json"

def load_ads():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_ads(ads):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(ads, f, ensure_ascii=False, indent=4)

if 'ads_data' not in st.session_state:
    st.session_state.ads_data = load_ads()

# دالة توليد رابط واتساب دقيق ومباشر
def get_whatsapp_link(ad_title=""):
    phone = "212691897126"
    text = f"مرحباً عامر، أنا مهتم بخصوص: {ad_title}"
    return f"https://wa.me/{phone}?text={requests_utils_quote(text)}"

import urllib.parse
def requests_utils_quote(text):
    return urllib.parse.quote(text)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "مرحباً بك يا عامر! النظام جاهز لدعم مشاريعك بقلعة السراغنة ومراكش."}
    ]

# ==========================================
# 2. القائمة الجانبية (تم تحسين مظهرها وترتيبها)
# ==========================================
st.sidebar.title("👑 Tassaout OMEGA OS")
app_mode = st.sidebar.radio("القائمة الرئيسية:", [
    "🏠 المنصة الرئيسية والعروض",
    "➕ إضافة إعلان جديد (صور متعددة وكاميرا)",
    "🎨 مصنع البرومبتات والهوية",
    "🤖 الوكيل الذكي (AI Agent)",
    "✨ استوديو توليد ومعالجة الصور",
    "📋 إدارة صفقات Supabase",
    "🛠️ الخدمات الرقمية والهندسية",
    "📞 تواصل"
])

st.markdown("---")

# ==========================================
# 3. محتوى الأقسام
# ==========================================

if app_mode == "🏠 المنصة الرئيسية والعروض":
    st.title("🏢 Tassaout Immo & Media")
    
    filter_option = st.selectbox("فلترة العروض حسب القطاع:", [
        "جميع العروض",
        "العقاري الفلاحي",
        "العقاري الصناعي والتجاري",
        "العقاري المهني والاستثماري",
        "بيع مواد البناء",
        "مكتب الدراسات والهندسة",
        "الهندسة الرقمية والتصوير",
        "التسويق العقاري والتجاري"
    ])
    
    displayed_ads = st.session_state.ads_data
    if filter_option != "جميع العروض":
        displayed_ads = [ad for ad in st.session_state.ads_data if ad.get('category') == filter_option]
    
    if not displayed_ads:
        st.info("لا توجد عروض مضافة حالياً. قم بإضافة إعلانك الأول من القائمة الجانبية.")
    else:
        for idx, ad in enumerate(displayed_ads):
            st.markdown(f"""
            <div class="prop-card">
                <span class="badge-cat">{ad.get('category', 'عام')}</span>
                <h3 style="color: #4ade80; margin: 10px 0 5px 0;">{ad.get('title', '')}</h3>
                <p style="font-size: 13px; color: #cbd5e1; margin: 3px 0;">📍 {ad.get('location', '')}</p>
                <p style="font-size: 13px; color: #94a3b8; margin: 6px 0;">{ad.get('description', '')}</p>
                <p style="font-size: 15px; font-weight: bold; color: #4ade80;">{ad.get('price', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # عرض الصور المتعددة بشكل صحيح ومزود بـ columns
            images = ad.get('images', [])
            if images:
                cols = st.columns(len(images) if len(images) <= 3 else 3)
                for img_i, img_data in enumerate(images):
                    with cols[img_i % 3]:
                        st.image(img_data, use_container_width=True)

            # زر واتساب مباشر يعمل 100%
            w_link = f"https://wa.me/212691897126?text={urllib.parse.quote('مرحباً، أنا مهتم بعرضكم: ' + ad.get('title', ''))}"
            st.markdown(f"""
                <div style="margin-bottom: 25px;">
                    <a href="{w_link}" target="_blank" style="background-color: #16a34a; color: #fff; padding: 10px 15px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block;">💬 تواصل عبر الواتساب</a>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🗑️ حذف هذا العرض #{idx}", key=f"del_{idx}"):
                st.session_state.ads_data.remove(ad)
                save_ads(st.session_state.ads_data)
                st.rerun()

elif app_mode == "➕ إضافة إعلان جديد (صور متعددة والكاميرا)":
    st.title("➕ إضافة عرض أو إعلان جديد")
    with st.form("new_ad_form"):
        title = st.text_input("عنوان العرض", placeholder="مثال: أرض فلاحية مجهزة للبيع")
        category = st.selectbox("القطاع أو الفئة", [
            "العقاري الفلاحي",
            "العقاري الصناعي والتجاري",
            "العقاري المهني والاستثماري",
            "بيع مواد البناء",
            "مكتب الدراسات والهندسة",
            "الهندسة الرقمية والتصوير",
            "التسويق العقاري والتجاري"
        ])
        location = st.text_input("الموقع", placeholder="مثال: قلعة السراغنة / مراكش")
        price = st.text_input("السعر أو التكلفة", placeholder="مثال: 1,200,000 DH")
        
        # خيار رفع عدة صور من الهاتف أو الحاسوب
        uploaded_files = st.file_uploader("اختر صور متعددة (استوديو الهاتف)", accept_multiple_files=True, type=["png", "jpeg", "jpg", "webp"])
        
        # خيار التقاط صورة مباشرة بالكاميرا
        camera_file = st.camera_input("أو التقط صورة مباشرة بالكاميرا:")
        
        description = st.text_area("التفاصيل والوصف", placeholder="اكتب تفاصيل الإعلان هنا...")
        
        submitted = st.form_submit_button("نشر العرض فوراً")
        if submitted:
            if title and location and price and description:
                images_list = []
                
                # معالجة الصور المرفوعة المتعددة
                if uploaded_files:
                    for file in uploaded_files:
                        bytes_data = file.read()
                        encoded_img = base64.b64encode(bytes_data).decode("utf-8")
                        images_list.append(f"data:image/jpeg;base64,{encoded_img}")
                
                # معالجة صورة الكاميرا المباشرة إن وجدت
                if camera_file:
                    cam_bytes = camera_file.read()
                    encoded_cam = base64.b64encode(cam_bytes).decode("utf-8")
                    images_list.append(f"data:image/jpeg;base64,{encoded_cam}")
                
                new_ad = {
                    "title": title,
                    "category": category,
                    "location": location,
                    "price": price,
                    "description": description,
                    "images": images_list
                }
                st.session_state.ads_data.insert(0, new_ad)
                save_ads(st.session_state.ads_data)
                st.success("تم نشر العرض بنجاح مع صوره المتعددة!")
                st.rerun()
            else:
                st.error("الرجاء ملء الحقول الإجبارية.")

elif app_mode == "🎨 مصنع البرومبتات والهوية":
    st.title("🎨 مصنع البرومبتات والهوية البصرية")
    st.markdown("""
    <div class='prompt-box'>
    <b>Prompt 1 (العقارات الفلاحية والأراضـي):</b><br>
    <i>"Cinematic aerial drone shot of fertile agricultural land in El Kelaa des Sraghna, lush green fields, irrigation systems, bright sunny day, professional real estate photography, 8k --ar 16:9"</i>
    </div>
    """, unsafe_allow_html=True)

elif app_mode == "🤖 الوكيل الذكي (AI Agent)":
    st.title("🤖 الوكيل الذكي المتعدد القطاعات")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if user_query := st.chat_input("اطرح سؤالك أو اطلب محتوى..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)
            
        if client:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت مساعد ذكي ومحترف لإدارة العقارات والمشاريع لعامر في قلعة السراغنة ومراكش."},
                        {"role": "user", "content": user_query}
                    ]
                )
                agent_reply = response.choices[0].message.content
            except Exception as e:
                agent_reply = f"خطأ في الاتصال: {e}"
        else:
            agent_reply = "مفتاح OpenAI غير مفعل."
            
        st.session_state.chat_history.append({"role": "assistant", "content": agent_reply})
        with st.chat_message("assistant"):
            st.write(agent_reply)

elif app_mode == "✨ استوديو توليد ومعالجة الصور":
    st.title("🎨 استوديو الرؤية بالذكاء الاصطناعي")
    tab1, tab2 = st.tabs(["✨ توليد بالبرومبت", "🛠️ تحسين الصور"])
    with tab1:
        img_prompt = st.text_input("صف المشهد:")
        if st.button("توليد الصورة"):
            if client:
                with st.spinner("جاري التوليد..."):
                    try:
                        res = client.images.generate(model="dall-e-3", prompt=img_prompt, n=1, size="1024x1024")
                        st.image(res.data[0].url, use_container_width=True)
                    except Exception as e:
                        st.error(e)
            else:
                st.error("مفتاح OpenAI غير متوفر.")
    with tab2:
        up_img = st.file_uploader("اختر صورة للتحسين", type=["jpg", "png", "jpeg"])
        if up_img:
            img = Image.open(up_img)
            st.image(img, caption="الأصلية", use_container_width=True)
            if st.button("تحسين الحدة"):
                enhanced = ImageEnhance.Sharpness(img).enhance(2.0)
                st.image(enhanced, caption="بعد التحسين", use_container_width=True)

elif app_mode == "📋 إدارة صفقات Supabase":
    st.title("📋 إدارة صفقات Supabase")
    if supabase:
        with st.form("sup_form"):
            s_title = st.text_input("عنوان الصفقة:")
            s_city = st.selectbox("المدينة:", ["قلعة السراغنة", "مراكش"])
            s_desc = st.text_area("الوصف:")
            if st.form_submit_button("إحفظ في Supabase"):
                try:
                    supabase.table("properties").insert({"title": s_title, "city": s_city, "description": s_desc}).execute()
                    st.success("تم الحفظ بنجاح!")
                except Exception as e:
                    st.error(e)
        try:
            res = supabase.table("properties").select("*").execute()
            if res.data:
                st.dataframe(pd.DataFrame(res.data), use_container_width=True)
        except:
            st.info("تأكد من إنشاء جدول properties في Supabase.")
    else:
        st.warning("إعدادات Supabase غير متوفرة في الـ Secrets.")

elif app_mode == "🛠️ الخدمات الرقمية والهندسية":
    st.title("🛠️ خدماتنا الرقمية والهندسية")
    st.write("• التصوير الفوتوغرافي الاحترافي للمشاريع والعقارات.")
    st.write("• الحملات الإعلانية الرقمية.")
    st.write("• الهندسة المعمارية والصناعية والميكانيكية.")
    st.write("• التصميم الداخلي وهندسة الديكور والتصاميم ثلاثية الأبعاد 3D.")

elif app_mode == "📞 تواصل":
    st.title("📞 تواصل مع عامر بوخدادة")
    st.success("الهاتف والواتساب المباشر: 0691897126")
    st.markdown("[محادثة مباشرة عبر الواتساب](https://wa.me/212691897126)")
