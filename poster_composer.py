"""
PromptPoster AI - Professional Poster Composer Module
Master graphic design pipeline: 3D extruded typography, cinematic gradient overlays,
ambient depth watermarks, glassmorphic info plates, VIP ticket barcodes, and high-res export.
"""

import os
import io
import math
import random
from typing import Dict, Any, Optional, Tuple, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


# Available Font Families (Mapping to standard Windows system fonts with safe fallbacks)
FONT_MAP = {
    "Modern Sans (Segoe UI)": {
        "bold": ["C:/Windows/Fonts/segoeuib.ttf", "segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"],
        "regular": ["C:/Windows/Fonts/segoeui.ttf", "segoeui.ttf", "C:/Windows/Fonts/arial.ttf"],
        "light": ["C:/Windows/Fonts/segoeuil.ttf", "segoeuil.ttf", "C:/Windows/Fonts/arial.ttf"]
    },
    "Bold Impact (Display)": {
        "bold": ["C:/Windows/Fonts/impact.ttf", "impact.ttf", "C:/Windows/Fonts/ariblk.ttf"],
        "regular": ["C:/Windows/Fonts/segoeuib.ttf", "segoeuib.ttf"],
        "light": ["C:/Windows/Fonts/segoeui.ttf", "segoeui.ttf"]
    },
    "Clean Grotesk (Arial)": {
        "bold": ["C:/Windows/Fonts/arialbd.ttf", "arialbd.ttf"],
        "regular": ["C:/Windows/Fonts/arial.ttf", "arial.ttf"],
        "light": ["C:/Windows/Fonts/ariali.ttf", "arial.ttf"]
    },
    "Cyber Tech (Consolas)": {
        "bold": ["C:/Windows/Fonts/consolab.ttf", "consolab.ttf"],
        "regular": ["C:/Windows/Fonts/consola.ttf", "consola.ttf"],
        "light": ["C:/Windows/Fonts/consola.ttf", "consola.ttf"]
    },
    "Cinematic Serif (Georgia)": {
        "bold": ["C:/Windows/Fonts/georgiab.ttf", "georgiab.ttf"],
        "regular": ["C:/Windows/Fonts/georgia.ttf", "georgia.ttf"],
        "light": ["C:/Windows/Fonts/georgiai.ttf", "georgia.ttf"]
    },
    "Geometric Clean (Trebuchet)": {
        "bold": ["C:/Windows/Fonts/trebucbd.ttf", "trebucbd.ttf"],
        "regular": ["C:/Windows/Fonts/trebuc.ttf", "trebuc.ttf"],
        "light": ["C:/Windows/Fonts/trebuc.ttf", "trebuc.ttf"]
    }
}


def load_font(family_name: str, weight: str = "bold", size: int = 40) -> ImageFont.ImageFont:
    """Loads requested font with fallbacks to system fonts or default PIL font."""
    family = FONT_MAP.get(family_name, FONT_MAP["Modern Sans (Segoe UI)"])
    candidates = family.get(weight, family.get("bold", []))
    
    all_candidates = candidates + [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "arial.ttf"
    ]
    
    for path in all_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                continue
        try:
            return ImageFont.truetype(os.path.basename(path), size=size)
        except Exception:
            continue
            
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


