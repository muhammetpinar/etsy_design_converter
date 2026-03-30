import os
import sys
import shutil
import time
import threading
import pandas as pd
from PIL import Image
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ---------------------- Path Management ----------------------
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

# Gerekli importlar (Streamlit versiyonundaki asıl iş parçacıkları)
from src.core.processor import BrandConfig, DesignProcessor
from src.utils.image_processing import (
    apply_vintage_effect,
    apply_vintage_effect2,
    apply_vintage_effect3,
    calculate_hash
)

SCRIPT_DIR = PARENT_DIR

BRANDS = [
    BrandConfig("PINART", "PINART Design Kodu", "MP", apply_vintage_effect, "PINARTBackGround", "BB.png", "SB.png", "MP"),
    BrandConfig("Zeyto", "Zeyto Design Kodu", "Z", apply_vintage_effect2, "ZeytoBackGround", "BB.png", "SB.png", "ZB"),
    BrandConfig("Spring", "Spring Design Kodu", "S", apply_vintage_effect3, "SpringBackGround", "BB.png", "SB.png", "SB"),
    BrandConfig("Bosphorus", "Bosphorus Design Kodu", "B", apply_vintage_effect, "BosphBackGround", "BB.png", "SB.png", "BWB"),
    BrandConfig("Badis", "Badiş Art Design Kodu", "BA", apply_vintage_effect, "BadisBackGround", "BA.png", "BAS.png", "BAB"),
]

