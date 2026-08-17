import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from datetime import datetime
import io

# إعداد واجهة Streamlit
st.set_page_config(page_title="Tassaout Eagle Agent", layout="wide")
st.title("🦅 Tassaout Eagle Agent - Digital Agent")

# دالة المعالجة (وكيل المعالجة)
def process_image(image_file):
    img = Image.open(image_file).convert('RGB')
    # تطبيق التحسينات
    img = img.filter(ImageFilter.SHARPEN)
    img = ImageEnhance.Contrast(img).enhance(1.2)
    img = ImageEnhance.Color(img).enhance(1.1)
    return img

# واجهة المستخدم (الرفع أو التصوير)
option = st.radio("اختر طريقة العمل:", ["رفع صورة من الهاتف", "التصوير المباشر بالكاميرا"])

if option == "التصوير المباشر بالكاميرا":
    img_file = st.camera_input("التقط صورة:")
else:
    img_file = st.file_uploader("ارفع صورة العقار:", type=['jpg', 'jpeg', 'png'])

if img_file:
    # عرض الصورة الأصلية
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(img_file, caption="الصورة الأصلية", use_container_width=True)
        
    # المعالجة
    processed_img = process_image(img_file)
    
    with col2:
        st.image(processed_img, caption="Tassaout Gold Edition", use_container_width=True)
        
    # زر التحميل
    buf = io.BytesIO()
    processed_img.save(buf, format="JPEG")
    st.download_button("تحميل الصورة المعالجة", buf.getvalue(), "tassaout_eagle.jpg", "image/jpeg")
    
    st.success("تم تحليل ومعالجة الصورة بنجاح بواسطة وكلاء تساوت!")

# تذييل الصفحة
st.markdown("---")
st.write("🦅 Tassaout Immobilière - Digital Services")
