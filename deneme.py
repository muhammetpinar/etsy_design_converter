
from PIL import Image, ImageEnhance, ImageFilter
import imagehash


def get_perceptual_hash(image_path):
    img = Image.open(image_path)
    hash_value = imagehash.phash(img)
    return str(hash_value)


path1 = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_139/S_42.png"
path2 = f"C:/Users/mpina/OneDrive/Masaüstü/ETSY/Designs/MP_139/Z86.png"

print(f" PINART Output Algoritmik Görsel Kimlik (pHash): {get_perceptual_hash(path1)}")
print(f" PINART Output Algoritmik Görsel Kimlik (pHash): {get_perceptual_hash(path2)}")