"""
PromptPoster AI - Utilities and Prompt Engineering Module
Handles prompt validation, visual enhancement, style presets, and metadata formatting.
"""

from typing import Dict, Any, Tuple, List
import re

# Curated Category Enhancements
CATEGORY_MODIFIERS: Dict[str, Dict[str, str]] = {
    "Technology": {
        "visual": "futuristic technology, holographic HUD elements, clean circuits, glowing data streams, sleek tech aesthetic, cutting edge innovation",
        "lighting": "volumetric cyan and violet neon lighting, crisp reflections",
        "composition": "dynamic perspective, modern tech aesthetic, 8k resolution, octane render quality",
        "default_badge": "TECH INNOVATION"
    },
    "College Fest": {
        "visual": "vibrant celebration, energetic crowd silhouette, stage festival lights, dynamic colorful confetti, abstract celebration shapes",
        "lighting": "radiant party beams, prism flare, warm and vibrant glow",
        "composition": "energetic composition, festive atmosphere, celebratory poster artwork",
        "default_badge": "ANNUAL CULTURAL FEST"
    },
    "Gaming": {
        "visual": "esports battle arena, futuristic cyber armor, glowing energy weapons, dark atmospheric sci-fi scene, game concept art",
        "lighting": "high contrast neon edge lighting, dramatic backlight, volumetric fog",
        "composition": "cinematic action pose, unreal engine 5 style, hyper-detailed digital art",
        "default_badge": "CHAMPIONSHIP ARENA"
    },
    "Music": {
        "visual": "live concert stage, musical soundwaves, dramatic spotlight, smoke and laser beams, acoustic or electronic music festival vibe",
        "lighting": "moody concert lighting, ultraviolet glow, dramatic silhouette",
        "composition": "album cover art composition, deep atmosphere, cinematic festival poster",
        "default_badge": "LIVE IN CONCERT"
    },
    "Movie": {
        "visual": "hollywood cinematic film still, dramatic hero composition, depth of field, blockbuster movie atmosphere",
        "lighting": "dramatic key lighting, anamorphic lens flare, moody color grading, film noir contrast",
        "composition": "epic 35mm film still composition, masterpiece, photorealistic details",
        "default_badge": "PREMIERE RELEASE"
    },
    "Business": {
        "visual": "modern corporate elegance, abstract geometric glass structures, financial district architectural reflections, executive summit",
        "lighting": "clean ambient corporate lighting, soft shadows, golden hour glass highlights",
        "composition": "sophisticated minimalist layout, professional keynote presentation backdrop",
        "default_badge": "GLOBAL SUMMIT"
    },
    "Awareness": {
        "visual": "evocative natural world, lush green forests, pristine ocean, planet earth, hopeful emotional symbol",
        "lighting": "majestic golden sunlight, natural radiant illumination, soft morning mist",
        "composition": "powerful emotional environmental poster, high-impact visual storytelling",
        "default_badge": "PUBLIC INITIATIVE"
    }
}

# Curated Art Styles
STYLE_MODIFIERS: Dict[str, str] = {
    "Cyberpunk": "cyberpunk genre, neo-tokyo aesthetics, glowing neon tubes, rain-slicked chrome reflections, dark futuristic city",
    "Minimalist": "minimalist art, clean lines, vast negative space, elegant geometry, modern bauhaus influence, refined simplicity",
    "Cinematic": "cinematic movie poster aesthetics, 35mm film grain, moody cinematic depth of field, epic scope, IMAX visual style",
    "Retro": "retro 80s synthwave aesthetics, vintage halftone textures, vaporwave sunset grid, nostalgic chrome gradients",
    "Futuristic": "futuristic sci-fi world, utopian sleek architecture, aerodynamic forms, advanced quantum tech, white and chrome aesthetic",
    "Surreal": "surrealist masterpiece, dreamlike floating elements, paradoxical architecture, salvador dali inspired, mysterious symbolism",
    "Artistic": "painterly expressive brushstrokes, dynamic digital illustration, impasto textures, vivid artistic expression"
}

