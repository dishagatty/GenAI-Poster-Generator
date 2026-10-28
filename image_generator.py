"""
PromptPoster AI - Artwork Generator Module
Fully responsive AI image generation:
1. Online AI Text-to-Image Generation (Flux & Turbo models - Free, No API Key Required)
2. Curated High-Definition Studio Backdrops (Fallback if online AI is busy)
3. Custom Image Upload Support
4. Optional Hugging Face Inference API
"""

import os
import io
import time
import random
import urllib.parse
import logging
from typing import Optional, Dict, Any, Tuple
import requests
from PIL import Image, ImageEnhance

logger = logging.getLogger("PromptPosterAI.ImageGenerator")

# Path to local curated backgrounds
BACKDROPS_DIR = os.path.join(os.path.dirname(__file__), "assets", "backgrounds")

CATEGORY_BACKDROPS = {
    "Technology": "technology.jpg",
    "College Fest": "college_fest.jpg",
    "Gaming": "gaming.jpg",
    "Music": "music.jpg",
    "Movie": "movie.jpg",
    "Business": "business.jpg",
    "Awareness": "awareness.jpg"
}

AVAILABLE_MODELS = {
    "black-forest-labs/FLUX.1-schnell": {
        "name": "FLUX.1-schnell (Hosted API)",
        "provider": "fal-ai"
    },
    "stabilityai/stable-diffusion-xl-base-1.0": {
        "name": "Stable Diffusion XL 1.0 (Hosted API)",
        "provider": "hf-inference"
    }
}


def get_token_from_env() -> Optional[str]:
    """Retrieve optional Hugging Face API token from environment variables."""
    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
    if token and token.strip():
        return token.strip()
    return None


def verify_hf_token(token: str) -> Tuple[bool, str, Dict[str, Any]]:
    """Verifies optional Hugging Face token."""
    if not token or not token.strip():
        return False, "Token is empty.", {}
    try:
        resp = requests.get("https://huggingface.co/api/whoami-v2", headers={"Authorization": f"Bearer {token.strip()}"}, timeout=8)
        if resp.status_code == 200:
            return True, f"Connected as @{resp.json().get('name', 'User')}", resp.json()
        return False, f"Invalid token (HTTP {resp.status_code})", {}
    except Exception as e:
        return False, f"Network error: {str(e)}", {}


# ==============================================================================
# 🌟 FREE RESPONSIVE AI IMAGE GENERATOR (No Key Required)
# ==============================================================================

def generate_ai_pollinations(
    prompt: str,
    width: int = 768,
    height: int = 1024,
    timeout: int = 25
) -> Tuple[Optional[Image.Image], Optional[str]]:
    """
    Generates genuine AI artwork matching the user's prompt using Pollinations free endpoints.
    Tries 'flux' first, then 'turbo' model.
    """
    cleaned_prompt = prompt.strip()[:350]
    encoded_prompt = urllib.parse.quote(cleaned_prompt)
    seed = random.randint(1000, 9999999)
    
    # Try high-quality Flux model first, fallback to Turbo
    models_to_try = ["flux", "turbo"]
    last_err = ""

    for model_name in models_to_try:
        try:
            url = (
                f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                f"?model={model_name}&seed={seed}&width={width}&height={height}&nologo=true"
            )
            headers = {"User-Agent": "PromptPosterAI/2.0"}
            resp = requests.get(url, headers=headers, timeout=timeout)
            
            content_type = resp.headers.get("content-type", "").lower()
            if resp.status_code == 200 and ("image" in content_type or len(resp.content) > 10000):
                img = Image.open(io.BytesIO(resp.content))
                img.load()
                return img.convert("RGB"), None
            elif resp.status_code == 402:
                last_err = "Free queue cooldown in effect (1 request per 45s per IP)."
            else:
                last_err = f"AI service returned HTTP {resp.status_code}."
        except requests.exceptions.Timeout:
            last_err = f"Model '{model_name}' request timed out after {timeout}s."
        except Exception as ex:
            last_err = f"Connection error: {str(ex)}"

    return None, last_err


# ==============================================================================
# 🖼️ CURATED STUDIO ARTWORK (Instant & Offline)
# ==============================================================================

