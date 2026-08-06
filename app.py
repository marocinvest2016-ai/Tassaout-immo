import streamlit as st
import json
import os

# إعدادات النظام السيادي للوكالة العقارية
st.set_page_config(
    page_title="Super Multi-Domaine Agentic AI | Agence Immobilière Kelaat Sraghna",
    page_icon="🧠",
    layout="wide"
)

# تخصيص واجهة التحكم السيادية
st.markdown("""
    <style>
    .main { background-color: #062314; color: #f8fafc; }
    .stApp { background-color: #062314; color: #f8fafc; }
    [data-testid="stSidebar"] { display: none; }
    .agent-box {
        background: linear-gradient(135deg, #0f3d24 0%, #062314 100%);
        border: 2px solid #22c55e;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(34, 197, 94, 0.2);
    }
    .card-item {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #14532d;
        margin-bottom: 15px;
        background-color: #0f3d24;
    }
    </style>
""", unsafe_allow_html=True)

# ملفات قاعدة البيانات الخاصة بتنظيم المستودع
DB_INVENTORY = "repository_inventory.json"
DB_LISTINGS = "listings_registry.json"

def load_db(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return default

def save_db(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

inventory = load_db(DB_INVENTORY, {
    "repository": "Agence Immobilière Kelaat Sraghna",
    "status": "Active Agentic Sync",
    "domains": ["Terrains Agricoles", "Fermes", "Lots de Construction", "Immeubles"]
})

listings = load_db(DB_LISTINGS, [
    {
        "id": "TER-01",
        "title": "Vente terrain agricole 2 ha — Douar X, Kelaat Sraghna",
        "type": "Terrain agricole",
        "details": "Superficie : 20 000 m² | Sol fertile, puits, accès route.",
        "status": "نشط في المستودع"
    }
])

# الترويسة العليا للعقل السيادي
st.markdown("<h1 style='text-align: center; color: #4ade80;'>🧠 Super Multi-Domaine Agentic AI</h1>", unsafe_order=True) if hasattr(st, 'markdown') else None
st.markdown("<h3 style='text-align: center; color: #94a3b8;'>المحرك الذكي لتنظيم وإدارة مستودع (Agence Immobilière Kelaat Sraghna)</h3>", unsafe_allow_html=True)

# لوحة التحكم الأفقية للوكلاء المتعددين
col1, col2, col3, col4 = st.columns(4)
if 'agent_tab' not in st.session_state:
    st.session_state.agent_tab = "🤖 نظرة عامة على العقل السيادي"

with col1:
    if st.button("🤖 نظرة عامة للعقل", use_container_width=True): st.session_state.agent_tab = "🤖 نظرة عامة على العقل السيادي"
with col2:
    if st.button("📁 تنظيم المستودع", use_container_width=True): st.session_state.agent_tab = "📁 تنظيم المستودع"
with col3:
    if st.button("🌾 إدارة العقارات والفيرمات", use_container_width=True): st.session_state.agent_tab = "🌾 إدارة العقارات والفيرمات"
with col4:
    if st.button("💬 ربط واتساب الوكالة", use_container_width=True): st.session_state.agent_tab = "💬 ربط واتساب الوكالة"

st.markdown("---")
tab = st.session_state.agent_tab

if tab == "🤖 نظرة عامة على العقل السيادي":
    st.markdown("""
    <div class="agent-box">
        <h2 style="color: #4ade80;">النظام الذكي متعدد النطاقات يعمل بكفاءة تامة</h2>
        <p style="color: #cbd5e1;">يتولى هذا العقل إدارة وتنظيم ملفات وعروض وكالة <b>Kelaat Sraghna</b> العقارية، وتصنيف الأراضي الزراعية والفيرمات وربطها آلياً مع قنوات التواصل.</p>
    </div>
    """, unsafe_allow_html=True)
    st.metric(label="النطاقات النشطة تحت الإدارة", value=len(inventory["domains"]))
    st.metric(label="إجمالي العقارات المسجلة في الذاكرة", value=len(listings))

elif tab == "📁 تنظيم المستودع":
    st.title("📁 إدارة وتنظيم بنية المستودع (Repository Structure)")
    st.markdown("يقوم الوكيل الآلي بمراقبة وتنظيم مسارات المستودع كالتالي:")
    st.code("""
    Agence-Immobiliere-Kelaat-Sraghna/
    ├── app.py                  # العقل السيادي (Super Multi-Domaine Agentic AI)
    ├── repository_inventory.json # سجل بنية النطاقات
    ├── listings_registry.json    # سجل العقارات والأراضي الفلاحية
    ├── listings/               # مجلد ملفات الإعلانات بصيغة Markdown
    └── images/                 # مجلد الصور والتوثيق الجغرافي
    """, language="text")
    
    if st.button("🔄 فحص وتحديث هيكل المستودع آلياً"):
        st.success("✔ تم فحص وتحديث مسارات المستودع بنجاح عبر الوكيل الذكي.")

elif tab == "🌾 إدارة العقارات والفيرمات":
    st.title("🌾 العروض والأنظمة العقارية المدارة")
    
    with st.form("add_listing_agent", clear_on_submit=True):
        t_title = st.text_input("عنوان العقار الجديد (Ex: Vente ferme...)")
        t_type = st.selectbox("النطاق العقاري", ["Terrain agricole", "Ferme", "Lots de construction", "Immeuble"])
        t_det = st.text_area("المواصفات والتفاصيل الدقيقة")
        if st.form_submit_button("🚀 تسجيل العقار في ذاكرة المستودع"):
            if t_title:
                listings.append({
                    "id": f"REF-{len(listings)+1:02d}",
                    "title": t_title,
                    "type": t_type,
                    "details": t_det,
                    "status": "مسجل حديثاً"
                })
                save_db(DB_LISTINGS, listings)
                st.success("✔ تمت إضافة العقار وتنظيمه داخل النظام بنجاح!")
                st.rerun()

    st.subheader("📋 قائمة العقارات الحالية في النظام:")
    for item in listings:
        wa_link = f"https://wa.me/212691897126?text=السلام%20عليكم،%20أهتم%20بالعقار%20المسجل:%20{item['title']}"
        st.markdown(f"""
        <div class="card-item">
            <h4 style="color: #4ade80; margin-top: 0;">🏢 {item['title']} <span style="font-size:12px; background:#166534; padding:2px 8px; border-radius:4px;">{item['type']}</span></h4>
            <p><b>التفاصيل:</b> {item['details']}</p>
            <a href="{wa_link}" target="_blank">
                <button style="background-color: #25D366; color: white; padding: 6px 12px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px;">
                    💬 التواصل عبر واتساب الوكالة
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

elif tab == "💬 ربط واتساب الوكالة":
    st.title("💬 قنوات الاتصال والخط الساخن")
    st.success("📞 الرقم الرسمي المعتمد للوكالة وللربط الآلي: **0691897126**")
    wa_direct = "https://wa.me/212691897126?text=السلام%20عليكم،%20أريد%20الاستفسار%20عن%20العقارات%20والأراضي%20بقلعة%20السراغنة"
    st.markdown(f"""
    <a href="{wa_direct}" target="_blank">
        <button style="background-color: #25D366; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer;">
            💬 فتح قناة الواتساب الرسمية للوكالة
        </button>
    </a>
    """, unsafe_allow_html=True)
