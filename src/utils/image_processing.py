import os
import io
import base64
import hashlib
import imagehash
from PIL import Image, ImageEnhance, ImageFilter
from PIL.ExifTags import TAGS

def apply_vintage_effect(img):
    """Slightly warmer and higher contrast."""
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    if img.mode == 'RGBA':
        r, g, b, a = img.split()
        r = r.point(lambda i: i * 1.1)
        b = b.point(lambda i: i * 0.9)
        img = Image.merge('RGBA', (r, g, b, a))
    return img

def apply_vintage_effect2(img):
    """Slightly darker and more saturated."""
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.3)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.9)
    return img

def apply_vintage_effect3(img):
    """Blurry/dreamy look."""
    return img.filter(ImageFilter.GaussianBlur(radius=1))

def apply_vintage_effect4(img):
    """Greyscale-ish vintage."""
    return img.convert("L").convert("RGBA")

def apply_retro_effect(img):
    """Lower contrast, shifted colors."""
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(0.8)
    if img.mode == 'RGBA':
        r, g, b, a = img.split()
        g = g.point(lambda i: i * 1.1)
        img = Image.merge('RGBA', (r, g, b, a))
    return img

def overlay_image(foreground_img, background_path, output_path, scale_ratio=0.75):
    """
    Overlays a foreground image onto a background image.
    Args:
        foreground_img (PIL.Image): The design to overlay.
        background_path (str): Path to the mockup background.
        output_path (str): Path to save the result.
        scale_ratio (float): Scaling factor for the foreground.
    """
    # Ensure background exists
    if not os.path.exists(background_path):
        return False

    background = Image.open(background_path).convert("RGBA")
    
    # Resize foreground
    new_size = (int(foreground_img.width * scale_ratio), int(foreground_img.height * scale_ratio))
    foreground = foreground_img.resize(new_size, resample=Image.LANCZOS)
    
    # Center position
    bg_width, bg_height = background.size
    fg_width, fg_height = foreground.size
    position = ((bg_width - fg_width) // 2, (bg_height - fg_height) // 2)
    
    # Paste
    background.paste(foreground, position, foreground)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if os.path.exists(output_path):
        os.remove(output_path)
        
    background.save(output_path, format="PNG")
    background.close()
    return True

def calculate_hash(image_path):
    """Calculates MD5 hash of a file."""
    if not os.path.exists(image_path):
        return "N/A"
    with open(image_path, "rb") as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()

def image_to_svg(img, output_svg_path):
    """Wraps a PNG in an SVG tag."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{img.width}" height="{img.height}">
    <image href="data:image/png;base64,{img_str}" height="100%" width="100%"/>
    </svg>'''
    os.makedirs(os.path.dirname(output_svg_path), exist_ok=True)
    with open(output_svg_path, "w") as f:
        f.write(svg_content)