def crop_and_resize(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Resizes and crops the image to fill the target dimensions with high-quality Lanczos resampling."""
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        new_h = target_h
        new_w = int(src_w * (target_h / src_h))
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - target_w) // 2
        return resized.crop((left, 0, left + target_w, target_h))
    else:
        new_w = target_w
        new_h = int(src_h * (target_w / src_w))
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        top = (new_h - target_h) // 2
        return resized.crop((0, top, target_w, top + target_h))


def apply_vignette(image: Image.Image, amount: float = 0.45) -> Image.Image:
    """Applies a smooth radial dark vignette around the edges to focus dramatic attention."""
    if not NUMPY_AVAILABLE or amount <= 0.05:
        return image

    w, h = image.size
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    xx, yy = np.meshgrid(x, y)
    radius = np.sqrt(xx**2 + yy**2)
    norm_radius = radius / math.sqrt(2.0)
    
    mask = 1.0 - np.clip((norm_radius - 0.35) / 0.65, 0.0, 1.0) * amount
    mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
    
    img_np = np.array(image.convert("RGB"), dtype=np.float32)
    vignetted_np = np.clip(img_np * mask, 0, 255).astype(np.uint8)
    return Image.fromarray(vignetted_np)


def create_cinematic_gradient_overlay(
    width: int,
    height: int,
    placement: str = "Bottom",
    intensity: float = 0.55,
    tint_rgb: Tuple[int, int, int] = (10, 12, 20)
) -> Image.Image:
    """Creates a multi-stop translucent atmospheric gradient overlay for readability."""
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    max_alpha = int(255 * min(max(intensity, 0.0), 0.95))
    r, g, b = tint_rgb

    if placement == "Bottom":
        fade_start = int(height * 0.35)
        fade_len = max(height - fade_start, 1)
        for y in range(height):
            if y < fade_start:
                a = int(max_alpha * 0.22 * (1.0 - y / fade_start))
            else:
                ratio = (y - fade_start) / fade_len
                a = int(max_alpha * (ratio ** 1.25))
            draw.line([(0, y), (width, y)], fill=(r, g, b, min(a, 255)))

    elif placement == "Top":
        fade_end = int(height * 0.65)
        for y in range(height):
            if y <= fade_end:
                ratio = 1.0 - (y / fade_end)
                a = int(max_alpha * (ratio ** 1.25))
            else:
                ratio = (y - fade_end) / (height - fade_end)
                a = int(max_alpha * 0.28 * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b, min(a, 255)))

    else:  # Center
        for y in range(height):
            norm_y = abs(y - height / 2) / (height / 2)
            a = int(max_alpha * (0.35 + 0.55 * (norm_y ** 1.4)))
            draw.line([(0, y), (width, y)], fill=(r, g, b, min(a, 255)))

    return overlay


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    """Wraps text neatly to fit within max_width pixels."""
    words = text.split()
    if not words:
        return []
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def draw_3d_extruded_text(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill_color: Tuple[int, int, int] = (255, 255, 255),
    glow_color: Tuple[int, int, int] = (0, 240, 255),
    depth: int = 5
):
    """Draws 3D extruded title text with multiple micro-offset shadow layers and glowing rim."""
    x, y = xy
    # 1. Subtle wide ambient glow
    for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
        draw.text((x + dx, y + dy), text, font=font, fill=glow_color + (90,))
        
    # 2. Extrusion depth layers (dark volumetric drop)
    for d in range(depth, 0, -1):
        alpha = int(240 * (1.0 - (d / (depth + 1)) * 0.4))
        draw.text((x + d, y + d), text, font=font, fill=(0, 0, 0, alpha))
        
    # 3. Main face text
    draw.text((x, y), text, font=font, fill=fill_color)


def draw_barcode(draw: ImageDraw.ImageDraw, x: int, y: int, width: int = 110, height: int = 32, color=(255, 255, 255, 180)):
    """Draws a sleek VIP ticket barcode graphic accent on the poster."""
    random.seed(999)
    curr_x = x
    while curr_x < x + width:
        bar_w = random.choice([1, 2, 3, 4])
        draw.rectangle([(curr_x, y), (curr_x + bar_w - 1, y + height)], fill=color)
        curr_x += bar_w + random.choice([2, 3, 4])


def draw_decorative_frame(
    draw: ImageDraw.ImageDraw,
    width: int,
    height: int,
    frame_style: str = "Modern Minimalist",
    color: Tuple[int, int, int] = (255, 255, 255),
    accent_color: Tuple[int, int, int] = (0, 240, 255)
):
    """Draws customizable graphic frames, borderlines, or high-tech corner brackets."""
    inset = 28
    
    if frame_style == "Modern Minimalist":
        draw.rectangle([(inset, inset), (width - inset, height - inset)], outline=color + (140,), width=2)
    elif frame_style == "Cyberpunk Brackets":
        bracket_len = 55
        line_w = 3
        # Top-Left
        draw.line([(inset, inset), (inset + bracket_len, inset)], fill=accent_color, width=line_w)
        draw.line([(inset, inset), (inset, inset + bracket_len)], fill=accent_color, width=line_w)
        draw.ellipse([(inset - 2, inset - 2), (inset + 4, inset + 4)], fill=accent_color)
        # Top-Right
        draw.line([(width - inset, inset), (width - inset - bracket_len, inset)], fill=accent_color, width=line_w)
        draw.line([(width - inset, inset), (width - inset, inset + bracket_len)], fill=accent_color, width=line_w)
        draw.ellipse([(width - inset - 3, inset - 2), (width - inset + 3, inset + 4)], fill=accent_color)
        # Bottom-Left
        draw.line([(inset, height - inset), (inset + bracket_len, height - inset)], fill=accent_color, width=line_w)
        draw.line([(inset, height - inset), (inset, height - inset - bracket_len)], fill=accent_color, width=line_w)
        draw.ellipse([(inset - 2, height - inset - 3), (inset + 4, height - inset + 3)], fill=accent_color)
        # Bottom-Right
        draw.line([(width - inset, height - inset), (width - inset - bracket_len, height - inset)], fill=accent_color, width=line_w)
        draw.line([(width - inset, height - inset), (width - inset, height - inset - bracket_len)], fill=accent_color, width=line_w)
        draw.ellipse([(width - inset - 3, height - inset - 3), (width - inset + 3, height - inset + 3)], fill=accent_color)
    elif frame_style == "Double Luxury Frame":
        draw.rectangle([(inset, inset), (width - inset, height - inset)], outline=color + (180,), width=2)
        inner_inset = inset + 12
        draw.rectangle([(inner_inset, inner_inset), (width - inner_inset, height - inner_inset)], outline=accent_color + (120,), width=1)


def compose_final_poster(
    background_image: Image.Image,
    title: str = "PROMPTPOSTER AI",
    subtitle: str = "Next-Gen AI Poster Creation",
    category: str = "Technology",
    date_text: str = "",
    venue_text: str = "",
    organizer_text: str = "",
    extra_details: str = "",
    target_width: int = 900,
    target_height: int = 1200,
    font_family: str = "Modern Sans (Segoe UI)",
    theme_colors: Optional[Dict[str, Any]] = None,
    text_placement: str = "Bottom",
    overlay_intensity: float = 0.55,
    frame_style: str = "Modern Minimalist",
    title_scale: float = 1.0,
    apply_vignette_effect: bool = True,
    title_color: Optional[Tuple[int, int, int]] = None,
    **kwargs
) -> Image.Image:
    """
    Master poster composition pipeline.
    Transforms artwork into a commercial agency-quality graphic poster.
    """
    if not date_text and "date" in kwargs:
        date_text = kwargs["date"]
    if not venue_text and "venue" in kwargs:
        venue_text = kwargs["venue"]
    if not organizer_text and "organizer" in kwargs:
        organizer_text = kwargs["organizer"]

    # 1. Resize and crop background with Lanczos
    base_poster = crop_and_resize(background_image, target_width, target_height)

    # 2. Dramatic Color Grading & Vibrance Boost
    color_enhancer = ImageEnhance.Color(base_poster)
    base_poster = color_enhancer.enhance(1.22)
    contrast_enhancer = ImageEnhance.Contrast(base_poster)
    base_poster = contrast_enhancer.enhance(1.18)

    # 3. Apply radial vignette
    if apply_vignette_effect:
        base_poster = apply_vignette(base_poster, amount=0.45)

    # 4. Color theme resolution
    if not theme_colors:
        theme_colors = {
            "primary_rgb": (0, 240, 255),
            "secondary_rgb": (255, 0, 128),
            "accent_rgb": (255, 255, 255),
            "overlay_tint": (10, 14, 25)
        }
    primary_color = theme_colors.get("primary_rgb", (0, 240, 255))
    accent_color = theme_colors.get("accent_rgb", (255, 255, 255))
    tint = theme_colors.get("overlay_tint", (10, 14, 25))

    # 5. Apply dynamic gradient overlay
    overlay = create_cinematic_gradient_overlay(
        target_width,
        target_height,
        placement=text_placement,
        intensity=overlay_intensity,
        tint_rgb=tint
    )
    composed = Image.alpha_composite(base_poster.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(composed)

    safe_margin_x = 56
    max_text_width = target_width - (safe_margin_x * 2)
    center_x = target_width // 2

    # 6. Subtle Atmospheric Background Watermark Text (Adds Massive Depth!)
    watermark_word = category.upper() if len(category) <= 8 else "PREMIERE"
    watermark_font = load_font(font_family, weight="bold", size=int(140 * (target_width / 900)))
    bbox_wm = draw.textbbox((0, 0), watermark_word, font=watermark_font)
    wm_w = bbox_wm[2] - bbox_wm[0]
    wm_y = int(target_height * 0.44)
    draw.text((center_x - wm_w // 2, wm_y), watermark_word, font=watermark_font, fill=primary_color + (25,))

    # 7. Draw graphic decorative frame
    draw_decorative_frame(draw, target_width, target_height, frame_style, color=(255, 255, 255), accent_color=primary_color)

    # 8. Top Category Badge Pill with Glow
    badge_text = f"★  {category.upper()}  •  OFFICIAL SELECTION  ★"
    badge_font = load_font(font_family, weight="bold", size=int(13 * (target_width / 900)))
    bbox_b = draw.textbbox((0, 0), badge_text, font=badge_font)
    bw = bbox_b[2] - bbox_b[0]
    bh = bbox_b[3] - bbox_b[1]
    
    badge_y = 52
    badge_pad_x, badge_pad_y = 22, 9
    badge_rect = [
        (center_x - (bw // 2) - badge_pad_x, badge_y - badge_pad_y),
        (center_x + (bw // 2) + badge_pad_x, badge_y + bh + badge_pad_y)
    ]
    draw.rounded_rectangle(badge_rect, radius=14, fill=(10, 16, 32, 215), outline=primary_color + (220,), width=2)
    draw.text((center_x - (bw // 2), badge_y - 2), badge_text, font=badge_font, fill=primary_color)

    # 9. Main Title Layout (3D Extruded Masterpiece)
    base_title_size = int(72 * title_scale * (target_width / 900))
    title_font = load_font(font_family, weight="bold", size=base_title_size)
    title_clean = title.strip().upper() if title else "POSTER TITLE"
    title_lines = wrap_text(draw, title_clean, title_font, max_text_width)
    
    if len(title_lines) > 2:
        base_title_size = int(base_title_size * 0.78)
        title_font = load_font(font_family, weight="bold", size=base_title_size)
        title_lines = wrap_text(draw, title_clean, title_font, max_text_width)

    test_bbox = draw.textbbox((0, 0), "Aj", font=title_font)
    title_line_h = int((test_bbox[3] - test_bbox[1]) * 1.15)

    if text_placement == "Top":
        title_start_y = 125
    elif text_placement == "Center":
        total_title_h = len(title_lines) * title_line_h
        title_start_y = (target_height // 2) - (total_title_h // 2) - 80
    else:  # "Bottom" (Classic Blockbuster Poster)
        title_start_y = int(target_height * 0.53)

    curr_y = title_start_y
    title_fill = title_color if title_color else (255, 255, 255)
    for line in title_lines:
        bbox_l = draw.textbbox((0, 0), line, font=title_font)
        lw = bbox_l[2] - bbox_l[0]
        draw_3d_extruded_text(
            draw,
            (center_x - (lw // 2), curr_y),
            line,
            font=title_font,
            fill_color=title_fill,
            glow_color=primary_color,
            depth=6
        )
        curr_y += title_line_h

    # 10. Glowing Geometric Accent Divider
    curr_y += 10
    bar_width = min(int(max_text_width * 0.48), 260)
    bar_y = curr_y
    draw.line([(center_x - bar_width // 2, bar_y), (center_x + bar_width // 2, bar_y)], fill=primary_color + (230,), width=3)
    # Center diamond
    d_size = 5
    draw.polygon([
        (center_x, bar_y - d_size), (center_x + d_size, bar_y),
        (center_x, bar_y + d_size), (center_x - d_size, bar_y)
    ], fill=accent_color)
    curr_y += 22

    # 11. Subtitle / Tagline
    if subtitle and subtitle.strip():
        sub_size = int(22 * title_scale * (target_width / 900))
        sub_font = load_font(font_family, weight="regular", size=sub_size)
        sub_lines = wrap_text(draw, subtitle.strip(), sub_font, max_text_width - 30)
        test_sub = draw.textbbox((0, 0), "Aj", font=sub_font)
        sub_line_h = int((test_sub[3] - test_sub[1]) * 1.3)
        
        for sline in sub_lines[:2]:
            bbox_s = draw.textbbox((0, 0), sline, font=sub_font)
            sw = bbox_s[2] - bbox_s[0]
            # Soft shadow
            draw.text((center_x - (sw // 2) + 2, curr_y + 2), sline, font=sub_font, fill=(0, 0, 0, 220))
            draw.text((center_x - (sw // 2), curr_y), sline, font=sub_font, fill=(230, 240, 255))
            curr_y += sub_line_h
        curr_y += 12

    # 12. Event Details Card (Frosted Glass Pill)
    has_event_info = bool((date_text and date_text.strip()) or (venue_text and venue_text.strip()))
    
    if has_event_info:
        info_font_bold = load_font(font_family, weight="bold", size=int(18 * (target_width / 900)))
        card_w = min(max_text_width, 780)
        card_h = 76
        card_x1 = center_x - (card_w // 2)
        card_x2 = center_x + (card_w // 2)
        
        if text_placement == "Bottom":
            card_y1 = max(curr_y + 10, target_height - 215)
        elif text_placement == "Top":
            card_y1 = max(curr_y + 18, int(target_height * 0.42))
        else:
            card_y1 = max(curr_y + 18, int(target_height * 0.72))
            
        card_y2 = card_y1 + card_h

        # Frosted Glass Card with Gradient Rim
        draw.rounded_rectangle(
            [(card_x1, card_y1), (card_x2, card_y2)],
            radius=16,
            fill=(10, 16, 32, 225),
            outline=primary_color + (180,),
            width=2
        )
        
        if date_text and venue_text:
            col_mid = center_x
            draw.line([(col_mid, card_y1 + 12), (col_mid, card_y2 - 12)], fill=(255, 255, 255, 60), width=1)
            
            # Left: Date
            draw.text((card_x1 + 30, card_y1 + 14), date_text.strip().upper(), font=info_font_bold, fill=(255, 255, 255))
            draw.text((card_x1 + 30, card_y1 + 42), "📅 DATE & TIME", font=load_font(font_family, weight="bold", size=10), fill=primary_color)

            # Right: Venue
            draw.text((col_mid + 28, card_y1 + 14), venue_text.strip()[:35].upper(), font=info_font_bold, fill=(255, 255, 255))
            draw.text((col_mid + 28, card_y1 + 42), "📍 LOCATION & VENUE", font=load_font(font_family, weight="bold", size=10), fill=primary_color)
        else:
            single_text = (date_text or venue_text).strip().upper()
            bbox_st = draw.textbbox((0, 0), single_text, font=info_font_bold)
            stw = bbox_st[2] - bbox_st[0]
            draw.text((center_x - (stw // 2), card_y1 + 25), single_text, font=info_font_bold, fill=(255, 255, 255))

    # 13. VIP Ticket Barcode & Agency Branding in Footer
    footer_y = target_height - 68
    footer_font = load_font(font_family, weight="bold", size=int(12 * (target_width / 900)))
    
    # Draw graphic ticket barcode on bottom right
    barcode_x = target_width - safe_margin_x - 120
    draw_barcode(draw, barcode_x, footer_y - 20, width=110, height=26, color=(255, 255, 255, 170))
    draw.text((barcode_x, footer_y + 10), "VIP ACCESS #9924-A", font=load_font(font_family, weight="light", size=9), fill=primary_color)

    # Organizer billing block on bottom left / center
    if organizer_text and organizer_text.strip():
        org_line = f"PRODUCED & PRESENTED BY {organizer_text.strip().upper()}"
        draw.text((safe_margin_x, footer_y - 18), org_line, font=footer_font, fill=(210, 225, 245))

    if extra_details and extra_details.strip():
        ext_font = load_font(font_family, weight="light", size=int(11 * (target_width / 900)))
        ext_line = f"• {extra_details.strip().upper()} •"
        draw.text((safe_margin_x, footer_y + 3), ext_line[:65], font=ext_font, fill=primary_color)

    return composed.convert("RGB")


def export_poster_bytes(image: Image.Image, format: str = "PNG", dpi: int = 300) -> bytes:
    """Exports poster to high-res PNG or PDF byte buffer."""
    buf = io.BytesIO()
    if format.upper() == "PDF":
        image.save(buf, format="PDF", resolution=float(dpi))
    else:
        image.save(buf, format="PNG", dpi=(dpi, dpi), optimize=True)
    buf.seek(0)
    return buf.getvalue()
