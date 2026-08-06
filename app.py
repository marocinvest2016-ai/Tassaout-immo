import streamlit as st
import json
import os

# إعدادات الصفحة والتصميم العام (عرض واسع)
st.set_page_config(
    page_title="Tassaout Immo | وكالة تساوت العقارية", 
    page_icon="🏢", 
    layout="wide"
)

# تخصيص التصميم عبر CSS: خلفية خضراء فاخرة مستوحاة من الطابع الزراعي والعقاري
st.markdown("""
    <style>
    .main {
        background-color: #062314;
    }
    .stApp {
        background-color: #062314;
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
    .hero-box {
        background: linear-gradient(135deg, #0f3d24 0%, #062314 100%);
        border: 2px solid #22c55e;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(34, 197, 94, 0.2);
    }
    .prop-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #14532d;
        margin-bottom: 20px;
        background-color: #0f3d24;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .badge-active {
        background-color: #166534;
        color: #4ade80;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ملفات تخزين البيانات
PROPERTIES_FILE = "properties.json"
CLIENTS_FILE = "client_requests.json"

def load_data(file_path, default_data):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return default_data

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# العروض العقارية الافتراضية الخاصة بـ Tassaout Immo
properties = load_data(PROPERTIES_FILE, [
    {
        "title": "Vente terrain agricole 2 ha — Douar X, Kelaat Sraghna",
        "category": "Terrain agricole",
        "details": "Superficie : 2 hectares (20 000 m²) | Sol fertile, puits, idéal pour oliveraie.",
        "phone": "0691897126"
    },
    {
        "title": "بقع سكنية وتجارية في تجزئة الهدى",
        "category": "Lots de construction",
        "details": "مساحات من 80م² إلى 240م² مع موقع استراتيجي وتراخيص جاهزة.",
        "phone": "0691897126"
    }
])

client_requests = load_data(CLIENTS_FILE, [])

# العنوان الرئيسي للوكالة
st.markdown("<h1 style='text-align: center; color: #4ade80; margin-bottom: 5px;'>🏢 Tassaout Immo — Agence Immobilière</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 20px;'>الوكالة العقارية المتخصصة بقلعة السراغنة والناحية (أراضي، فيرمات، بقع ومنازل)</p>", unsafe_allow_html=True)

# لوحة التنقل الأفقية
nav1, nav2, nav3, nav4, nav5 = st.columns(5)
if 'page' not in st.session_state:
    st.session_state.page = "🏠 الرئيسية"

with nav1:
    if st.button("🏠 الرئيسية", use_container_width=True): st.session_state.page = "🏠 الرئيسية"
with nav2:
    if st.button("🌾 عروض العقارات", use_container_width=True): st.session_state.page = "🌾 عروض العقارات"
with nav3:
    if st.button("📝 طلبات الزبناء", use_container_width=True): st.session_state.page = "📝 طلبات الزبناء"
with nav4:
    if st.button("➕ إضافة عقار", use_container_width=True): st.session_state.page = "➕ إضافة عقار"
with nav5:
    if st.button("💬 اتصل بنا", use_container_width=True): st.session_state.page = "💬 اتصل بنا"

st.markdown("---")
page = st.session_state.page

if page == "🏠 الرئيسية":
    st.markdown("""
    <div class="hero-box">
        <h1 style="color: #4ade80;">bienvenue chez Tassaout Immo</h1>
        <p style="color: #cbd5e1; font-size: 1.1rem;">نرافقكم في جميع معاملاتكم العقارية بقلعة السراغنة: بيع وشراء الأراضي الزراعية، الفيرمات، البقع، والعقارات السكنية بضمان وشفافية تامّة.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="📊 العقارات النشطة", value=len(properties))
    with col2:
        st.metric(label="📝 طلبات الزبناء المسجلة", value=len(client_requests))

elif page == "🌾 عروض العقارات":
    st.title("🌾 قائمة العقارات والأراضي المتاحة")
    for prop in properties:
        wa_url = f"https://wa.me/212691897126?text=السلام%20عليكم،%20مهتم%20بالعقار:%20{prop['title']}"
        st.markdown(f"""
        <div class="prop-card">
            <h3 style="color: #4ade80; margin-top: 0;">🏢 {prop['title']}</h3>
            <p><b>🏷️ Type:</b> {prop['category']}</p>
            <p><b>📝 Détails:</b> {prop['details']}</p>
            <a href="{wa_url}" target="_blank">
                <button style="background-color: #25D366; color: white; padding: 8px 16px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;">💬 Contact WhatsApp</button>
            </a>
        </div>
        """, unsafe_allow_html=True)

elif page == "📝 طلبات الزبناء":
    st.title("📝 الشاشة التفاعلية لطلبات وعروض الزبناء")
    with st.form("client_form", clear_on_submit=True):
        c_name = st.text_input("الاسم الكامل / Nom complet")
        c_phone = st.text_input("رقم الهاتف / Téléphone", value="06")
        c_type = st.selectbox("نوع الطلب", ["بحث عن أرض زراعية", "بحث عن بقعة سكنية", "عرض عقار للبيع", "بحث عن فيرمة / ضيعة"])
        c_details = st.text_area("تفاصيل الطلب (المساحة، الميزانية، الموقع...)")
        
        if st.form_submit_button("إرسال الطلب للوكالة"):
            if c_name and c_details:
                client_requests.append({"name": c_name, "phone": c_phone, "type": c_type, "details": c_details})
                save_data(CLIENTS_FILE, client_requests)
                st.success("تم إرسال طلبك بنجاح!")
                st.rerun()
            else:
                st.error("المرجو ملء الخانات الضرورية.")
                
    st.subheader("📋 قائمة الطلبات الواردة")
    for req in client_requests:
        st.markdown(f"""
        <div class="prop-card">
            <h4 style="color: #4ade80; margin-top: 0;">👤 {req['name']} <span class="badge-active">{req['type']}</span></h4>
            <p><b>التفاصيل:</b> {req['details']}</p>
            <p style="color: #cbd5e1;"><b>الهاتف:</b> {req['phone']}</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "➕ إضافة عقار":
    st.title("➕ نشر عقار جديد (خاص بالإدارة)")
    with st.form("add_prop", clear_on_submit=True):
        p_title = st.text_input("عنوان العقار (Ex: Vente terrain...)")
        p_cat = st.selectbox("التصنيف", ["Terrain agricole", "Lots de construction", "Ferme", "Maison / Immeuble"])
        p_det = st.text_area("المواصفات والتفاصيل الكاملة")
        if st.form_submit_button("حفظ ونشر العقار"):
            if p_title:
                properties.append({"title": p_title, "category": p_cat, "details": p_det, "phone": "0691897126"})
                save_data(PROPERTIES_FILE, properties)
                st.success("تم إضافة العقار بنجاح!")
                st.rerun()

elif page == "💬 اتصل بنا":
    st.title("💬 التواصل والخط الساخن - Tassaout Immo")
    st.success("📞 الهاتف الرسمي: **0691897126**")
    st.markdown("""
    * **Spécialité:** Vente de terrains agricoles, fermes, et lots de construction.
    * **Zone:** Kelaat Sraghna et environs.
    """)
    wa_link = "https://wa.me/212691897126?text=السلام%20عليكم،%20أريد%20الاستفسار%20حول%20خدمات%20Tassaout%20Immo"
    st.markdown(f"""
    <a href="{wa_link}" target="_blank">
        <button style="background-color: #25D366; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer;">
            💬 التواصل المباشر عبر واتساب
        </button>
    </a>
    """, unsafe_allow_html=True)
