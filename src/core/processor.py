import os
from dataclasses import dataclass
from typing import Callable
from PIL import Image
from src.utils.image_processing import (
    apply_vintage_effect,
    apply_vintage_effect2,
    apply_vintage_effect3,
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

    def process_brand(self, brand: BrandConfig, input_img: Image.Image, design_code: str, scale_ratio: float, bg_opacity: float = 1.0, custom_bg1=None, custom_bg2=None):
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
        mockup_base_path = os.path.join(self.script_dir, "assets", "mockups", brand.bg_folder)
        
        # Determine background sources (Custom override or Default brand path)
        bg1_source = custom_bg1 if custom_bg1 is not None else os.path.join(mockup_base_path, brand.mockup_white)
        bg2_source = custom_bg2 if custom_bg2 is not None else os.path.join(mockup_base_path, brand.mockup_black)

        # White background mockup (or custom 1)
        mockup_white_path = os.path.join(self.base_output_dir, f"{brand.mockup_prefix}1_{design_code}.png")
        overlay_image(
            processed_img,
            bg1_source,
            mockup_white_path,
            scale_ratio,
            bg_opacity
        )
        
        # Black background mockup (or custom 2)
        mockup_black_path = os.path.join(self.base_output_dir, f"{brand.mockup_prefix}2_{design_code}.png")
        overlay_image(
            processed_img,
            bg2_source,
            mockup_black_path,
            scale_ratio,
            bg_opacity
        )
        
        return {
            "design": design_path,
            "mockup_white": mockup_white_path,
            "mockup_black": mockup_black_path
        }
