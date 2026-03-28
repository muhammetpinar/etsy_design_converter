from functions import *
# ---------------------- Streamlit Başlangıcı ----------------------

st.title(" ETSY FAST IMAGE")

tab1, tab2, tab3 = st.tabs(["Original to Changed Photos", "ChatGPT Prompt Title-Tag-Description", "American Special Days"])

# 1. Vintage Efekti
with tab1:
    st.header("Change Photo Hash")
    
    #st.image("https://media.licdn.com/dms/image/v2/D4D03AQG1wvvZmAp8-g/profile-displayphoto-shrink_200_200/B4DZPfV64AHMAY-/0/1734618887524?e=2147483647&v=beta&t=R_A6FtMHgPRby6-tz8QVSGzy-EBC7iVXS3bsUQ0scNs", caption="Muhammet Pınar", use_container_width =False)

    input_image = st.file_uploader("Girdi görselini yükle", type=["png"], key="vintage_input")
    output_png_vintage = st.text_input("MP Klasör ve Design Kodu", "12")
    output_png_vintage2 = st.text_input("Zeyto Design Kodu", "12")
    output_png_vintage3 = st.text_input("Spring Design Kodu", "12")
    output_png_vintage4 = st.text_input("Hope Design Kodu", "12")
    output_png_vintage5 = st.text_input("Bosphorus Design Kodu", "12")
    output_png_vintage6 = st.text_input("Badiş Art Design Kodu", "12")

    path_PINART = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/MP{output_png_vintage}.png"
    path_Zeyto = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/Z{output_png_vintage2}.png"
    path_Spring = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/S{output_png_vintage3}.png"
    path_Hope = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/H{output_png_vintage4}.png"
    path_Bosph = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/B{output_png_vintage5}.png"
    path_Badis = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/BA{output_png_vintage6}.png"

    scale_ratio = st.slider("Ön plan ölçek oranı", 0.1, 2.0, 0.75, step=0.05)


    if st.button("RUN"):
        if input_image:
            with open("temp_input_image.png", "wb") as f:
                f.write(input_image.read())
                img = Image.open("temp_input_image.png").convert("RGBA")
                img = apply_vintage_effect(img)
                img2 = apply_vintage_effect2(img)
                img3 = apply_vintage_effect3(img)
                img4 = apply_retro_effect(img)
                img5 = apply_vintage_effect(img)
                img6 = apply_vintage_effect(img)

                output_folder = os.path.dirname(path_PINART)
                if output_folder and not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                            
                img.save(path_PINART, format="PNG", dpi=(300, 300))
                img2.save(path_Zeyto, format="PNG", dpi=(350, 300))
                img3.save(path_Spring, format="PNG", dpi=(400, 300))
                img4.save(path_Hope, format="PNG", dpi=(450, 300))
                img5.save(path_Bosph, format="PNG", dpi=(300, 350))
                img6.save(path_Badis, format="PNG", dpi=(320, 350))


                # Ayrıca SVG olarak da kaydet
                output_svg_vintage = path_PINART.replace(".png", ".svg")
                output_svg_vintage2 = path_Zeyto.replace(".png", ".svg")
                output_svg_vintage3 = path_Spring.replace(".png", ".svg")
                output_svg_vintage4 = path_Hope.replace(".png", ".svg")
                output_svg_vintage5 = path_Bosph.replace(".png", ".svg")
                output_svg_vintage6 = path_Badis.replace(".png", ".svg")

                image_to_svg(img, output_svg_vintage)
                image_to_svg(img2, output_svg_vintage2)
                image_to_svg(img3, output_svg_vintage3)
                image_to_svg(img, output_svg_vintage4)
                image_to_svg(img, output_svg_vintage5)
                image_to_svg(img, output_svg_vintage6)
                


                st.success(f"Güncellenmiş Fotoğraflar Yüklendi !: {path_PINART}")

                foreground_file_PIN = path_PINART
                foreground_file_ZEY = path_Zeyto
                foreground_file_SIP = path_Spring
                foreground_file_HOPE =path_Hope
                foreground_file_BOSPH =path_Bosph
                foreground_file_BADIS =path_Badis

                backgroundPINART_White = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/PINARTBackGround/BB.png"
                backgroundPINART_Black = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/PINARTBackGround/SB.png"
                backgroundZeyto_White = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/ZeytoBackGround/BB.png"
                backgroundZeyto_Black = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/ZeytoBackGround/SB.png"
                backgroundSpring_White = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/SpringBackGround/BB.png"
                backgroundSpring_Black = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/SpringBackGround/SB.png"
                backgroundHope_White = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/HopeBackGround/BB.png"
                backgroundHope_Black = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/HopeBackGround/SB.png"
                backgroundBosph_White = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/BosphBackGround/BB.png"
                backgroundBosph_Black = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/BosphBackGround/SB.png"
                backgroundBadis_White = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/BadisBackGround/BA.png"
                backgroundBadis_Black = "C:/Users/mpina/OneDrive/Masaüstü/ETSY/Codes/BadisBackGround/BAS.png"
                
                output_overlay_PIN  = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/MP1_{output_png_vintage}.png"
                output_overlay_PIN2 = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/MP2_{output_png_vintage}.png"
                output_overlay_ZEY = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/ZB1_{output_png_vintage2}.png"
                output_overlay_ZEY2= f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/ZB2_{output_png_vintage2}.png"
                output_overlay_SIP  = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/SB1_{output_png_vintage3}.png"
                output_overlay_SIP2 = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/SB2_{output_png_vintage3}.png"    
                output_overlay_HOP  = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/HB1_{output_png_vintage4}.png"
                output_overlay_HOP2 = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/HB2_{output_png_vintage4}.png"
                output_overlay_BOSPH  = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/BWB1_{output_png_vintage5}.png"
                output_overlay_BOSPH2 = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/BWB2_{output_png_vintage5}.png"
                output_overlay_BADIS  = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/BAB1_{output_png_vintage6}.png"
                output_overlay_BADIS2 = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_{output_png_vintage}/BAB2_{output_png_vintage6}.png"

                # Normal arka plan üzerine overlay
                overlay_image(foreground_file_PIN, backgroundPINART_White, output_overlay_PIN, scale_ratio)
                overlay_image(foreground_file_PIN, backgroundPINART_Black, output_overlay_PIN2, scale_ratio)

                overlay_image(foreground_file_ZEY, backgroundZeyto_White, output_overlay_ZEY, scale_ratio)
                overlay_image(foreground_file_ZEY, backgroundZeyto_Black, output_overlay_ZEY2, scale_ratio)

                overlay_image(foreground_file_SIP, backgroundSpring_White, output_overlay_SIP, scale_ratio)
                overlay_image(foreground_file_SIP, backgroundSpring_Black, output_overlay_SIP2, scale_ratio)

                overlay_image(foreground_file_HOPE, backgroundHope_White, output_overlay_HOP, scale_ratio)
                overlay_image(foreground_file_HOPE, backgroundHope_Black, output_overlay_HOP2, scale_ratio)

                overlay_image(foreground_file_BOSPH, backgroundBosph_White, output_overlay_BOSPH, scale_ratio)
                overlay_image(foreground_file_BOSPH, backgroundBosph_Black, output_overlay_BOSPH2, scale_ratio)

                overlay_image(foreground_file_BADIS, backgroundBadis_White, output_overlay_BADIS, scale_ratio)
                overlay_image(foreground_file_BADIS, backgroundBadis_Black, output_overlay_BADIS2, scale_ratio)

                st.success(f"Overlay İşlemleri Başarıyla Tamamlandı !")



                
                # Hash bilgilerini göster
                st.subheader("🔎 Hash Bilgileri")
                st.text(f"Input MD5 Hash: {calculate_hash('temp_input_vintage.png')}")
                st.text(f" PINART  Output MD5 Hash: {calculate_hash(path_PINART)}")
                st.text(f" Zeyto  Output MD5 Hash: {calculate_hash(path_Zeyto)}")
                st.text(f" Spring  Output MD5 Hash: {calculate_hash(path_Spring)}")
                st.text(f" Hope  Output MD5 Hash: {calculate_hash(path_Hope)}")
                st.text(f" Bosp  Output MD5 Hash: {calculate_hash(path_Bosph)}")
                st.text(f" Badis  Output MD5 Hash: {calculate_hash(path_Badis)}")

                """st.text(f" Input Algoritmik Görsel Kimlik (pHash): {get_perceptual_hash('temp_input_vintage.png')}")
                st.text(f" PINART Output Algoritmik Görsel Kimlik (pHash): {get_perceptual_hash(path_PINART)}")
                st.text(f" Zeyto Output Algoritmik Görsel Kimlik (pHash): {get_perceptual_hash(path_Zeyto)}")
                st.text(f" Spring Output Algoritmik Görsel Kimlik (pHash): {get_perceptual_hash(path_Spring)}")
                st.text(f" Hope Output Algoritmik Görsel Kimlik (pHash): {get_perceptual_hash(path_Hope)}")

                st.text(f" Bosphorus Output Algoritmik Görsel Kimlik (pHash): {get_perceptual_hash(path_Bosph)}")"""

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("🔗 Developed by **Muhammet Pınar** | Powered by Streamlit", unsafe_allow_html=True)