# Curated Color Themes
THEME_MODIFIERS: Dict[str, Dict[str, Any]] = {
    "Neon": {
        "prompt": "neon cyan, electric magenta, vibrant ultraviolet glow against deep midnight dark background",
        "primary_rgb": (0, 240, 255),
        "secondary_rgb": (255, 0, 128),
        "accent_rgb": (180, 70, 255),
        "text_color": (255, 255, 255),
        "badge_bg": (10, 15, 30, 200),
        "overlay_tint": (5, 10, 25)
    },
    "Warm": {
        "prompt": "warm amber, sunset orange, rich crimson, golden hour glow and deep mahogany tones",
        "primary_rgb": (255, 140, 0),
        "secondary_rgb": (255, 60, 40),
        "accent_rgb": (255, 215, 0),
        "text_color": (255, 255, 255),
        "badge_bg": (30, 15, 10, 200),
        "overlay_tint": (25, 10, 5)
    },
    "Cool": {
        "prompt": "cool arctic blue, frosty cyan, deep sapphire navy, crystalline turquoise lighting",
        "primary_rgb": (50, 190, 255),
        "secondary_rgb": (90, 120, 255),
        "accent_rgb": (160, 230, 255),
        "text_color": (255, 255, 255),
        "badge_bg": (10, 20, 35, 200),
        "overlay_tint": (5, 15, 30)
    },
    "Pastel": {
        "prompt": "soft pastel lavender, mint green, peach and powdery sky blue, gentle dreamy light",
        "primary_rgb": (230, 180, 250),
        "secondary_rgb": (175, 225, 200),
        "accent_rgb": (255, 210, 190),
        "text_color": (255, 255, 255),
        "badge_bg": (25, 20, 35, 200),
        "overlay_tint": (20, 15, 30)
    },
    "Monochrome": {
        "prompt": "high contrast black and white, dramatic noir chiaroscuro, pure silver and obsidian shadows",
        "primary_rgb": (240, 240, 240),
        "secondary_rgb": (180, 180, 180),
        "accent_rgb": (255, 255, 255),
        "text_color": (255, 255, 255),
        "badge_bg": (15, 15, 15, 210),
        "overlay_tint": (10, 10, 10)
    },
    "Vibrant": {
        "prompt": "saturated electric colors, radiant rainbow spectrum, intense contrast, energetic luminous palette",
        "primary_rgb": (255, 75, 130),
        "secondary_rgb": (0, 220, 180),
        "accent_rgb": (255, 220, 50),
        "text_color": (255, 255, 255),
        "badge_bg": (20, 15, 30, 200),
        "overlay_tint": (15, 10, 25)
    }
}

# Aspect Ratio Dimensions
ASPECT_RATIOS: Dict[str, Dict[str, Any]] = {
    "Portrait": {
        "ratio_str": "3:4",
        "width": 900,
        "height": 1200,
        "hf_width": 768,
        "hf_height": 1024,
        "description": "Standard Event & Movie Poster (3:4 ratio)"
    },
    "Square": {
        "ratio_str": "1:1",
        "width": 1080,
        "height": 1080,
        "hf_width": 1024,
        "hf_height": 1024,
        "description": "Social Media & Album Art (1:1 ratio)"
    },
    "Landscape": {
        "ratio_str": "16:9",
        "width": 1280,
        "height": 720,
        "hf_width": 1024,
        "hf_height": 576,
        "description": "Digital Display & Billboard (16:9 ratio)"
    }
}

