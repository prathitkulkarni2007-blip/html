import streamlit as st

from config import setup_page
from constants import DEFAULT_SCORE, SCENARIO_PRESETS
from student_logic import default_state, get_mood_data, get_progress_message
from ui import (
    render_header,
    render_mood_card,
    render_quick_actions,
    render_reset,
    render_rules_table,
    render_score_input,
)


setup_page()

if "score" not in st.session_state:
    st.session_state.update(default_state())

render_header()

selected_scenario = render_quick_actions()
if selected_scenario:
    st.session_state.score = SCENARIO_PRESETS[selected_scenario]

current_score = render_score_input(st.session_state.score)
st.session_state.score = current_score

mood = get_mood_data(st.session_state.score)
message = get_progress_message(st.session_state.score)
render_mood_card(st.session_state.score, mood, message)

st.markdown("---")
render_rules_table()

if render_reset():
    st.session_state.score = DEFAULT_SCORE
    st.rerun()