# Temayı "Sistem" (Light/Dark ayarına uygun) kullanıyoruz.
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("ETSY FAST IMAGE PRO")
        self.geometry("1000x750")
        self.minsize(900, 650)
        
        # Ekranı ortalamak için Grid yapılandırması
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # ------------------ BAŞLIK ------------------
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, pady=(15, 5), sticky="ew")
        
        self.header_label = ctk.CTkLabel(
            self.header_frame, 
            text="🎨 ETSY FAST IMAGE PRO", 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.header_label.pack()
        
        # ------------------ SEKMELER (TABS) ------------------
        self.tabview = ctk.CTkTabview(self, width=950)
        self.tabview.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        self.tab1 = self.tabview.add("🚀 DİJİTAL ATÖLYE")
        self.tab2 = self.tabview.add("📝 SEO SİHİRBAZI")
        self.tab3 = self.tabview.add("🇺🇸 ÖZEL GÜNLER")
        
        self.tabview.set("🚀 DİJİTAL ATÖLYE")
        
        # Sekme içeriklerini inşa ediyoruz
        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
        
    def setup_tab1(self):
        self.tab1.grid_columnconfigure(0, weight=1)
        self.tab1.grid_columnconfigure(1, weight=1)
        
        # ---- SOL SÜTUN (Yükleme ve Ayarlar) ----
        left_frame = ctk.CTkFrame(self.tab1)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(left_frame, text="📤 Tasarımı Yükle", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.file_path_var = ctk.StringVar()
        self.upload_btn = ctk.CTkButton(left_frame, text="Görsel Seç (PNG)", command=self.select_file, height=40)
        self.upload_btn.pack(pady=(0, 5), padx=20, fill="x")
        
        self.file_label = ctk.CTkLabel(left_frame, text="Dosya seçilmedi", text_color="gray")
        self.file_label.pack(pady=(0, 20))
        
        ctk.CTkLabel(left_frame, text="⚙️ İşlem Parametreleri", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        input_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(input_frame, text="📁 Klasör Kodu :").grid(row=0, column=0, sticky="w", pady=5)
        self.folder_code_entry = ctk.CTkEntry(input_frame, width=150)
        self.folder_code_entry.insert(0, "12")
        self.folder_code_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        ctk.CTkLabel(input_frame, text="📏 Tasarım Ölçeği :").grid(row=1, column=0, sticky="w", pady=15)
        self.scale_slider = ctk.CTkSlider(input_frame, from_=0.1, to=2.0, number_of_steps=38)
        self.scale_slider.set(0.75)
        self.scale_slider.grid(row=1, column=1, sticky="ew", padx=10, pady=15)
        
        self.scale_val_label = ctk.CTkLabel(input_frame, text="0.75")
        self.scale_val_label.grid(row=1, column=2, sticky="w")
        self.scale_slider.configure(command=lambda val: self.scale_val_label.configure(text=f"{val:.2f}"))
        
        # ---- SAĞ SÜTUN (Mağaza Kodları) ----
        right_frame = ctk.CTkFrame(self.tab1)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(right_frame, text="🏷️ Mağaza Kodları", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.brand_entries = {}
        brands_grid = ctk.CTkFrame(right_frame, fg_color="transparent")
        brands_grid.pack(fill="x", padx=20, pady=10)
        
        for i, brand in enumerate(BRANDS):
            row_idx = i // 2
            col_idx = (i % 2) * 2
            
            ctk.CTkLabel(brands_grid, text=f"🆔 {brand.name}:").grid(row=row_idx, column=col_idx, sticky="w", pady=10, padx=(0, 10))
            entry = ctk.CTkEntry(brands_grid, width=100)
            entry.insert(0, "12")
            entry.grid(row=row_idx, column=col_idx+1, sticky="w", pady=10, padx=(0, 20))
            self.brand_entries[brand.name] = entry
            
        # ---- ALT BÖLÜM (Buton ve İşlem Durumu) ----
        action_frame = ctk.CTkFrame(self.tab1, fg_color="transparent")
        action_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky="ew")
        
        self.process_btn = ctk.CTkButton(
            action_frame, 
            text="🚀 TASARIMLARI VE MOCKUPLARI ÜRET", 
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self.start_processing
        )
        self.process_btn.pack(fill="x", padx=10)
        
        self.progress_bar = ctk.CTkProgressBar(action_frame)
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(action_frame, text="")
        
        self.download_btn = ctk.CTkButton(
            action_frame, 
            text="🎁 ÇIKTI KLASÖRÜNÜ VE ZIP'İ AÇ", 
            height=40, 
            command=self.open_output_dir,
            fg_color="#28a745", # Yeşil Renk
            hover_color="#218838"
        )
        
    def setup_tab2(self):
        prompt_text = "ETSY'de dijital ürün satıyorum. Bu ürünler tshirt kupa bardak vs için digital yazdırılabilir ürünler. Format olarak png ve svg satıyorum. ETSY 2025 SEO uyumlu çok fazla satış yapmak istiyorum. Satış yapabilmek ve arttırabilmek için, sana verdiğim konu başlığıyla ilgili tag,title ve açıklama çıkarmanı istiyorum. Bundan sonra bu şekilde ilerleyebilir miyiz ? Tag içerikleri virgülle ayrılsın istiyorum ki kolayca kopyala ypıştır yapabileyim. Bu yaptıklarımın amacı etsy'de satışlarımı arttırabilmek. Dolayısıyla en çok satış yaptıracak tag-tittle ve açıklamayı vermeni istiyorum. Tek bir geniş satış yaptıracak title istiyorum. Tagler en fazla 13 tane olmalı ve satış yaptıracak tagler olmalı. Açıklama kısmında bunun instant dowload ve digital ürün olduğu geçmeli ve kısa ve öz ve açıklayıcı olmalı. Her şey ingilizce ve etsy'de en çok kullanılan anahtar kelimelerle olsun. Description'ın en üst kısmında konu başlığı olsun. En sonunda ise tagler virgülle yazılsın. title 130-140 karakter arası olsun. Tagler 13 tane olsun. Tagler 1 karakter ile 20 karakter arasında olmalı."
        
        ctk.CTkLabel(self.tab2, text="📄 ChatGPT Hazır Prompt", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        textbox = ctk.CTkTextbox(self.tab2, width=800, height=280, font=ctk.CTkFont(size=14))
        textbox.pack(pady=10)
        textbox.insert("0.0", prompt_text)
        textbox.configure(state="disabled")
        
        def copy_to_clipboard():
            self.clipboard_clear()
            self.clipboard_append(prompt_text)
            self.update()
            messagebox.showinfo("Başarılı", "Prompt başarıyla kopyalandı!")
            
        ctk.CTkButton(self.tab2, text="📋 Panoya Kopyala", command=copy_to_clipboard, height=45, width=200).pack(pady=15)
        
    def setup_tab3(self):
        ctk.CTkLabel(self.tab3, text="🇺🇸 Amerika Özel Günleri", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        data = [
            ("NEW YEARS DAY", "1 OCAK"), ("MARTIN LUTHER KING DAY", "17 OCAK"), ("PRESIDENTS DAY", "21 ŞUBAT"),
            ("VALENTINES DAY", "14 ŞUBAT"), ("ST PATRICKS DAY", "17 MART"), ("EASTER DAY", "17 NİSAN"),
            ("MOTHERS DAY", "8 MAYIS"), ("MEMORIAL DAY", "30 MAYIS"), ("JUNETEENTH", "19 HAZİRAN"),
            ("FATHERS DAY", "19 HAZİRAN"), ("4TH OF JULY", "4 TEMMUZ"), ("LABOR DAY", "5 EYLÜL"),
            ("COLUMBUS DAY", "10 EKİM"), ("HALLOWEEN", "31 EKİM"), ("VETERANS DAY", "11 KASIM"),
            ("THANKSGIVING", "24 KASIM"), ("CHRISTMAS", "25 ARALIK")
        ]
        
        frame = ctk.CTkFrame(self.tab3)
        frame.pack(fill="both", expand=True, padx=40, pady=10)
        
        tree = ttk.Treeview(frame, columns=("Etkinlik", "Tarih"), show="headings", height=15)
        tree.heading("Etkinlik", text="ETKİNLİK")
        tree.heading("Tarih", text="TARİH")
        tree.column("Etkinlik", width=400)
        tree.column("Tarih", width=200, anchor="center")
        
        for ev, dt in data:
            tree.insert("", tk.END, values=(ev, dt))
            
        # Tkinter Treeview için CustomTkinter temasıyla uyumlu görsel yapılandırma
        style = ttk.Style()
        style.theme_use("default")
        
        bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        
        style.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, rowheight=30, font=('Helvetica', 12))
        style.map('Treeview', background=[('selected', selected_color)])
        style.configure("Treeview.Heading", background=selected_color, foreground="white", font=('Helvetica', 12, 'bold'))
        
        tree.pack(fill="both", expand=True, padx=20, pady=20)

    # ------------------ İŞLEM FONKSİYONLARI ------------------
    def select_file(self):
        filetypes = [('PNG Dosyaları', '*.png')]
        filename = filedialog.askopenfilename(title='Tasarım Seç (Sadece .png)', filetypes=filetypes)
        if filename:
            self.file_path_var.set(filename)
            self.file_label.configure(text=os.path.basename(filename), text_color=("black", "white"))
            
    def open_output_dir(self):
        if hasattr(self, 'last_output_dir') and os.path.exists(self.last_output_dir):
            os.startfile(self.last_output_dir)
        else:
            messagebox.showwarning("Uyarı", "Görüntülenecek klasör bulunamadı.")

    def start_processing(self):
        if not self.file_path_var.get():
            messagebox.showerror("Hata", "Lütfen önce üretime başlamak için bir tasarım (.png) yükleyin!")
            return
            
        # Arayüzü dondur ve yükleme ekranı göster
        self.process_btn.configure(state="disabled", text="İşleniyor...")
        self.progress_bar.pack(fill="x", padx=10, pady=(15, 5))
        self.status_label.pack(pady=5)
        self.download_btn.pack_forget()
        
        self.progress_bar.set(0)
        self.status_label.configure(text="💎 Masterpiece işleniyor...", text_color="#1f538d")
        
        # Thread ile arkada çalıştır (Pencere donmaması için)
        threading.Thread(target=self.process_task, daemon=True).start()
        
    def process_task(self):
        try:
            folder_code = self.folder_code_entry.get().strip()
            scale_ratio = self.scale_slider.get()
            input_image_path = self.file_path_var.get()
            
            output_dir = os.path.join(SCRIPT_DIR, "outputs", f"MP_{folder_code}")
            processor = DesignProcessor(SCRIPT_DIR, output_dir)
            
            temp_input_path = os.path.join(SCRIPT_DIR, "temp_input.png")
            shutil.copy2(input_image_path, temp_input_path)
            
            img = Image.open(temp_input_path).convert("RGBA")
            self.results = []
            
            for i, brand in enumerate(BRANDS):
                d_code = self.brand_entries[brand.name].get().strip()
                
                # Arayüzü güvenli şekilde güncelle (after kullanarak main thread'e aktar)
                self.after(0, self.update_status, f"🎨 {brand.name} varyasyonları oluşturuluyor", i/len(BRANDS))
                
                design_path = processor.process_brand(brand, img, d_code, scale_ratio)
                self.results.append({
                    "Marka": brand.name, 
                    "Dosya": os.path.basename(design_path), 
                    "Hash": calculate_hash(design_path)
                })
            
            # Zip oluştur
            self.after(0, self.update_status, f"📦 Çıktılar Zipleniyor...", 0.95)
            timestamp = int(time.time())
            zip_filename = f"MP_{folder_code}_{timestamp}"
            zip_full_path = os.path.join(SCRIPT_DIR, zip_filename)
            shutil.make_archive(zip_full_path, 'zip', output_dir)
            
            self.last_output_dir = output_dir
            
            # Bitti
            self.after(0, self.finish_processing)
            
        except Exception as e:
            self.after(0, self.fail_processing, str(e))
            
    def update_status(self, text, progress):
        self.status_label.configure(text=text)
        self.progress_bar.set(progress)
        
    def finish_processing(self):
        self.progress_bar.set(1.0)
        self.status_label.configure(text="✅ Tüm süreç başarıyla tamamlandı!", text_color="#28a745")
        self.process_btn.configure(state="normal", text="🚀 TASARIMLARI VE MOCKUPLARI ÜRET")
        self.download_btn.pack(fill="x", padx=10, pady=10)
        messagebox.showinfo("Başarılı", "Çıktılar başarıyla üretildi ve ziplendi!\n'Aç' butonuna tıklayarak dosyalara ulaşabilirsiniz.")
        
    def fail_processing(self, error):
        self.progress_bar.pack_forget()
        self.status_label.configure(text=f"❌ Hata oluştu: {error}", text_color="red")
        self.process_btn.configure(state="normal", text="🚀 TASARIMLARI VE MOCKUPLARI ÜRET")
        messagebox.showerror("İşlem Hatası", f"Beklenmeyen bir hata oluştu:\n{error}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