# 3. Overlay Görsel Ekleme
with tab2:
    st.header("📄ChatGPT Hazır Prompt")
    st.markdown(f"""

    <div style="background-color:#DFF0D8;padding:10px;border-radius:10px">
ETSY'de dijital ürün satıyorum. Bu ürünler tshirt kupa bardak vs için digital yazdırılabilir ürünler. Format olarak png ve svg satıyorum. ETSY 2025 SEO uyumlu çok fazla satış yapmak istiyorum. Satış yapabilmek ve arttırabilmek için, sana verdiğim konu başlığıyla ilgili tag,title ve açıklama çıkarmanı istiyorum. Bundan sonra bu şekilde ilerleyebilir miyiz ? Tag içerikleri virgülle ayrılsın istiyorum ki kolayca kopyala ypıştır yapabileyim. Bu yaptıklarımın amacı etsy'de satışlarımı arttırabilmek. Dolayısıyla en çok satış yaptıracak tag-tittle ve açıklamayı vermeni istiyorum. Tek bir geniş satış yaptıracak title istiyorum. Tagler en fazla 13 tane olmalı ve satış yaptıracak tagler olmalı. Açıklama kısmında bunun instant dowload ve digital ürün olduğu geçmeli ve kısa ve öz ve açıklayıcı olmalı. Her şey ingilizce ve etsy'de en çok kullanılan anahtar kelimelerle olsun. Description'ın en üst kısmında koınu başlığı olsun. En sonunda ise tagler virgülle yazılsın.  title 130-140 karakter arası olsun. Tagler 13 tane olsun. Tagler 1 karakter ile 20 karakter arasında olmalı.
    </div>
    """,
    unsafe_allow_html=True)
    
    
    
    
