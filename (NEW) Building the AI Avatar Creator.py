import io
import streamlit as st
from huggingface hub import InferenceClient
import config

st.set_page_config(page_title="AI Avatar Creator", page_icon="🎨", layout="centered")

OPTIONS = {
    "avatar type": ["boy hero", "girl hero", "wizard", "robot explorer", "space warrior", "animal adventurer"],
    "hairstyle": ["short spiky hair", "curly hair", "long straight hair", "ponytail","glowing hair", "helmet"],
    "outfit": ["superhero suit", "magical robe", "space armor", "casual hoodie", "battle costume", "royal outfit"],
    "expression": ["happy", "confident", "excited", "brave", "mysterious", "playful"],
    "background": ["forest", "space station", "magic castle", "city skyline", "rainbow world", "cloud kingdom"],
    "art style": ["crtoon style", "anime style", "3D game style", "fantasy illustration", "comic style"],
  }

  client = InferenceClient(api_key=config.HF_API_KEY)
  st.session_state.setdefault("generated_image", None)

  st.title("🎨 AI Avatar Creator")
  st.write("Create your own avatar with AI!")
  st.markdown("Choose your avatar details or write your own custom prompt, then click **Generate Avatar**.")
  st.subheader(" 🛠️Create Your Avatar")
  
  mode = st.selectbox("Choose prompt mode", ["Use Avatar Builder", "Write Custome Prompt"])

  if mode == "Use Avatar Builder":
     values = {k: st.selectbox(f"Choose {k}", v) for k, v in OPTIONS.items()}
     extra = st.text_input("Add one extra detail (optional)", placeholder="Example: glowing blue eyes").strip()
     prompt = (
        f"A kid-friendly {values['avatar type']},"
        
     )