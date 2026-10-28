"""
PromptPoster AI - Self-Testing & Pipeline Verification Script
Validates prompt enhancement, composition pipeline, typography, and PDF/PNG export.
"""

import sys
import os
from PIL import Image, ImageDraw

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_tests():

    print("==================================================")
    print("PromptPoster AI — Automated Verification Suite")
    print("==================================================")

    # 1. Test Utils & Prompt Enhancement
    print("\n[1/4] Testing utils.py (Prompt Validation & Enhancement)...")
    import utils
    
    val_ok, msg = utils.validate_user_prompt("Create an AI poster")
    assert val_ok, f"Validation failed unexpectedly: {msg}"
    
    val_bad, msg = utils.validate_user_prompt("   ")
    assert not val_bad, "Empty prompt should be invalid"
    
    enhanced = utils.enhance_prompt(
        base_prompt="Futuristic city with flying cars",
        category="Technology",
        style="Cyberpunk",
        theme="Neon"
    )
    print(f"  -> Enhanced Prompt: {enhanced[:80]}...")
    assert "futuristic" in enhanced.lower() or "cyberpunk" in enhanced.lower()
    print("  ✓ utils.py passed all tests!")

    # 2. Test Image Generator Module (Local Generative Engine)
    print("\n[2/4] Testing image_generator.py (100% Offline Engine)...")
    import image_generator
    local_bg = image_generator.generate_local_artwork(
        category="Technology",
        style="Cyberpunk",
        theme="Neon",
        theme_colors=utils.THEME_MODIFIERS["Neon"],
        width=900,
        height=1200
    )
    assert local_bg is not None and local_bg.size == (900, 1200)
    print("  ✓ image_generator.py local generative engine verified!")

    # 3. Test Graphic Poster Composer Pipeline
    print("\n[3/4] Testing poster_composer.py (Image Processing & Typography)...")
    import poster_composer
    synthetic_bg = local_bg

    
    theme_info = utils.THEME_MODIFIERS["Neon"]
    
    composed_poster = poster_composer.compose_final_poster(
        background_image=synthetic_bg,
        title="NEUROHACK 2025",
        subtitle="National AI & Robotics Hackathon",
        category="Technology",
        date_text="OCTOBER 28-30, 2025",
        venue="Cyber Arena & Metaverse",
        organizer="Department of AI & Data Science",
        extra_details="Prizes Worth $25,000 | 48-Hour Coding Marathon",
        target_width=900,
        target_height=1200,
        font_family="Modern Sans (Segoe UI)",
        theme_colors=theme_info,
        text_placement="Bottom",
        overlay_intensity=0.55,
        frame_style="Cyberpunk Brackets",
        apply_vignette_effect=True
    )
    
    assert composed_poster.size == (900, 1200), f"Unexpected size: {composed_poster.size}"
    print(f"  ✓ Composed poster generated with size: {composed_poster.size}")

    # 4. Test Export (PNG and PDF)
    print("\n[4/4] Testing high-res export (PNG & PDF)...")
    png_bytes = poster_composer.export_poster_bytes(composed_poster, format="PNG", dpi=300)
    assert len(png_bytes) > 10000, "PNG export generated unexpectedly small buffer"
    print(f"  ✓ High-res PNG generated: {len(png_bytes) / 1024:.1f} KB")

    pdf_bytes = poster_composer.export_poster_bytes(composed_poster, format="PDF", dpi=300)
    assert len(pdf_bytes) > 10000, "PDF export generated unexpectedly small buffer"
    print(f"  ✓ Print-ready PDF generated: {len(pdf_bytes) / 1024:.1f} KB")

    # Save a verification test poster
    os.makedirs("test_output", exist_ok=True)
    test_poster_path = os.path.join("test_output", "verification_test_poster.png")
    composed_poster.save(test_poster_path)
    print(f"  ✓ Saved visual verification poster to: {test_poster_path}")

    print("\n==================================================")
    print("ALL TESTS PASSED! PromptPoster AI pipeline is 100% operational.")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