def get_curated_studio_backdrop(
    category: str = "Technology",
    theme_colors: Optional[Dict[str, Any]] = None,
    width: int = 900,
    height: int = 1200
) -> Image.Image:
    """Loads curated studio photographic backdrop for the category with theme grading."""
    filename = CATEGORY_BACKDROPS.get(category, "technology.jpg")
    file_path = os.path.join(BACKDROPS_DIR, filename)
    
    if os.path.exists(file_path):
        try:
            base_img = Image.open(file_path).convert("RGB")
        except Exception:
            base_img = Image.new("RGB", (width, height), (15, 23, 42))
    else:
        base_img = Image.new("RGB", (width, height), (15, 23, 42))
        
    if base_img.size != (width, height):
        base_img = base_img.resize((width, height), Image.Resampling.LANCZOS)

    if theme_colors:
        primary = theme_colors.get("primary_rgb", (0, 240, 255))
        enhancer = ImageEnhance.Color(base_img)
        base_img = enhancer.enhance(1.22)
        c_enhancer = ImageEnhance.Contrast(base_img)
        base_img = c_enhancer.enhance(1.15)
        
        tint_layer = Image.new("RGB", base_img.size, primary)
        base_img = Image.blend(base_img, tint_layer, alpha=0.08)

    return base_img


# ==============================================================================
# 🎨 MASTER GENERATOR: PROMPT-RESPONSIVE BY DEFAULT
# ==============================================================================

def generate_artwork(
    prompt: str,
    category: str = "Technology",
    style: str = "Cyberpunk",
    theme: str = "Neon",
    theme_colors: Optional[Dict[str, Any]] = None,
    mode: str = "ai_online",
    width: int = 900,
    height: int = 1200,
    hf_token: Optional[str] = None,
    hf_model: str = "black-forest-labs/FLUX.1-schnell"
) -> Tuple[Image.Image, str, bool]:
    """
    Generates background artwork based on user's exact prompt.
    Returns: (Image, engine_description_string, is_fallback_boolean)
    """
    # Option A: Hosted Hugging Face Token (if user specifically configured it)
    if mode == "hf_api" and hf_token and hf_token.strip():
        img, err = generate_image_hf(prompt, hf_token, hf_model, width=width, height=height)
        if img:
            return img, f"Hugging Face AI ({hf_model})", False
        logger.warning(f"HF API failed ({err}), falling back to AI generator...")

    # Option B: Responsive AI Generation (Default!)
    if mode == "ai_online":
        ai_img, err = generate_ai_pollinations(prompt, width=min(width, 768), height=min(height, 1024))
        if ai_img:
            return ai_img, "Generated with AI from your prompt", False
        else:
            logger.info(f"Online AI service unavailable ({err}). Using curated studio backdrop.")
            curated = get_curated_studio_backdrop(category, theme_colors, width, height)
            return curated, f"Curated Studio Art ({category}) — [AI in cooldown]", True

    # Option C: Curated Studio Artwork Mode
    curated = get_curated_studio_backdrop(category, theme_colors, width, height)
    return curated, f"Curated Studio Art ({category})", False


def generate_local_artwork(
    category: str = "Technology",
    style: str = "Cyberpunk",
    theme: str = "Neon",
    theme_colors: Optional[Dict[str, Any]] = None,
    width: int = 900,
    height: int = 1200
) -> Image.Image:
    """Backward compatibility wrapper."""
    return get_curated_studio_backdrop(category, theme_colors, width, height)


def generate_image_hf(
    prompt: str,
    token: str,
    model_id: str = "black-forest-labs/FLUX.1-schnell",
    width: int = 768,
    height: int = 1024,
    timeout: int = 50
) -> Tuple[Optional[Image.Image], Optional[str]]:
    """Optional Hugging Face Inference API call."""
    if not token or not token.strip():
        return None, "No token provided."
    headers = {
        "Authorization": f"Bearer {token.strip()}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": prompt}
    endpoint = f"https://api-inference.huggingface.co/models/{model_id}"
    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
        if resp.status_code == 200 and len(resp.content) > 1000:
            return Image.open(io.BytesIO(resp.content)), None
        return None, f"HTTP {resp.status_code}: {resp.text[:120]}"
    except Exception as e:
        return None, str(e)
