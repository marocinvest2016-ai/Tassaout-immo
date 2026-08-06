import streamlit as st
import json
import os
import glob

# إعدادات الصفحة والتصميم السيادي للوكالة العقارية
st.set_page_config(
    page_title="Tassaout Immo | Agence Immobilière Kelaat Sraghna",
    page_icon="🏢",
    layout="wide"
)

# تخصيص التصميم والواجهة
st.markdown("""
    <style>
    .main { background-color: #062314; color: #f8fafc; }
    .stApp { background-color: #062314; color: #f8fafc; }
    [data-testid="stSidebar"] { display: none; }
    .hero-box {
        background: linear-gradient(135deg, #0f3d24 0%, #062314 100%);
        border: 2px solid #22c55e;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
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
    .badge-cat {
        background-color: #166534;
        color: #4ade80;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# مسارات البيانات
PROPERTIES_JSON = "properties_master.json"
LISTINGS_DIR = "listings"

def load_properties_from_repo():
    """قراءة العقارات تلقائياً من ملفات المستودع (JSON أو مجلد listings)"""
    properties_list = []
    
    # 1. القراءة من ملف JSON الشامل إن وجد
    if os.path.exists(PROPERTIES_JSON):
        try:
            with open(PROPERTIES_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "listings" in data:
                    return data["listings"]
                elif isinstance(data, list):
                    return data
        except:
            pass

    # 2. القراءة الديناميكية التلقائية من مجلد ملفات الـ Markdown (listings/)
    if os.path.exists(LISTINGS_DIR):
        md_files = glob.glob(os.path.join(LISTINGS_DIR, "*.md"))
        for file_path in md_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.splitlines()
                    title = lines[0].replace("#", "").strip() if lines else "عقار بدون عنوان"
                    
                    # استخراج البيانات الأساسية من الملف
                    prop_type = "عام"
                    surface = "غير محددة"
                    price = "حسب الاتفاق"
                    location = "قلعة السراغنة"
                    
                    for line in lines:
                        if "Type" in line: prop_type = line.split(":")[-1].strip()
                        if "Superficie" in line: surface = line.split(":")[-1].strip()
                        if "Prix" in line: price = line.split(":")[-1].strip()
                        if "Localisation" in line: location = line.split(":")[-1].strip()
                    
                    properties_list.append({
                        "ref": os.path.basename(file_path),
                        "title": title,
                        "category": prop_type,
                        "surface": surface,
                        "location": location,
                        "price": price,
                        "details": content[:250] + "..."
                    })
            except:
                continue

    # بيانات افتراضية في حال عدم وجود ملفات لتجنب الفراغ
    if not properties_list:
        properties_list = [
            {"ref": "AGR-01", "title": "Vente terrain agricole 2 ha", "category": "العقاري الفلاحي", "surface": "20 000 m²", "location": "قلعة السراغنة", "price": "450 000 MAD", "details": "أرض فلاحية مع بئر ومجهزة بالكامل."},
            {"ref": "IND-01", "title": "Terrain Industriel 3000 m²", "category": "العقاري الصناعي والتجاري", "surface": "3 000 m²", "location": "المنطقة الصناعية", "price": "2 200 000 MAD", "details": "قطعة أرضية مخصصة للمستودعات والمصانع."},
            {"ref": "PRO-01", "title": "Bureau professionnel 120 m²", "category": "العقاري المهني", "surface": "120 m²", "location": "شارع محمد الخامس", "price": "750 000 MAD", "details": "مكتب تجاري مهني في موقع استراتيجي."},
            {"ref": "INV-01", "title": "Lot de terrain R+4 Al Hoda", "category": "العقاري الاستثماري", "surface": "400 m²", "location": "تجزئة الهدى", "price": "1 100 000 MAD", "details": "بقعة أرضية استثمارية لبناء عمارة."}
        ]
    return properties_list

all_properties = load_properties_from_repo()

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: #4ade80; margin-bottom: 0;'>🏢 Tassaout Immo — Agence Immobilière</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 20px;'>النظام الذكي لإدارة وعرض المحفظة العقارية بقلعة السراغنة (فلاحي، صناعي، مهني، واستثمار)</p>", unsafe_allow_html=True)

# شريط التنقل العلوي
nav1, nav2, nav3 = st.columns(3)
if 'nav_mode' not in st.session_state:
    st.session_state.nav_mode = "🌾 تصفح والبحث في العقارات"

with nav1:
    if st.button("🌾 تصفح العقارات", use_container_width=True): st.session_state.nav_mode = "🌾 تصفح والبحث في العقارات"
with nav2:
    if st.button("📊 إحصائيات المحفظة", use_container_width=True): st.session_state.nav_mode = "📊 إحصائيات المحفظة"
with nav3:
    if st.button("💬 اتصل بالوكالة", use_container_width=True): st.session_state.nav_mode = "💬 اتصل بالوكالة"

st.markdown("---")
mode = st.session_state.nav_mode

if mode == "🌾 تصفح والبحث في العقارات":
    st.title("🔍 البحث والفرز المتقدم للمحفظة العقارية")
    
    # خيارات الفرز والبحث المتقدم
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        search_query = st.text_input("بحث بالكلمة المفتاحية أو الموقع:", placeholder="مثال: زراعة، المنطقة الصناعية، الهدى...")
    with col_s2:
        category_filter = st.selectbox("الفرز حسب القطاع النوعي:", [
            "الكل", 
            "العقاري الفلاحي", 
            "العقاري الصناعي والتجاري", 
            "العقاري المهني", 
            "العقاري الاستثماري",
            "Terrain agricole",
            "Industriel et Commercial",
            "Professionnel et Bureaux",
            "Investissement et Résidentiel"
        ])

    # تطبيق الفلترة والبحث
    filtered_props = all_properties
    if category_filter != "الكل":
        filtered_props = [p for p in filtered_props if category_filter.lower() in p.get("category", "").lower() or category_filter in p.get("category", "")]
    
    if search_query:
        filtered_props = [p for p in filtered_props if search_query.lower() in str(p.values()).lower()]

    st.markdown(f"<p style='color: #4ade80;'>عدد العقارات المطابقة للبحث: <b>{len(filtered_props)}</b></p>", unsafe_allow_html=True)

    # عرض العقارات بطاقات منسقة
    for prop in filtered_props:
        wa_text = f"السلام عليكم، مهتم بالعقار: {prop.get('title')} ({prop.get('ref', '')})"
        wa_url = f"https://wa.me/212691897126?text={wa_text.replace(' ', '%20')}"
        
        st.markdown(f"""
        <div class="prop-card">
            <h3 style="color: #4ade80; margin-top: 0;">🏢 {prop.get('title')} <span class="badge-cat">{prop.get('category')}</span></h3>
            <p><b>📐 المساحة:</b> {prop.get('surface')} | <b>📍 الموقع:</b> {prop.get('location')}</p>
            <p><b>💰 السعر:</b> <span style="color: #facc15; font-weight: bold;">{prop.get('price')}</span></p>
            <p style="color: #cbd5e1; font-size: 14px;">{prop.get('details', '')}</p>
            <a href="{wa_url}" target="_blank">
                <button style="background-color: #25D366; color: white; padding: 8px 16px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;">
                    💬 التواصل عبر واتساب الوكالة
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

elif mode == "📊 إحصائيات المحفظة":
    st.title("📊 لوحة مؤشرات المحفظة العقارية لـ Tassaout Immo")
    st.metric(label="إجمالي العقارات المسجلة في المستودع", value=len(all_properties))
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.info("🌾 القطاع الأكثر طلباً: الأراضي الفلاحية والفيرمات بقلعة السراغنة والناحية.")
    with col_m2:
        st.success("🏗️ القطاع الاستثماري الصناعي: متوافق مع معايير الطرق الرئيسية والمناطق المهنية.")

elif mode == "💬 اتصل بالوكالة":
    st.title("💬 قنوات الاتصال والخط الساخن - Tassaout Immo")
    st.success("📞 الهاتف الرسمي المعتمد للوكالة: **0691897126**")
    st.markdown("""
    * **النشاط الرئيسي:** بيع الأراضي الزراعية، الفيرمات، البقع الصناعية، المحلات المهنية، والعقارات الاستثمارية.
    * **منطقة التدخل:** قلعة السراغنة، مراكش، والضواحي والقيادات المجاورة.
    """)
    direct_wa = "https://wa.me/212691897126?text=السلام%20عليكم،%20أريد%20الاستفسار%20عن%20العقارات%20المتاحة%20لدى%20Tassaout%20Immo"
    st.markdown(f"""
    <a href="{direct_wa}" target="_blank">
        <button style="background-color: #25D366; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer;">
            💬 فتح محادثة واتساب المباشرة
        </button>
    </a>
    """, unsafe_allow_html=True)
