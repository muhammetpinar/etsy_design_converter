import streamlit as st
import os
import shutil
import time
import sys
import pandas as pd
from PIL import Image

# ---------------------- Path Management ----------------------
# Resolve 'src' module whether running as a script or as a bundled EXE
def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Injects the parent directory into sys.path to resolve 'src' modules
# This fixes ModuleNotFoundError when running via 'streamlit run src/app.py'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from src.core.processor import BrandConfig, DesignProcessor
from src.utils.image_processing import (
    apply_vintage_effect,
    apply_vintage_effect2,
    apply_vintage_effect3,
    calculate_hash
)

# ---------------------- Configuration ----------------------
SCRIPT_DIR = PARENT_DIR  # Root of the project workspace

# Define Brands (DRY)
BRANDS = [
    BrandConfig("PINART", "PINART Design Kodu", "MP", apply_vintage_effect, "PINARTBackGround", "BB.png", "SB.png", "MP"),
    BrandConfig("Zeyto", "Zeyto Design Kodu", "Z", apply_vintage_effect2, "ZeytoBackGround", "BB.png", "SB.png", "ZB"),
    BrandConfig("Spring", "Spring Design Kodu", "S", apply_vintage_effect3, "SpringBackGround", "BB.png", "SB.png", "SB"),
    BrandConfig("Bosphorus", "Bosphorus Design Kodu", "B", apply_vintage_effect, "BosphBackGround", "BB.png", "SB.png", "BWB"),
    BrandConfig("Badis", "Badiş Art Design Kodu", "BA", apply_vintage_effect, "BadisBackGround", "BA.png", "BAS.png", "BAB"),
]

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="ETSY FAST IMAGE Pro", page_icon="🎨", layout="wide")

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Gradient animated title */
    .animated-title {
        background: linear-gradient(-45deg, #ff4b2b, #ff8c00, #ff4b2b, #8a2be2);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 30px;
        padding-top: 20px;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphism Card Style */
    .stCard {
        background: rgba(26, 28, 36, 0.6);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Primary Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #ff4b2b, #ff8c00);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 4rem;
        width: 100%;
        margin-top: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02) translateY(-3px);
        box-shadow: 0 10px 25px rgba(255, 75, 43, 0.5);
        color: white;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(26, 28, 36, 0.4);
        border-radius: 10px 10px 0px 0px;
        padding: 10px 25px;
        font-weight: 700;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff8c00 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="animated-title">🎨 ETSY FAST IMAGE PRO</h1>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🚀 DİJİTAL ATÖLYE", "🎨 DİNAMİK MOCKUP", "📝 SEO SİHİRBAZI", "🇺🇸 ÖZEL GÜNLER"])

with tab1:
    col_l, col_r = st.columns([1, 1.4], gap="large")
    
    with col_l:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("📤 Tasarımı Yükle")
        input_image = st.file_uploader("Görselini buraya bırak (PNG)", type=["png"], key="design_upload")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("⚙️ İşlem Parametreleri")
        folder_code = st.text_input("📁 Klasör Kodu", value="12")
        scale_ratio = st.slider("📏 Tasarım Ölçeği", 0.1, 2.0, 0.75, step=0.05)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("🏷️ Mağaza Kodları")
        brand_codes = {}
        b_cols = st.columns(2)
        for i, brand in enumerate(BRANDS):
            col_idx = i % 2
            brand_codes[brand.name] = b_cols[col_idx].text_input(f"🆔 {brand.name}", "12")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 TASARIMLARI VE MOCKUPLARI ÜRET", width="stretch"):
        if input_image:
            with st.status("💎 Masterpiece işleniyor...", expanded=True) as status:
                output_dir = os.path.join(SCRIPT_DIR, "outputs", f"MP_{folder_code}")
                processor = DesignProcessor(SCRIPT_DIR, output_dir)
                
                temp_input_path = os.path.join(SCRIPT_DIR, "temp_input.png")
                with open(temp_input_path, "wb") as f:
                    f.write(input_image.getbuffer())
                
                img = Image.open(temp_input_path).convert("RGBA")
                
                results = []
                progress_bar = st.progress(0)
                
                for i, brand in enumerate(BRANDS):
                    d_code = brand_codes[brand.name]
                    status.update(label=f"🎨 {brand.name} varyasyonları oluşturuluyor...")
                    design_path = processor.process_brand(brand, img, d_code, scale_ratio)
                    results.append({"Marka": brand.name, "Dosya": os.path.basename(design_path), "Hash": calculate_hash(design_path)})
                    progress_bar.progress((i + 1) / len(BRANDS))
                
                status.update(label="✅ Tüm süreç tamamlandı!", state="complete", expanded=False)
            
            st.success(f"📂 Çıktılar Kaydedildi: `{output_dir}` (Sunucu Klasörü)")
            
            # Create ZIP for download (Unique name with timestamp)
            timestamp = int(time.time())
            zip_filename = f"MP_{folder_code}_{timestamp}"
            zip_full_path = os.path.join(SCRIPT_DIR, zip_filename)
            shutil.make_archive(zip_full_path, 'zip', output_dir)
            
            with open(f"{zip_full_path}.zip", "rb") as f:
                st.download_button(
                    label="🎁 TÜM TASARIMLARI ZIP OLARAK İNDİR",
                    data=f,
                    file_name=f"MP_{folder_code}_Tasarimlar.zip",
                    mime="application/zip",
                    width="stretch"
                )

            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            st.subheader("🔎 Dijital Kimlik (Hash) Raporu")
            st.dataframe(pd.DataFrame(results), width="stretch", hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("❗ Lütfen önce bir tasarım görseli yükleyin!")

with tab2:
    col_dl, col_dr = st.columns([1, 1], gap="large")
    
    with col_dl:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("📤 Görselleri Yükle")
        dyn_name = st.text_input("📝 Tasarım/Dosya İsmi", placeholder="Örn: My_Design")
        dyn_design = st.file_uploader("🎨 Tasarımını Yükle (PNG)", type=["png"], key="dyn_design")
        st.divider()
        dyn_bg_1 = st.file_uploader("🖼️ Arka Plan 1 Yükle", type=["png", "jpg", "jpeg"], key="dyn_bg_1")
        dyn_bg_2 = st.file_uploader("🖼️ Arka Plan 2 Yükle", type=["png", "jpg", "jpeg"], key="dyn_bg_2")
        dyn_scale = st.slider("📏 Yerleşim Ölçeği", 0.1, 2.0, 0.75, step=0.05, key="dyn_scale")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("✨ DİNAMİK MOCKUP ÜRET", use_container_width=True):
            if dyn_design and (dyn_bg_1 or dyn_bg_2) and dyn_name:
                with st.spinner("⏳ Görseller harmanlanıyor..."):
                    # Process in memory
                    from src.utils.image_processing import overlay_image, apply_hash_breaker, calculate_hash
                    
                    # 1. Prepare output folder
                    output_dir = os.path.join(SCRIPT_DIR, "outputs", f"{dyn_name}")
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # 2. Process original design (Hash breaker)
                    fg_img = Image.open(dyn_design).convert("RGBA")
                    modified_fg = apply_hash_breaker(fg_img)
                    
                    design_output_path = os.path.join(output_dir, f"{dyn_name}_original.png")
                    modified_fg.save(design_output_path)
                    
                    # 3. Store results in session state
                    st.session_state.dyn_results_list = []
                    st.session_state.dyn_results_list.append({
                        "type": "🚀 Orijinal Tasarım (Hash Değişti)",
                        "path": design_output_path
                    })
                    
                    # 4. Generate Mockups
                    bgs = [dyn_bg_1, dyn_bg_2]
                    for idx, bg in enumerate(bgs):
                        if bg is not None:
                            out_name = f"{dyn_name}_mockup_{idx+1}.png"
                            output_file = os.path.join(output_dir, out_name)
                            
                            success = overlay_image(modified_fg, bg, output_file, dyn_scale)
                            if success:
                                st.session_state.dyn_results_list.append({
                                    "type": f"🖼️ Mockup {idx+1}",
                                    "path": output_file
                                })
                    
                    # 5. Create ZIP of the entire folder
                    zip_path = os.path.join(SCRIPT_DIR, f"{dyn_name}")
                    shutil.make_archive(zip_path, 'zip', output_dir)
                    st.session_state.dyn_zip = f"{zip_path}.zip"
                    
                    st.balloons()
            else:
                st.error("❗ Lütfen İsim, Tasarım ve en az 1 Arka Plan yükleyin!")

    with col_dr:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("🖼️ Önizleme ve İndirme")
        
        if "dyn_results_list" in st.session_state and st.session_state.dyn_results_list:
            # ZIP Download Button at the top
            if "dyn_zip" in st.session_state and os.path.exists(st.session_state.dyn_zip):
                with open(st.session_state.dyn_zip, "rb") as f:
                    st.download_button(
                        label="🎁 TÜMÜNÜ ZIP OLARAK İNDİR",
                        data=f,
                        file_name=f"{dyn_name}_Tum_Dosyalar.zip",
                        mime="application/zip",
                        use_container_width=True,
                        type="primary"
                    )
                st.divider()

            # Preview individual results
            for res in st.session_state.dyn_results_list:
                res_path = res["path"]
                if os.path.exists(res_path):
                    res_img = Image.open(res_path)
                    st.image(res_img, caption=res["type"], use_container_width=True)
                    
                    with open(res_path, "rb") as f:
                        st.download_button(
                            label=f"💾 {res['type']} Dosyasını İndir",
                            data=f,
                            file_name=os.path.basename(res_path),
                            mime="image/png",
                            key=f"dl_{res_path}",
                            use_container_width=True
                        )
                    st.divider()
        else:
            st.info("💡 Sol taraftan görselleri yükleyip 'Üret' butonuna bastığınızda sonuçlar burada belirecektir.")
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.header("📄 ChatGPT Hazır Prompt")
    st.code("""ETSY'de dijital ürün satıyorum. Bu ürünler tshirt kupa bardak vs için digital yazdırılabilir ürünler. Format olarak png ve svg satıyorum. ETSY 2025 SEO uyumlu çok fazla satış yapmak istiyorum. Satış yapabilmek ve arttırabilmek için, sana verdiğim konu başlığıyla ilgili tag,title ve açıklama çıkarmanı istiyorum. Bundan sonra bu şekilde ilerleyebilir miyiz ? Tag içerikleri virgülle ayrılsın istiyorum ki kolayca kopyala ypıştır yapabileyim. Bu yaptıklarımın amacı etsy'de satışlarımı arttırabilmek. Dolayısıyla en çok satış yaptıracak tag-tittle ve açıklamayı vermeni istiyorum. Tek bir geniş satış yaptıracak title istiyorum. Tagler en fazla 13 tane olmalı ve satış yaptıracak tagler olmalı. Açıklama kısmında bunun instant dowload ve digital ürün olduğu geçmeli ve kısa ve öz ve açıklayıcı olmalı. Her şey ingilizce ve etsy'de en çok kullanılan anahtar kelimelerle olsun. Description'ın en üst kısmında konu başlığı olsun. En sonunda ise tagler virgülle yazılsın. title 130-140 karakter arası olsun. Tagler 13 tane olsun. Tagler 1 karakter ile 20 karakter arasında olmalı.""", language="text")
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.header("🇺🇸 Amerika Özel Günleri")
    
    special_days_data = {
        "ETKİNLİK": ["NEW YEARS DAY", "MARTIN LUTHER KING DAY", "PRESIDENTS DAY", "VALENTINES DAY", "ST PATRICKS DAY", "EASTER DAY", "MOTHERS DAY", "MEMORIAL DAY", "NATIONAL INDEPENDENCE DAY", "FATHERS DAY", "4TH OF JULY", "LABOR DAY", "COLUMBUS DAY", "HALLOWEEN", "VETERANS DAY", "THANKSGIVING", "CHRISTMAS"],
        "TARİH": ["1 OCAK", "17 OCAK", "21 ŞUBAT", "14 ŞUBAT", "17 MART", "17 NİSAN", "8 MAYIS", "30 MAYIS", "19 HAZİRAN", "19 HAZİRAN", "4 TEMMUZ", "5 EYLÜL", "10 EKİM", "31 EKİM", "11 KASIM", "24 KASIM", "25 ARALIK"]
    }
    st.dataframe(pd.DataFrame(special_days_data), width="stretch", hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.3); font-size:0.8rem;">💎 Professional Aesthetic Suite v2.0 | Developed by Muhammet Pınar</p>', unsafe_allow_html=True)
