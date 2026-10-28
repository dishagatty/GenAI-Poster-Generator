"""
PromptPoster AI - Streamlit Web Application
A modern, visually captivating AI poster generation studio.
Works 100% locally and instantaneously without any API key or external accounts required!
"""

import os
import time
import importlib
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
from PIL import Image

# Load optional environment variables from .env
load_dotenv()

# Import project modules
import utils
import image_generator
import poster_composer

# Ensure submodules are always freshly reloaded in Streamlit
importlib.reload(utils)
importlib.reload(image_generator)
importlib.reload(poster_composer)


# Set Streamlit Page Configuration
st.set_page_config(
    page_title="PromptPoster AI — AI Poster Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Modern CSS Design System
CUSTOM_CSS = """
<style>
/* Base Theme & Background */
.stApp {
    background: radial-gradient(circle at 15% 15%, #0d1326 0%, #070a13 55%, #05070d 100%) !important;
    color: #e2e8f0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Glassmorphic Container Cards */
.glass-card {
    background: rgba(18, 25, 44, 0.65);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: rgba(99, 102, 241, 0.35);
    box-shadow: 0 12px 35px rgba(99, 102, 241, 0.15);
}

/* Header & Typography */
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 20%, #a5b4fc 60%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
    line-height: 1.15;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    margin-bottom: 20px;
}

.badge-tag {
    display: inline-block;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 20px;
    background: rgba(99, 102, 241, 0.18);
    color: #818cf8;
    border: 1px solid rgba(99, 102, 241, 0.3);
    margin-bottom: 12px;
}

.badge-local {
    display: inline-block;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 20px;
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
    margin-bottom: 12px;
}

/* Form Section Headers */
.section-heading {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-top: 10px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 8px;
}

/* Primary Action Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #3b82f6 50%, #06b6d4 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(99, 102, 241, 0.6) !important;
}

/* Download Buttons */
.stDownloadButton > button {
    background: rgba(30, 41, 69, 0.8) !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
}

.stDownloadButton > button:hover {
    background: rgba(56, 189, 248, 0.15) !important;
    border-color: #38bdf8 !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #090e1a !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}

.status-box-offline {
    padding: 10px 14px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 10px;
    color: #34d399;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 12px;
}

/* ============================================================== */
/* HIGH-CONTRAST INPUT FIELDS, TEXTAREAS & LABELS (FIX FONT COLOR) */
/* ============================================================== */
.stTextArea textarea, 
.stTextInput input,
[data-baseweb="textarea"] textarea,
[data-baseweb="input"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input {
    background-color: #0b1120 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
    border: 1.5px solid rgba(99, 102, 241, 0.45) !important;
    border-radius: 12px !important;
    padding: 12px 14px !important;
    caret-color: #00f0ff !important;
}

/* Focus and Active States */
.stTextArea textarea:focus, 
.stTextInput input:focus,
[data-baseweb="textarea"]:focus-within,
[data-baseweb="input"]:focus-within {
    background-color: #0f172a !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border-color: #00f0ff !important;
    box-shadow: 0 0 0 3px rgba(0, 240, 255, 0.25) !important;
}

/* BaseWeb container wrapping */
[data-baseweb="textarea"], 
[data-baseweb="input"], 
[data-baseweb="base-input"] {
    background-color: #0b1120 !important;
    border-radius: 12px !important;
}

/* Placeholder visibility */
.stTextArea textarea::placeholder, 
.stTextInput input::placeholder {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    opacity: 0.85 !important;
}

/* Labels and Field titles */
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] p,
.stSelectbox label p,
.stSlider label p,
.stCheckbox label span,
[data-testid="stWidgetLabel"] span {
    color: #f8fafc !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    margin-bottom: 6px !important;
}

/* Selectbox dropdowns */
[data-baseweb="select"] > div {
    background-color: #0b1120 !important;
    color: #ffffff !important;
    border: 1.5px solid rgba(99, 102, 241, 0.4) !important;
    border-radius: 12px !important;
}
[data-baseweb="select"] * {
    color: #ffffff !important;
}

/* Hide Streamlit default hamburger & footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# Initialize Session State
if "generated_bg" not in st.session_state:
    st.session_state.generated_bg = None
if "final_poster" not in st.session_state:
    st.session_state.final_poster = None
if "last_enhanced_prompt" not in st.session_state:
    st.session_state.last_enhanced_prompt = ""
if "generation_metadata" not in st.session_state:
    st.session_state.generation_metadata = {}
if "preset_selected" not in st.session_state:
    st.session_state.preset_selected = None


# Sidebar: Studio Engine & Artwork Settings
with st.sidebar:
    st.markdown("### 🎨 PromptPoster AI")
    st.markdown("<div class='badge-local'>⚡ 100% OFFLINE READY</div>", unsafe_allow_html=True)
    
    st.markdown(
        "<div class='status-box-offline'>🟢 Local Engine Active<br><span style='font-size:0.75rem; color:#a7f3d0;'>No API key required • Zero latency • Unlimited generations</span></div>",
        unsafe_allow_html=True
    )

    st.markdown("#### ⚙️ Background Engine")
    engine_mode = st.radio(
        "Source Mode",
        options=[
            "✨ AI Text-to-Image Generation (Free • Generates from your prompt)",
            "🌟 Curated Studio Backdrops (Instant & Offline)",
            "📁 Upload Custom Artwork / Image",
            "🌐 Optional Hosted Hugging Face API"
        ],
        index=0,
        help="AI Text-to-Image Generation creates brand new original artwork directly from whatever prompt you type!"
    )


    uploaded_file = None
    api_token = ""
    api_model = "black-forest-labs/FLUX.1-schnell"

    if "Upload Custom" in engine_mode:
        uploaded_file = st.file_uploader("Upload background image (PNG / JPG)", type=["png", "jpg", "jpeg", "webp"])
        if uploaded_file:
            st.success("Image uploaded successfully!")


    elif "Hosted Hugging Face" in engine_mode:
        st.markdown("##### Optional API Settings")
        env_tok = image_generator.get_token_from_env() or ""
        api_token = st.text_input("HF Access Token", value=env_tok, type="password")
        api_model = st.selectbox(
            "Model",
            options=list(image_generator.AVAILABLE_MODELS.keys()),
            format_func=lambda m: image_generator.AVAILABLE_MODELS[m]["name"],
            index=0
        )
        if api_token:
            if st.button("Test Token", use_container_width=True):
                ok, msg, _ = image_generator.verify_hf_token(api_token)
                if ok:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")

    st.markdown("---")
    st.markdown("#### 📐 Quality Settings")
    export_dpi = st.select_slider("Print Quality (DPI)", options=[150, 300, 600], value=300)
    st.caption("PromptPoster AI • Windows & Python 3.12 • No GPU or API Token Required")


# Main Application Tabs
tab_studio, tab_docs = st.tabs(["🎨 Poster Studio", "📖 Architecture & How It Works"])


with tab_studio:
    # Hero Title Bar
    st.markdown("<div class='badge-tag'>INSTANT GRAPHIC POSTER ENGINE</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='hero-title'>PromptPoster AI</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='hero-subtitle'>Turn prompts into professional, artistic posters with high-contrast graphic typography, glassmorphism badges, and dynamic styling — <b>instantly and without any API keys!</b></p>",
        unsafe_allow_html=True
    )

    # Quick Example Presets (Chips)
    st.markdown("<div class='section-heading'>💡 One-Click Preset Inspirations</div>", unsafe_allow_html=True)
    
    preset_cols = st.columns(len(utils.EXAMPLE_PRESETS))
    for idx, preset in enumerate(utils.EXAMPLE_PRESETS):
        with preset_cols[idx]:
            if st.button(preset["label"], key=f"preset_btn_{idx}", use_container_width=True):
                st.session_state.preset_selected = preset

    # Determine default values (from selected preset or defaults)
    p_data = st.session_state.preset_selected or utils.EXAMPLE_PRESETS[0]

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Main Input Layout in Two Master Columns
    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        st.markdown("<div class='section-heading'>1. 🎨 Visual Background Prompt</div>", unsafe_allow_html=True)
        
        prompt_input = st.text_area(
            "Describe the poster theme & visual scene:",
            value=p_data["prompt"],
            height=110,
            placeholder="e.g. Create a futuristic AI hackathon poster with neon blue lighting, a robotic face, and a cyberpunk background..."
        )

        enhance_toggle = st.checkbox("✨ Automatically Enhance Prompt with Pro Visual Cues", value=True)

        st.markdown("<div class='section-heading'>2. 📝 Poster Typography & Event Details</div>", unsafe_allow_html=True)
        
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            title_input = st.text_input("Poster Title", value=p_data["title"])
        with t_col2:
            subtitle_input = st.text_input("Subtitle / Tagline", value=p_data["subtitle"])

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            date_input = st.text_input("Date & Time", value=p_data["date"])
        with d_col2:
            venue_input = st.text_input("Venue / Location", value=p_data["venue"])

        o_col1, o_col2 = st.columns(2)
        with o_col1:
            organizer_input = st.text_input("Organizer / Presented By", value=p_data["organizer"])
        with o_col2:
            extra_input = st.text_input("Additional Highlights / Badges", value=p_data["extra"])

    with col_right:
        st.markdown("<div class='section-heading'>3. 🎭 Style & Poster Design Controls</div>", unsafe_allow_html=True)
        
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            category_list = list(utils.CATEGORY_MODIFIERS.keys())
            cat_default_idx = category_list.index(p_data["category"]) if p_data["category"] in category_list else 0
            selected_category = st.selectbox("Category", options=category_list, index=cat_default_idx)
            
            style_list = list(utils.STYLE_MODIFIERS.keys())
            style_default_idx = style_list.index(p_data["style"]) if p_data["style"] in style_list else 0
            selected_style = st.selectbox("Aesthetic Style", options=style_list, index=style_default_idx)

        with c_col2:
            theme_list = list(utils.THEME_MODIFIERS.keys())
            theme_default_idx = theme_list.index(p_data["theme"]) if p_data["theme"] in theme_list else 0
            selected_theme = st.selectbox("Color Palette", options=theme_list, index=theme_default_idx)

            ratio_list = list(utils.ASPECT_RATIOS.keys())
            ratio_default_idx = ratio_list.index(p_data.get("ratio", "Portrait")) if p_data.get("ratio") in ratio_list else 0
            selected_ratio = st.selectbox("Aspect Ratio", options=ratio_list, index=ratio_default_idx)

        st.markdown("<div class='section-heading'>4. 📐 Layout & Composition Fine-Tuning</div>", unsafe_allow_html=True)
        
        l_col1, l_col2 = st.columns(2)
        with l_col1:
            text_placement = st.selectbox(
                "Text Placement Anchor",
                options=["Bottom", "Center", "Top"],
                index=0,
                help="'Bottom' is the classic movie/event poster composition where artwork leads at the top."
            )
            font_choice = st.selectbox(
                "Typography Font",
                options=list(poster_composer.FONT_MAP.keys()),
                index=0
            )
            title_color_choice = st.selectbox(
                "Title Font Color",
                options=[
                    "⚪ Crisp White",
                    "⚡ Theme Accent Glow",
                    "🟡 Electric Gold",
                    "🔵 Neon Cyan",
                    "🔴 Crimson Red",
                    "🟢 Emerald Green",
                    "🟣 Neon Magenta"
                ],
                index=0,
                help="Choose the color of the main poster title."
            )
            TITLE_COLOR_MAP = {
                "⚪ Crisp White": (255, 255, 255),
                "⚡ Theme Accent Glow": None,
                "🟡 Electric Gold": (255, 215, 0),
                "🔵 Neon Cyan": (0, 240, 255),
                "🔴 Crimson Red": (255, 68, 68),
                "🟢 Emerald Green": (16, 185, 129),
                "🟣 Neon Magenta": (255, 0, 128)
            }
            selected_title_color = TITLE_COLOR_MAP[title_color_choice]


        with l_col2:
            frame_choice = st.selectbox(
                "Border / Frame Style",
                options=["Modern Minimalist", "Cyberpunk Brackets", "Double Luxury Frame", "None"],
                index=0
            )
            overlay_opacity = st.slider(
                "Background Overlay Intensity",
                min_value=0.20,
                max_value=0.85,
                value=0.55,
                step=0.05,
                help="Controls readability overlay behind text."
            )

        vignette_toggle = st.checkbox("Apply Cinematic Radial Vignette", value=True)

    # Master Action Area
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    generate_col, adjust_col = st.columns([1.5, 1])

    with generate_col:
        generate_clicked = st.button("🚀 Generate AI Poster", use_container_width=True)

    with adjust_col:
        recompose_clicked = st.button("🔄 Recompose with Current Settings", use_container_width=True, 
                                     help="Updates text, fonts, colors, and layout instantly.")

    # Execution Logic
    if generate_clicked:
        # Validate Prompt
        is_valid, val_err = utils.validate_user_prompt(prompt_input)
        if not is_valid:
            st.error(f"⚠️ Validation Error: {val_err}")
        else:
            # Enhance Prompt if enabled
            if enhance_toggle:
                final_prompt = utils.enhance_prompt(
                    base_prompt=prompt_input,
                    category=selected_category,
                    style=selected_style,
                    theme=selected_theme
                )
            else:
                final_prompt = prompt_input.strip()

            st.session_state.last_enhanced_prompt = final_prompt
            
            # Dimensions based on aspect ratio
            ratio_info = utils.ASPECT_RATIOS[selected_ratio]
            target_w = ratio_info["width"]
            target_h = ratio_info["height"]
            theme_info = utils.THEME_MODIFIERS[selected_theme]

            progress_bar = st.progress(0, text="Creating background artwork...")
            start_time = time.time()

            try:
                raw_img = None
                engine_desc = "AI Generated Artwork"
                is_fallback = False

                
                # Check Engine Mode
                if "Upload Custom" in engine_mode:
                    if uploaded_file is not None:
                        raw_img = Image.open(uploaded_file).convert("RGB")
                        engine_desc = "Custom Uploaded Artwork"
                    else:
                        st.info("ℹ️ No file uploaded; generating matching backdrop.")
                        raw_img, engine_desc, is_fallback = image_generator.generate_artwork(
                            prompt=final_prompt,
                            category=selected_category,
                            style=selected_style,
                            theme=selected_theme,
                            theme_colors=theme_info,
                            mode="curated",
                            width=target_w,
                            height=target_h
                        )
                elif "Curated Studio Backdrops" in engine_mode:
                    progress_bar.progress(35, text="Loading studio-grade backdrop...")
                    raw_img, engine_desc, is_fallback = image_generator.generate_artwork(
                        prompt=final_prompt,
                        category=selected_category,
                        style=selected_style,
                        theme=selected_theme,
                        theme_colors=theme_info,
                        mode="curated",
                        width=target_w,
                        height=target_h
                    )
                elif "Hosted Hugging Face" in engine_mode and api_token:
                    progress_bar.progress(30, text=f"Requesting hosted model '{api_model}'...")
                    raw_img, engine_desc, is_fallback = image_generator.generate_artwork(
                        prompt=final_prompt,
                        category=selected_category,
                        style=selected_style,
                        theme=selected_theme,
                        theme_colors=theme_info,
                        mode="hf_api",
                        width=target_w,
                        height=target_h,
                        hf_token=api_token,
                        hf_model=api_model
                    )
                else:
                    # Default: Generates from the user's prompt!
                    progress_bar.progress(30, text="Synthesizing original AI artwork from your prompt...")
                    raw_img, engine_desc, is_fallback = image_generator.generate_artwork(
                        prompt=final_prompt,
                        category=selected_category,
                        style=selected_style,
                        theme=selected_theme,
                        theme_colors=theme_info,
                        mode="ai_online",
                        width=target_w,
                        height=target_h
                    )

                progress_bar.progress(70, text="Composing 3D typography, badges, and layout...")
                st.session_state.generated_bg = raw_img

                # Master Graphic Typography Composition
                composed = poster_composer.compose_final_poster(
                    background_image=raw_img,
                    title=title_input,
                    subtitle=subtitle_input,
                    category=selected_category,
                    date_text=date_input,
                    venue_text=venue_input,
                    organizer_text=organizer_input,
                    extra_details=extra_input,
                    target_width=target_w,
                    target_height=target_h,
                    font_family=font_choice,
                    theme_colors=theme_info,
                    text_placement=text_placement,
                    overlay_intensity=overlay_opacity,
                    frame_style=frame_choice,
                    apply_vignette_effect=vignette_toggle,
                    title_color=selected_title_color
                )

                st.session_state.final_poster = composed
                elapsed = time.time() - start_time
                progress_bar.progress(100, text=f"✨ Done in {elapsed:.2f}s!")
                time.sleep(0.3)
                progress_bar.empty()

                # Metadata
                st.session_state.generation_metadata = {
                    "engine": engine_desc,
                    "dimensions": f"{target_w}x{target_h}",
                    "ratio": selected_ratio,
                    "elapsed": f"{elapsed:.2f}s",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                if is_fallback:
                    st.info("ℹ️ Free AI queue is currently cooling down (15s). Composed with matching category art. Click 'Generate AI Poster' again in a few moments for new AI generation!")
                else:
                    st.success(f"🎉 Original AI poster generated from your prompt in {elapsed:.2f}s!")


            except Exception as ex:
                progress_bar.empty()
                st.error(f"An error occurred: {str(ex)}")

    # Fast Recomposition
    elif recompose_clicked:
        if st.session_state.generated_bg is None:
            # Generate default artwork if not exists
            ratio_info = utils.ASPECT_RATIOS[selected_ratio]
            target_w = ratio_info["width"]
            target_h = ratio_info["height"]
            theme_info = utils.THEME_MODIFIERS[selected_theme]
            st.session_state.generated_bg = image_generator.generate_local_artwork(
                category=selected_category,
                style=selected_style,
                theme=selected_theme,
                theme_colors=theme_info,
                width=target_w,
                height=target_h
            )

        with st.spinner("Recomposing poster with updated settings..."):
            ratio_info = utils.ASPECT_RATIOS[selected_ratio]
            target_w = ratio_info["width"]
            target_h = ratio_info["height"]
            theme_info = utils.THEME_MODIFIERS[selected_theme]

            composed = poster_composer.compose_final_poster(
                background_image=st.session_state.generated_bg,
                title=title_input,
                subtitle=subtitle_input,
                category=selected_category,
                date_text=date_input,
                venue_text=venue_input,
                organizer_text=organizer_input,
                extra_details=extra_input,
                target_width=target_w,
                target_height=target_h,
                font_family=font_choice,
                theme_colors=theme_info,
                text_placement=text_placement,
                overlay_intensity=overlay_opacity,
                frame_style=frame_choice,
                apply_vignette_effect=vignette_toggle,
                title_color=selected_title_color
            )
            st.session_state.final_poster = composed
            st.success("✨ Poster updated with new typography and styling!")



    # Results & Showcase Display
    if st.session_state.final_poster is not None:
        st.markdown("---")
        st.markdown("<div class='section-heading'>🖼️ Poster Showcase & Export</div>", unsafe_allow_html=True)

        preview_tab_composed, preview_tab_split = st.tabs(["🌟 Composed Final Poster", "🔄 Side-by-Side Comparison"])

        with preview_tab_composed:
            p_col1, p_col2, p_col3 = st.columns([1, 2.4, 1])
            with p_col2:
                st.image(
                    st.session_state.final_poster,
                    caption=f"Final Poster — {title_input} ({st.session_state.generation_metadata.get('dimensions', '')})",
                    use_container_width=True
                )

        with preview_tab_split:
            cmp_col1, cmp_col2 = st.columns(2)
            with cmp_col1:
                st.markdown("#### 1. Background Artwork")
                if st.session_state.generated_bg:
                    st.image(st.session_state.generated_bg, caption="Generative Artwork Canvas", use_container_width=True)
            with cmp_col2:
                st.markdown("#### 2. Composed Typography Poster")
                st.image(st.session_state.final_poster, caption="Composed with Pillow graphic pipeline", use_container_width=True)

        # Download Actions
        st.markdown("#### 📥 Download Your Poster")
        dl_col1, dl_col2, dl_col3 = st.columns(3)

        png_bytes = poster_composer.export_poster_bytes(st.session_state.final_poster, format="PNG", dpi=export_dpi)
        pdf_bytes = poster_composer.export_poster_bytes(st.session_state.final_poster, format="PDF", dpi=export_dpi)

        filename_base = f"poster_{title_input.lower().replace(' ', '_')[:20]}_{int(time.time())}"

        with dl_col1:
            st.download_button(
                label=f"📥 Download PNG ({export_dpi} DPI)",
                data=png_bytes,
                file_name=f"{filename_base}.png",
                mime="image/png",
                use_container_width=True
            )

        with dl_col2:
            st.download_button(
                label="📄 Download PDF (Print Ready)",
                data=pdf_bytes,
                file_name=f"{filename_base}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with dl_col3:
            raw_png_bytes = poster_composer.export_poster_bytes(st.session_state.generated_bg, format="PNG", dpi=150)
            st.download_button(
                label="🖼️ Download Background Only",
                data=raw_png_bytes,
                file_name=f"{filename_base}_bg.png",
                mime="image/png",
                use_container_width=True
            )

        # Technical Metadata Expander
        with st.expander("🔍 Generation Technical Diagnostics"):
            meta = st.session_state.generation_metadata
            st.json({
                "Engine": meta.get("engine", "Built-in Generative Studio"),
                "Dimensions": meta.get("dimensions", ""),
                "DPI": export_dpi,
                "Generation Time": meta.get("elapsed", ""),
                "Timestamp": meta.get("timestamp", "")
            })


with tab_docs:
    st.markdown("## 📖 PromptPoster AI Architecture")
    st.markdown(
        """
        ### 1. How It Works (100% Offline & Instant)
        PromptPoster AI creates stunning event, festival, tech, and movie posters without requiring any external API keys or GPU compute:
        
        - **Generative Background Synthesis:** Uses NumPy, Pillow, and OpenCV to algorithmically compose category-specific background elements (cyberpunk perspective grids, cosmic nebulae, concert stage lights, aurora ribbons, and geometric glass refraction planes).
        - **Precision Typography Engine:** Uses Python Pillow to render flawless, high-contrast text with word-wrapping, multi-pass drop shadows, neon rim glows, and Windows TrueType fonts.
        - **Frosted Glass Cards:** Renders translucent badge containers and 2-column event date/venue cards.
        - **300 DPI High-Res Export:** Saves directly to print-ready PDF and uncompressed PNG.

        ---

        ### 2. How to Run
        ```powershell
        # Double click run.bat OR execute in PowerShell:
        .\\venv\\Scripts\\streamlit run app.py
        ```
        """
    )
