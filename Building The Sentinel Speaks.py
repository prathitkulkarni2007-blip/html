# TASK 1 - fallback_sentinel
def fallback_sentinel(player_name: str, message: str, mood: str) -> str:

    if any(w in message.lower() for w in RUDE_HINTS):
        return random.choice([
            "Watch yourself. I've turned away far greater than less.",
            "That kind of talk doesn't open doors here. It closes them.",
            "Careful. The vault remembers every word spoken at its gate.",
        ])
     return random.choice(SENTINEL_FALLBACKS>get(mood SENTINEL_FALLBACKS["Suspicious"]))

    # TASK 2 - ask_sentinel
    def ask_sentinel(player_name: str, message: str, trust: int, mood: str) -> str:

        if not config.GROQ_API_KEY:
            return fallback_sentinel(player_name, message, mood)
        
        system_prompt = (
            f"You are The Sentinel - an ancient immortal gatekeeper.\n"
            f"{MOOD_STYLES.get(mood, MOOD_STYLES['Suspicious'])}\n"
            "Use contractions, vary sentence length, react emotionally.\n"
            "Never break character. Never mention being an AI.\n"
            "Under 80 words. End with a question, warning, or hint."
        )

        user_prompt = (
            f"Traveler: {player_name or 'Unknown'}\n"
            f"How you feel about them: {MOOD_FEEL.get(mood, MOOD_FEEL['Suspicious'])}\n"
            f"Their message: \"{message}\"\n"
            "Respond naturally. Don't reveal any numbers."
        )

        try:
            r = Groq(api_key=config.GROQ_API_KEY).chat.completions.create(
                model=config.GROQ_TEXT_MODEL,
                temperature=0.9,
                message=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user _prompt},
                ],
            )
            return r.choices[0].message.content.strip()
          except Exception:
            return fallback_sentinel(player_name, message, mood)
        
          # TASK 3 - generate_riddle_hint
          def generate_riddle_hint(riddle_question: str, riddle_answer: str, plain_hint: str) -> str:

            if not config.GROQ_API_KEY:
                return f"Hint: {plain_hint}"
            
              try:
                r = GROQ(api key = config GROQ_API_KEY) chat completions create(
                    model=config.GROQ_ TEXT _MODEL,
                    temperature=1.0,
                    messages=[
                        {"role": "system", "content": (
                            "You are The Sentinel. Give a cryptic, atmospheric one-line hint"
                            "for a riddle. Stay in character. Under 30 words."
                        )},
                        {"role": "user", "content": (
                            f"The riddle is: {riddle_question}\n"
                            f"The answer is: {riddle_answer}\n"
                            "Give a cryptic hint without revealing the answer."
                        )},
                    ],
                )
                return r.choices[0].message.content.strip()
            except Exception:
                return f"Hint: {plain_hint}"
            
            #  TASK 4 - generate_event_narration
            def generate_event_narration(event_title: str, plain_description: str) -> str:

                if not config.GROQ_ API_KEY:
                   return plain_description
                
            try:
                r = Groq(api_key=config.GROQ_ API_KEY).chat.completions.create(
                    model=config.GROQ_ TEXT _MODEL,
                    temperature=0.95,
                    messages=[
                        {"role": "system", "content": (
                            "You are The Sentinel narrating a vault event. "
                            "One dramatic sentence, in character, under 25 words."
                        )},
                        {"role": "user", "content": (
                            f"Event: {event_title}\n"
                             f"Description: {plain_description}\n"
                             "Narrate this as The Sentinel in one sentence."
                        )},
                    ],
                )
                return r.choices[0].message.content.strip()
            except Exception:
                return plain_description