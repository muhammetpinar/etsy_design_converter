import os
import zipfile
from dataclasses import dataclass
from typing import List, Callable
from PIL import Image
from src.utils.image_processing import (
    apply_vintage_effect,
    apply_vintage_effect2,
    apply_vintage_effect3,
    apply_vintage_effect4,
    apply_retro_effect,
    overlay_image,
    image_to_svg
)

@dataclass
class BrandConfig:
    name: str           # e.g., "PINART"
    display_title: str  # e.g., "PINART Design Kodu"
    prefix: str         # e.g., "MP"
    effect_fn: Callable # e.g., apply_vintage_effect
    bg_folder: str      # e.g., "PINARTBackGround"
    mockup_white: str   # e.g., "BB.png"
    mockup_black: str   # e.g., "SB.png"
    mockup_prefix: str  # e.g., "MP"
    dpi: tuple = (300, 300)

class DesignProcessor:
    def __init__(self, script_dir: str, base_output_dir: str):
        self.script_dir = script_dir
        self.base_output_dir = base_output_dir
        os.makedirs(self.base_output_dir, exist_ok=True)

    def process_brand(self, brand: BrandConfig, input_img: Image.Image, design_code: str, scale_ratio: float):
        """Processes a single brand: effect -> save png/svg -> generate mockups."""
        
        # 1. Apply Effect
        processed_img = brand.effect_fn(input_img.copy())
        
        # 2. Save Design (PNG)
        design_filename = f"{brand.prefix}{design_code}.png"
        design_path = os.path.join(self.base_output_dir, design_filename)
        processed_img.save(design_path, format="PNG", dpi=brand.dpi)
        
        # 3. Save SVG
        image_to_svg(processed_img, design_path.replace(".png", ".svg"))
        
        # 4. Generate Mockups (Overlays)
        # Assuming asset path: assets/mockups/{brand.bg_folder}/{mockup_white}
        mockup_base_path = os.path.join(self.script_dir, "assets", "mockups", brand.bg_folder)
        
        # White background mockup
        overlay_image(
            processed_img,
            os.path.join(mockup_base_path, brand.mockup_white),
            os.path.join(self.base_output_dir, f"{brand.mockup_prefix}1_{design_code}.png"),
            scale_ratio
        )
        
        # Black background mockup
        overlay_image(
            processed_img,
            os.path.join(mockup_base_path, brand.mockup_black),
            os.path.join(self.base_output_dir, f"{brand.mockup_prefix}2_{design_code}.png"),
            scale_ratio
        )
        
        return design_path

    def create_zip(self, zip_path: str):
        """Packs the base output directory into a ZIP file."""
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(self.base_output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(self.base_output_dir))
                    zipf.write(file_path, arcname)
        return zip_path
