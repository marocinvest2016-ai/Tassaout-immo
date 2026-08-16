import streamlit as st
import json
import os
import glob

st.set_page_config(page_title="Tassaout Immo & Media", page_icon="🏢", layout="wide")

# التصميم الموحد
st.markdown("""
    <style>
    .main { background-color: #062314; color: #f8fafc; }
    .prop-card { padding: 20px; border-radius: 12px; border: 1px solid #14532d; margin-bottom: 20px; background-color: #0f3d24; }
    .badge-cat { background-color: #166534; color: #4ade80; padding: 4px 10px; border-radius: 6px; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

# دالة تحميل الخدمات
def load_services():
    try:
        with open("services_tassaout_sraghna.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"services": []}

# التبديل بين الصفحات
if 'nav_mode' not in st.session_state: st.session_state.nav_mode = "عقارات"

col1, col2, col3 = st.columns(3)
if col1.button("🏠 العقارات", use_container_width=True): st.session_state.nav_mode = "عقارات"
if col2.button("🛠️ الخدمات", use_container_width=True): st.session_state.nav_mode = "خدمات"
if col3.button("📞 اتصل بنا", use_container_width=True): st.session_state.nav_mode = "اتصال"

# محتوى الصفحات
if st.session_state.nav_mode == "عقارات":
    st.title("🏢 المحفظة العقارية")
    st.write("استعراض العقارات المتاحة (يمكنك إضافة ملفات في مجلد listings)")
    # هنا سيتم عرض العقارات من كودك السابق...

elif st.session_state.nav_mode == "خدمات":
    st.title("🛠️ خدماتنا الرقمية والهندسية")
    data = load_services()
    for s in data.get("services", []):
        with st.expander(f"✨ {s['الخدمة']}"):
            st.write(s['الوصف'])

elif st.session_state.nav_mode == "اتصال":
    st.title("📞 تواصل مع عامر بوخدادة")
    st.success("الهاتف/واتساب: 0691897126")
    st.markdown("[اضغط هنا للمحادثة المباشرة](https://wa.me/212691897126)")
