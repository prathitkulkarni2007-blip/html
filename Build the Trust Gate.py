# TASK 1 - analyze_player_tone
def analyze_player_tone(message: str, streak: int = 0, recent_messages: list = None) -> int:
    msg = message.lower().strip()

    if recent_messages:
        recent_lower = [m.lower().strip() for m in recent_messages[-6:]]
        if recent_lower.count(msg) >= 2:
            return 0
        delta = 4
        if len(msg) < 4:
            delta -= 1
        if any(word in msg for word in HELPFUL_HINTS):
            delta += 10
        if any(word in msg for word in RUDE_HINTS):
            delta -= 12
        if "?" in msg:
            delta += 2
        if streak >= STREAK_BONUS_AT and delta > 0:   
           delta += 6
        delta = max(-15, min(20, delta))

        return delta

    # TASK 2 - get_sentinel_mood
    def get_sentinel_mood(trust: int) -> str:

       if trust < 20:
           return "Suspicious"
       elif trust < 50:
           return "Watching"
       elif trust < 80:
           return "Curious"
       else:
           return "Accepting"
       
       # TASK 3 - process_player_message
       def process_player_message(msg: str):
           s = st.session_state

           # Step 1 - guard: empty player name
           if not s.player_name.strip():
               st.toast("Enter your traveler name first.", icon="📒")
               return
           
           # Step 2 - guard: empty message
           if not msg.strip():
               return
           
           # Step 3 - repeat detection
           recent = [m.lower().strip() for m in s.player_message[-6:]]
           if recent.count(msg.lower().strip()) >= 2:
               st.toast("The Sentinel noticed you're repeating yourself.", icon="😐")
               _append_log("YOU", msg)
               _append_log("SENTINEL", random.choice(REPEAT_REPLIES))
               s.player_messages.append(msg)
               s.message_sent += 1
               return
           
           # Step 4 - analyze tone
           delta = analyze_player_tone(msg, s.streak, s.player_messages)

           # Step 5 - update trust
           s.trust_score = max(0, min(MAX_TRUST, s.trust_score + delta))

           # Step 6 - update mood
           s.sentinel_mood = get_sentinel_mood(s.trust_score)

           # Step 7 - update streak
           s.streak = s.streak + 1 if delta > 0 else 0

           # Step 8 - log player message
           _append_log("YOU", msg)

           # Step 9 - get and log Sentinel reply
           reply = ask sentinal ai(s.player_name, msg, s.trust_score, s.sentinel_mood)
           _append_log("SENTINEL", reply)

           # Step 10 - append to player_messages
           s.player_messages.append(msg)

           # Step 11 - update latest clue
           s.latest_clue = "The Sentinel studies your tone."

           # Step 12 - increment messages_sent
           s.messages_sent += 1

           # Step 13 - banish check
           if s.trust_score <= BANISH_THRESHOLD and delta < 0:
               s.banished = True

           # TASK 4 - process_riddle_answer
           def process_riddle_answer(answer: str):
               s = st.session_state
            
            # Step 1 - guard: already solved
            if s.riddle_solved:
               st.toast("Logic lock already solved.", icon="ℹ️")
               return
           
           # Step 2 - guard: empty answer
           if not answer.strip():
               return
           
           # Step 3 - get riddle
           riddle = s.riddle

           # Step 4 - check correct or wrong
           if riddle["answer"].lower() in answer.lower().strip():
               # Correct
               s.riddle_solved = True
               s.trust_score = min(MAX_TRUST, s.trust_score + 35)
               s.sentinel_mood = get_sentinel_mood(s.trust_score)
               s.streak += 1
               _append_log("YOU", f"Riddle: {answer}")
               _append_log("SENTINEL", radom.choice([
                   "Yes. That's it. I felt the lock shift just now - something old and heavy, finally moving.",
                   "Hm. You actually got it. The seal loosens. Don't make me regret this.",
                   "Correct. The gate remembers that answer. You're smarter than you look, traveler.",
               ]))
               s.latest_clue = "The runes brighten - a thin line of light appers in the gate."
               st.toast("Correct! The lock flashes open.", icon="✅")
            else:
               # Wrong
               s.trust_score = max(0, s.trust_score - 5)
               s.sentinel_mood = get_sentinel_mood(s.trust_score)
               s.streak = 0
               _append_log("YOU", f"Riddle: {answer}")
               _append_log("SENTINEL", random.choice([
                   "That's not it. Think harder - the hint is right in front of you.",
                   "No... you're not there yet. Read the riddle again, slowly.",
                   f"Wrong answer. The lock doesn't budge. Hint: {riddle['hints']}",
               ]))
               s.latest_clue = f"Hint: {riddle['hints']}"
               st.toast("Incorrect - the seal holds.", icon="❌")