GESTURE_SPELLS = {
   "Palm": "Shield of Light",
   "Peace": "Healing Aura",
   "Pointer": "Lightning Strike",
   "Thumbs Up": "Phoenix Blessing",
   }

   @st.cache_resource(show_spinner=False)
   def get_model():
       return load_local_teachable_machine_model(str(config.Model_PATH), str(config.LABELS_PATH))
    
    def normalize(label: str) -> str:
       return LABEL_MAP.get(label.strip(), label.strip())

    def prediction_panel(image: Image.Image, source: str):
        st.image(image, caption="Gesture image", use_container_width=True)
        st.markdown(f'<div class="pill">Source: {source.title()}</div>', unsafe_allow_html=True)
         try:
            model, labels = get_model()
            pred = predict_gesture_from_image(model, labels, image)
            pred["label"] = normalize(pred["label])
            for item in pred["top_predictions"]:
                item["label"] = normalize(item["label"])
            st.success(f"Detected gesture: **{pred['label']}**")
            st.progress(float(pred["confidence"]), text=f"Confidence: {pred['confidence']: 1%}")
               spell = GESTURE_SPELLS.get(pred["label"], "Arcane Pulse")
               c1, c2 = st.colums(2)
               c1.markdown(f'<div class="card"><b>Detected Gesture</b><br><br> {pred["label"]}</div>', unsafe_allow_html=True)
                  c2.markdoen(f'<div class="card"><b>Mapped Spell</b><br><br>{spell}</div>', unsafe_allow_html=True)\
                    with st.expander("All predication scores"):
                        for item in pred["top _predications"]:
                            st.progress(float(item["confidence"]), text=f"{item['label']} - {item['confidence']:.1%}")
                              except Exception as e:
                                  st.error(f"Model error: {e}\n\nTip: use Python 3.10/3.11 and tensorflow==2.15.0")

                                  def main():
                                      render_style()
                                      st.markdown(f"""
                                          <div class="hero">
                                        <h1 style="margin:0 0 6px 0;">{config.APP_ICON} {config.APP_TITLE}</h1>
                                        <p style="margin:0;">Show a hand gesture via webcam or upload an image.
                                        The app dectects the sign and maps it to a magical spell.</p>
                                     </div>""", unsafe allow html=True)
                                     with st.expander("ℹ️ Detected gestures: Palm . Peace . Pointer . Thumbs Up"):
                                         st.markdown("Show one of these gestures clearly in the camera or image.")
                                    st.markdown('<div class="panel">', unsafe_allow_html=True)
                                    tabs = st.tabs(["📷 Webcam Capture", "🖼️ Upload Image"])
                                    with tabs[0]:
                                        cam = st.camera_input("Capture gesture from webcam", help=config.CAMERA_HELP)
                                          if cam:
                                             prediction_panel(Image.open(cam).convert("RGB"), "webcam")
                                         else:
                                              st.info("Take a photo with your webcam to detect a gesture.")
                                    with tabs[1]:
                                        up = st.file_uploader("Upload a gesture image", type=["png", "jpg", "jpeg"])
                                        if up:
                                             prediction_panel(Image.open(up).convert("RGB"), "upload")
                                          else:
                                             st.info("Upload a hard gesture image to detect a gesture.")
                                    st.markdown('</div>', unsafe_allow_html=True)