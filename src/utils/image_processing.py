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

def apply_hash_breaker(img):
    """Subtly modifies an image to change its hash without visual side effects."""
    enhancer = ImageEnhance.Brightness(img)
    # Apply a tiny 0.01% change to shift pixel values
    img = enhancer.enhance(1.0001)
    return img

def apply_retro_effect(img):
    """Lower contrast, shifted colors."""
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(0.8)
    if img.mode == 'RGBA':
        r, g, b, a = img.split()
        g = g.point(lambda i: i * 1.1)
        img = Image.merge('RGBA', (r, g, b, a))
    return img

def overlay_image(foreground_img, background_path_or_obj, output_path, scale_ratio=0.75, bg_opacity=1.0):
    """
    Overlays a foreground image onto a background image.
    Args:
        foreground_img (PIL.Image): The design to overlay.
        background_path_or_obj (str or PIL.Image): Path to mockup or an Image object.
        output_path (str): Path to save the result.
        scale_ratio (float): Scaling factor for the foreground.
        bg_opacity (float): Opacity of the background (0.0 to 1.0).
    """
    if isinstance(background_path_or_obj, str):
        if not os.path.exists(background_path_or_obj):
            return False
        background = Image.open(background_path_or_obj).convert("RGBA")
    elif hasattr(background_path_or_obj, "convert"):
        # It's likely already a PIL Image object
        background = background_path_or_obj.copy().convert("RGBA")
    else:
        # File-like object (UploadedFile from streamit)
        background = Image.open(background_path_or_obj).convert("RGBA")
    
    # Apply opacity to background
    if bg_opacity < 1.0:
        alpha = background.split()[3]
        alpha = alpha.point(lambda i: i * bg_opacity)
        background.putalpha(alpha)
    
    # Create a white canvas (base) of the same size as the background
    canvas = Image.new("RGBA", background.size, (255, 255, 255, 255))
    
    # Resize foreground (Design)
    new_size = (int(foreground_img.width * scale_ratio), int(foreground_img.height * scale_ratio))
    foreground = foreground_img.resize(new_size, resample=Image.LANCZOS)
    
    # Center position for design on canvas
    bg_width, bg_height = background.size
    fg_width, fg_height = foreground.size
    position = ((bg_width - fg_width) // 2, (bg_height - fg_height) // 2)
    
    # Step 1: Paste Design on White Canvas
    canvas.paste(foreground, position, foreground)

    # Step 2: Overlay semi-transparent Mockup (Background) on top
    canvas.paste(background, (0, 0), background)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if os.path.exists(output_path):
        os.remove(output_path)
        
    canvas.save(output_path, format="PNG")
    canvas.close()
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
