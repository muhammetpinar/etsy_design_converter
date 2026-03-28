import streamlit as st
import os
import pandas as pd
from PIL import Image
from src.core.processor import BrandConfig, DesignProcessor
from src.utils.image_processing import (
    apply_vintage_effect,
    apply_vintage_effect2,
    apply_vintage_effect3,
    apply_retro_effect,
    calculate_hash
)

# ---------------------- Configuration ----------------------
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define Brands (DRY)
BRANDS = [
    BrandConfig("PINART", "PINART Design Kodu", "MP", apply_vintage_effect, "PINARTBackGround", "BB.png", "SB.png", "MP"),
    BrandConfig("Zeyto", "Zeyto Design Kodu", "Z", apply_vintage_effect2, "ZeytoBackGround", "BB.png", "SB.png", "ZB"),
    BrandConfig("Spring", "Spring Design Kodu", "S", apply_vintage_effect3, "SpringBackGround", "BB.png", "SB.png", "SB"),
    BrandConfig("Bosphorus", "Bosphorus Design Kodu", "B", apply_vintage_effect, "BosphBackGround", "BB.png", "SB.png", "BWB"),
    BrandConfig("Badis", "Badiş Art Design Kodu", "BA", apply_vintage_effect, "BadisBackGround", "BA.png", "BAS.png", "BAB"),
]

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="ETSY FAST IMAGE", page_icon="🎨", layout="wide")

st.title("🎨 ETSY FAST IMAGE - Professional Suite")

tab1, tab2, tab3 = st.tabs(["🖼️ Fotoğraf İşleme", "📝 SEO Prompt", "📅 Özel Günler"])

with tab1:
    st.header("Görsel Hash Değiştirici ve Mockup Oluşturucu")
    
    input_image = st.file_uploader("Girdi görselini yükle (PNG)", type=["png"], key="design_upload")
    
    # UI Inputs for Brand Codes
    st.subheader("Mağaza Tasarım Kodları")
    col_k, col_p = st.columns([1, 1])
    with col_k:
        folder_code = st.text_input("Klasör Kodu (MP_...)", "12")
    
    brand_codes = {}
    cols = st.columns(len(BRANDS))
    for i, brand in enumerate(BRANDS):
        brand_codes[brand.name] = cols[i].text_input(brand.display_title, "12")

    scale_ratio = st.slider("Ön plan ölçek oranı", 0.1, 2.0, 0.75, step=0.05)

    if st.button("🚀 İŞLEMİ BAŞLAT", use_container_width=True):
        if input_image:
            # 1. Setup Processor
            output_dir = os.path.join(SCRIPT_DIR, "outputs", f"MP_{folder_code}")
            processor = DesignProcessor(SCRIPT_DIR, output_dir)
            
            # Temporary save for hash calculation (standardized name)
            temp_input_path = os.path.join(SCRIPT_DIR, "temp_input.png")
            with open(temp_input_path, "wb") as f:
                f.write(input_image.getbuffer())
            
            img = Image.open(temp_input_path).convert("RGBA")
            
            # 2. Iterate through Brands (DRY)
            results = []
            progress_bar = st.progress(0)
            
            for i, brand in enumerate(BRANDS):
                design_code = brand_codes[brand.name]
                design_path = processor.process_brand(brand, img, design_code, scale_ratio)
                results.append({"Brand": brand.name, "Path": design_path, "MD5": calculate_hash(design_path)})
                progress_bar.progress((i + 1) / len(BRANDS))
            
            st.success(f"✅ Tüm işlemler başarıyla tamamlandı! Çıktı Klasörü: {output_dir}")
            
            # 4. Show Hashes
            st.subheader("🔎 Görsel Kimlik (Hash) Bilgileri")
            df_hash = pd.DataFrame(results)
            st.table(df_hash)
        else:
            st.warning("Lütfen önce bir görsel yükleyin!")

with tab2:
    st.header("📄 ChatGPT Hazır Prompt")
    st.markdown("""
    <div style="background-color:#f0f2f6;padding:20px;border-radius:10px;border: 1px solid #d1d5db; color: #1f2937;">
    ETSY'de dijital ürün satıyorum. Bu ürünler tshirt kupa bardak vs için digital yazdırılabilir ürünler. Format olarak png ve svg satıyorum. ETSY 2025 SEO uyumlu çok fazla satış yapmak istiyorum. Satış yapabilmek ve arttırabilmek için, sana verdiğim konu başlığıyla ilgili tag,title ve açıklama çıkarmanı istiyorum. Bundan sonra bu şekilde ilerleyebilir miyiz ? Tag içerikleri virgülle ayrılsın istiyorum ki kolayca kopyala ypıştır yapabileyim. Bu yaptıklarımın amacı etsy'de satışlarımı arttırabilmek. Dolayısıyla en çok satış yaptıracak tag-tittle ve açıklamayı vermeni istiyorum. Tek bir geniş satış yaptıracak title istiyorum. Tagler en fazla 13 tane olmalı ve satış yaptıracak tagler olmalı. Açıklama kısmında bunun instant dowload ve digital ürün olduğu geçmeli ve kısa ve öz ve açıklayıcı olmalı. Her şey ingilizce ve etsy'de en çok kullanılan anahtar kelimelerle olsun. Description'ın en üst kısmında konu başlığı olsun. En sonunda ise tagler virgülle yazılsın. title 130-140 karakter arası olsun. Tagler 13 tane olsun. Tagler 1 karakter ile 20 karakter arasında olmalı.
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.header("🇺🇸 Amerika Özel Günleri")
    
    special_days_data = {
        "ÖZEL TARİH": [
            "NEW YEARS DAY", "MARTIN LUTHER KING DAY", "PRESIDENTS DAY", "VALENTINES DAY", 
            "ST PATRICKS DAY", "EASTER DAY", "MOTHERS DAY", "MEMORIAL DAY", 
            "NATIONAL INDEPENDENCE DAY", "FATHERS DAY", "4TH OF JULY", "LABOR DAY", 
            "COLUMBUS DAY", "HALLOWEEN", "VETERANS DAY", "THANKSGIVING", "CHRISTMAS"
        ],
        "TARİH": [
            "1 OCAK", "17 OCAK", "21 ŞUBAT", "14 ŞUBAT", "17 MART", "17 NİSAN", "8 MAYIS", 
            "30 MAYIS", "19 HAZİRAN", "19 HAZİRAN", "4 TEMMUZ", "5 EYLÜL", "10 EKİM", 
            "31 EKİM", "11 KASIM", "24 KASIM", "25 ARALIK"
        ]
    }
    df = pd.DataFrame(special_days_data)
    st.dataframe(df, use_container_width=True)

st.divider()
st.caption("🔗 Developed by Muhammet Pınar | Powered by Streamlit & AI")
