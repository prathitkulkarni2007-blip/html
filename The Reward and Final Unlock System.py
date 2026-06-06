#  TASK 1 — generate_chamber
def generate_chamber(idx: int, history: list) -> dict:
    name = CHAMBER_NAMES[idx % len(CHAMBER_NAMES)]
    hist = " | ".join(history[-3:]) if history else "None"
    text = call_groq(
        "Write immersive fantasy-mystery chamber descriptions. Output JSON: title, description, clue.",
        f"Chamber {idx+1}. Title: {name}. History: {hist}. Return valid JSON only.", 1.0)
    if text:
        try:
            d = json.loads(text)
            if all(k in d for k in ["title","description","clue"]): return d
        except Exception: pass
    clues = ["A cracked clock face points toward a hidden seam in the wall.",
             "A blue crystal hums whenever the truth is spoken nearby.",
             "Dust shifts in a pattern that looks almost like writing.",
             "A silent spark jumps between metal rings above the doorway."]
    return {"title": name,
            "description": f"{name} opens before you like a forgotten dream. Pale light spills across ancient stone.",
            "clue": clues[idx % len(clues)]}

#  TASK 2 — generate_relic
def generate_relic(chamber_title: str, description: str, count: int) -> dict:
    text = call_groq(
        "Create magical relics for a vault adventure. Output JSON: name, rarity, lore, power, art_prompt. Rarity: Common/Rare/Epic/Legendary.",
        f"Relic from: {chamber_title}\n{description}\nRelics so far: {count}\nReturn valid JSON only.", 1.0)
    if text:
        try:
            d = json.loads(text)
            if all(k in d for k in ["name","rarity","lore","power","art_prompt"]): return d
        except Exception: pass
    d = RELIC_FALLBACKS[count % len(RELIC_FALLBACKS)].copy()
    d["lore"] += f" It resonates with the memory of {chamber_title}."
    return d

#  TASK 3 — generate_final_ending
def generate_final_ending(player_name: str, relic_names: list, chamber_history: list) -> str:
    # ── LESSON 6 START ───────────────────────────────────────────

    text = call_groq(
        "Narrate the final ending of a mystery vault game. Triumphant, magical, under 160 words.",
        f"Player: {player_name}\nRelics: {', '.join(relic_names) or 'None'}\nChambers: {', '.join(chamber_history) or 'None'}")
    return text or (f"The final seal withdraws as {player_name or 'Traveler'} steps forward, carrying "
                    f"{', '.join(relic_names) or 'no relics'}. Ancient light spills across the floor. "
                    f"A voice older than stone declares: Vault Access Granted. Your journey is now legend.")

#  TASK 4 — apply_scenario
def apply_scenario(sc: dict):
    s = st.session_state

    ch = maybe_generate_current_chamber()
    if not ch: return

    change_trust(sc["trust"]); s.streak += 1
    append_log("YOU", sc["message"])
    append_log("SENTINEL", ask_sentinel(s.player_name or "Traveler", sc["message"], s.trust_score, s.sentinel_mood))
    s.latest_clue = sc["effect"]; s.last_action_feedback = sc["effect"]
    s.scenario_history.append(f"{ch['title']}: {sc['title']}")

    actions = sum(1 for h in s.scenario_history if h.startswith(ch["title"]))
    if sc["title"].startswith("➡") or actions >= 2:
        nxt = s.current_chamber + 1; s.current_chamber = nxt; s.last_chamber = None
        if nxt >= TOTAL_CHAMBERS:
            s.door_anim = "vault"; append_log("SENTINEL", "All chambers have spoken. The forge awaits you now.")
        else:
            s.door_anim = "chamber"; append_log("SYSTEM", f"Chamber {nxt+1} unlocked — the door opens.")

    event = maybe_trigger_event()
    if event:
        s.last_event = event; change_trust(event["trust_delta"])
        append_log("SYSTEM", f"EVENT: {event['title']} — {event['description']}")
    check_achievements()


#  TASK 5 — forge_relic
def forge_relic():
    s = st.session_state
    if not s.chamber_history: st.toast("No chambers explored yet.", icon="⚠️"); return
    last_title = s.chamber_history[-1]
    relic = generate_relic(last_title, s.chamber_descriptions.get(last_title, f"Ancient memories of {last_title}."), len(s.relic_inventory))
    with st.spinner(f"Forging {relic['name']}…"):
        card = make_relic_card(relic, get_relic_image(relic["art_prompt"], relic.get("rarity","Rare")))
    buf = io.BytesIO(); card.save(buf, format="PNG"); relic["card_bytes"] = buf.getvalue()
    s.relic_inventory.append(relic); s.latest_clue = f"Relic materialized: {relic['name']}."
    append_log("SYSTEM", f"Relic forged: {relic['name']} · {relic['rarity']}")
    append_log("SENTINEL", f"I can feel it taking shape — {relic['name']}. Hold onto it. You'll need it.")
    st.toast(f"💎 Relic forged: {relic['name']} [{relic['rarity']}]", icon="💎")
    check_achievements()


#  TASK 6 — unlock_final_vault
def unlock_final_vault():
    s = st.session_state

    s.ending_text = generate_final_ending(s.player_name, [r["name"] for r in s.relic_inventory], s.chamber_history)
    s.final_unlocked = True
    s.door_anim = "final"
    s.latest_clue = "The final vault recognizes your journey."
    append_log("SYSTEM", "Final seal lifted. Vault Access Granted.")
    check_achievements()