# Example Prompts for One-Click User Testing
EXAMPLE_PRESETS: List[Dict[str, str]] = [
    {
        "label": "🤖 Cyber Hackathon 2025",
        "prompt": "Create a futuristic AI hackathon poster with neon blue lighting, a robotic face, and a cyberpunk background.",
        "category": "Technology",
        "style": "Cyberpunk",
        "theme": "Neon",
        "ratio": "Portrait",
        "title": "NEUROHACK 2025",
        "subtitle": "National AI & Robotics Hackathon",
        "date": "OCTOBER 28-30, 2025",
        "venue": "Cyber Arena & Virtual Metaverse",
        "organizer": "Department of AI & Data Science",
        "extra": "Prizes Worth $25,000 | 48-Hour Coding Marathon"
    },
    {
        "label": "🎉 College Cultural Fest",
        "prompt": "Design a vibrant college cultural festival poster with colorful lights, music, and energetic abstract shapes.",
        "category": "College Fest",
        "style": "Artistic",
        "theme": "Vibrant",
        "ratio": "Portrait",
        "title": "EUPHORIA '25",
        "subtitle": "Unleash The Rhythm, Ignite The Night",
        "date": "NOVEMBER 15-17, 2025",
        "venue": "Grand Open Amphitheatre, Campus North",
        "organizer": "Student Cultural Council",
        "extra": "Battle of Bands • Dance Off • Fashion Gala • Food Carnival"
    },
    {
        "label": "🌱 Green Planet Awareness",
        "prompt": "Create an environmental awareness poster showing a green planet surrounded by lush forests and pure water.",
        "category": "Awareness",
        "style": "Cinematic",
        "theme": "Warm",
        "ratio": "Portrait",
        "title": "EARTH PULSE",
        "subtitle": "Preserve Our Planet, Protect Our Tomorrow",
        "date": "WORLD ENVIRONMENT DAY",
        "venue": "Global Action Campaign",
        "organizer": "EcoFuture Alliance",
        "extra": "Plant 10,000 Trees • Zero Waste Initiative • Join The Movement"
    },
    {
        "label": "🚀 Sci-Fi Odyssey Movie",
        "prompt": "Design a cinematic science-fiction movie poster featuring an astronaut exploring an alien world with twin moons.",
        "category": "Movie",
        "style": "Cinematic",
        "theme": "Cool",
        "ratio": "Portrait",
        "title": "HORIZON ZERO",
        "subtitle": "In The Deepest Silence, We Found The Light",
        "date": "IN CINEMAS DECEMBER 2025",
        "venue": "Worldwide in IMAX 3D",
        "organizer": "Nebula Pictures in Association with Stellar Media",
        "extra": "Directed by Ava Vance • Original Score in Dolby Atmos"
    },
    {
        "label": "🎮 Esports Arena Championship",
        "prompt": "Epic esports gaming championship poster featuring armored cyborg warriors in a glowing futuristic stadium with laser effects.",
        "category": "Gaming",
        "style": "Cyberpunk",
        "theme": "Neon",
        "ratio": "Portrait",
        "title": "TITAN CLASH",
        "subtitle": "Ultimate Esports World Championship",
        "date": "DECEMBER 05, 2025 • 6:00 PM EST",
        "venue": "Apex Mega Arena, Neo Tokyo & Twitch Live",
        "organizer": "Global Pro Gaming League",
        "extra": "16 Teams • $1,000,000 Championship Pool"
    },
    {
        "label": "💼 Global Tech Summit",
        "prompt": "Modern executive business summit poster with abstract geometric glass architectural reflections and golden accents.",
        "category": "Business",
        "style": "Minimalist",
        "theme": "Monochrome",
        "ratio": "Portrait",
        "title": "NEXUS SUMMIT",
        "subtitle": "Leadership, Strategy & Next-Gen Innovation",
        "date": "JANUARY 18-20, 2026",
        "venue": "Metropolitan Convention Center, New York",
        "organizer": "International Business & Venture Council",
        "extra": "Keynotes from Fortune 100 Leaders • Investor Networking"
    }
]

# Universal Negative Prompt to keep poster background clean of accidental text / watermarks
STANDARD_NEGATIVE_PROMPT = (
    "text, typography, letters, words, watermark, signature, logo, username, "
    "blurry, ugly, bad anatomy, deformed, distorted, low quality, artifacts, "
    "pixelated, duplicate, draft, border, framing"
)


def validate_user_prompt(prompt: str) -> Tuple[bool, str]:
    """
    Validates user input prompt for sufficient length and content.
    Returns (is_valid, error_message).
    """
    if not prompt or not prompt.strip():
        return False, "Prompt cannot be empty. Please describe the poster background you want to create."
    
    cleaned = prompt.strip()
    if len(cleaned) < 5:
        return False, "Prompt is too short. Please provide at least 5 characters describing your scene."
    
    # Check if prompt contains at least some alphanumeric characters
    if not re.search(r'[a-zA-Z0-9]', cleaned):
        return False, "Prompt must contain letters or numbers describing the subject."
        
    return True, ""


def enhance_prompt(
    base_prompt: str,
    category: str = "Technology",
    style: str = "Cyberpunk",
    theme: str = "Neon",
    extra_details: str = ""
) -> str:
    """
    Enhances user prompt with visual design cues, lighting, styling and composition tokens
    while preserving user's core intent. Specifically instructs the model to create
    background artwork suitable for a poster canvas.
    """
    category_data = CATEGORY_MODIFIERS.get(category, CATEGORY_MODIFIERS["Technology"])
    style_text = STYLE_MODIFIERS.get(style, STYLE_MODIFIERS["Cyberpunk"])
    theme_data = THEME_MODIFIERS.get(theme, THEME_MODIFIERS["Neon"])
    
    components = [
        # Original core intent
        base_prompt.strip().rstrip('.'),
        
        # Category cues
        category_data["visual"],
        category_data["lighting"],
        category_data["composition"],
        
        # Art style & color palette
        style_text,
        theme_data["prompt"],
        
        # Professional background composition instruction (no text embedded)
        "high quality poster background art, visual masterpiece, highly detailed, clean composition suitable for title overlay, wallpaper quality"
    ]
    
    if extra_details and extra_details.strip():
        components.append(extra_details.strip())
        
    # Join with clean separators
    return ", ".join(components)


def format_text_snippet(text: str, max_chars: int = 50) -> str:
    """Safely shortens or formats a string snippet."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 3] + "..."
