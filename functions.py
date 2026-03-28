import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
import numpy as np
import hashlib
import imagehash
from PIL.ExifTags import TAGS
import os
import pandas as pd
from openpyxl import load_workbook



# ---------------------- Fonksiyonlar ----------------------

def apply_vintage_effect(img):


    return img

def apply_vintage_effect2(img):


    return img

def apply_vintage_effect3(img):


    return img

def apply_vintage_effect4(img):

    return img

def apply_retro_effect(img):

    return img

from PIL import Image

def overlay_image(foreground_path, background_path, output_path, scale_ratio=0.75):
    # Arka planı aç ve RGBA formatına dönüştür
    background = Image.open(background_path).convert("RGBA")
    
    # Ön planı aç ve RGBA formatına dönüştür
    foreground = Image.open(foreground_path).convert("RGBA")
    
    # Ön planı yeniden boyutlandır
    new_size = (int(foreground.width * scale_ratio), int(foreground.height * scale_ratio))
    foreground = foreground.resize(new_size, resample=Image.LANCZOS)
    
    # Ön planı arka planın ortasına yerleştir
    bg_width, bg_height = background.size
    fg_width, fg_height = foreground.size
    position = ((bg_width - fg_width) // 2, (bg_height - fg_height) // 2)
    
    # Ön planı arka planın üzerine yapıştır
    background.paste(foreground, position, foreground)
    if os.path.exists(output_path):
        os.remove(output_path)    
    # Sonucu kaydet
    background.save(output_path, format="PNG")
    
    background.close()


# Hash Fonksiyonları
def calculate_hash(image_path):
    with open(image_path, "rb") as f:
        bytes = f.read()
        readable_hash = hashlib.md5(bytes).hexdigest()
    return readable_hash

def get_exif(image_path):
    img = Image.open(image_path)
    exif_data = img._getexif()
    if not exif_data:
        return {}
    exif = {TAGS.get(tag): value for tag, value in exif_data.items()}
    return exif

def get_perceptual_hash(image_path):
    img = Image.open(image_path)
    hash_value = imagehash.phash(img)
    return str(hash_value)

def image_to_svg(img, output_svg_path):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{img.width}" height="{img.height}">
    <image href="data:image/png;base64,{img_str}" height="100%" width="100%"/>
    </svg>'''
    with open(output_svg_path, "w") as f:
        f.write(svg_content)
        