with tab3:
    st.header("🇺🇸 Amerika Özel Günleri")

    # Özel günler sözlüğü
    special_days = {
        "OZEL TARIH": [
            "NEW YEARS DAY",
            "MARTIN LUTHER KING DAY",
            "PRESIDENTS DAY",
            "VALENTINES DAY",
            "ST PATRICKS DAY",
            "EASTER DAY",
            "MOTHERS DAY",
            "MEMORIAL DAY",
            "NATIONAL INDEPENDENCE DAY",
            "FATHERS DAY",
            "4TH OF JULY",
            "LABOR DAY",
            "COLUMBUS DAY",
            "HALLOWEEN",
            "VETERANS DAY",
            "THANKSGIVING",
            "CHRISTMAS"
        ],
        "TARIH": [
            "1 OCAK",
            "17 OCAK",
            "21 ŞUBAT",
            "14 ŞUBAT",
            "17 MART",
            "17 NİSAN",
            "8 MAYIS",
            "30 MAYIS",
            "19 HAZİRAN",
            "19 HAZİRAN",
            "4 TEMMUZ",
            "5 EYLÜL",
            "10 EKİM",
            "31 EKİM",
            "11 KASIM",
            "24 KASIM",
            "25 ARALIK"
        ]
    }

    df = pd.DataFrame(special_days)
    st.dataframe(df, use_container_width=True)
    
    
    