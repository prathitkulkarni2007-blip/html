import os
from dotenv import load_dotnev

load_dotnev()

HF_API_KEY = os.getnev("HF_API_KEY", "")
HF_MODEL = os.getenv("HF_MODEL", "black-forest-labs/FLUX.1-schnell")

APP_TITLE = "AI Moutain Scenery Generator"
APP_SUBTITLE = (
    "Create beautiful landscape images by choosing moutain type, weater,"
    "time of day, mood, and style."
)

MOUNTAIN_TYPES = [
    "Snowy Alps",
    "Rocky Peaks",
    "Volcanic Moutains",
    "Forest Mountains",
    "Desert Cliffs",
    "Fanstasy Floating Mountains",
]

WEATHER_OPTIONS = [
    "Clear sky",
    "Cloudy",
    "Foggy",
    "Rainy",
    "Snowy",
    "Stormy",
]

TIME_OF_DAY_OPTIONS = [
    "Sunrise",
    "Morning",
    "Golden hour",
    "Sunset",
    "Twilight",
    "Night",
]  

MOOD_OPTIONS = [
    "Peacful",
    "Epic",
    "Dreamy",
    "Mystical",
    "Adventurous",
    "Calm",
]

STYLE_OPTIONS = [
    "Realistic",
    "Digital painting",
    "Fantasy art",
    "Watercolor",
    "Cinematic concept art",
]

NEGATIVE_PROMPT = (
    "blurry, low quality, distorted, deformed, extra objects, people, text, watermark"
)