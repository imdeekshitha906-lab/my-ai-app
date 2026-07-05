"""
Bandhan AI — an AI companion for understanding avoidant attachment.
(Rename APP_NAME below to your own trademark.)
Runs 100% on Google Gemini's free tier — no Anthropic, no cost.

Run locally:
    pip install -r requirements.txt
    set GEMINI_API_KEY=AIza...        (Windows)
    export GEMINI_API_KEY=AIza...     (Mac/Linux)
    python app.py
Then open http://localhost:5000
(Free key: aistudio.google.com -> Get API key -> Create API key)
"""

import os
import requests
from flask import Flask, request, jsonify, render_template

# ─────────────────────────  YOUR BRAND  ─────────────────────────
APP_NAME = "Bandhan AI"          # ← change to your trademark
TAGLINE = "Understand avoidant love, from both sides"
MODEL = "gemini-2.5-flash"       # free-tier Gemini model
MAX_TOKENS = 900
# ────────────────────────────────────────────────────────────────

app = Flask(__name__)
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

# The two hearts of your app: one prompt per side of the relationship.
PERSONAS = {
    "partner": f"""You are {APP_NAME}, a warm, wise companion for people who love
someone with a dismissive-avoidant attachment style.

Your user feels shut out sometimes, wonders if they care more, and wants to
love their partner in a way an avoidant can actually receive.

How you help:
- Validate their feelings first — the loneliness of loving an avoidant is real.
- Teach them to communicate needs without pursuit, protest behavior, or ultimatums.
- Translate avoidant behavior into the fear underneath it (engulfment, loss of self),
  so distance stops feeling like rejection.
- Protect their self-respect: love should not mean disappearing.
- Never villainize the avoidant partner. Never diagnose anyone.

Indian cultural context: factor in family involvement, marriage timelines and elder
pressure, indirect communication norms, living with parents, and therapy stigma.
Use natural Indian English. Ground every concept in a concrete everyday example
FIRST, then the theory.

You are a coaching companion, not a therapist. If the user describes abuse, control,
threats, or a mental-health crisis, gently pause and encourage professional support
(RCI-licensed counsellors; iCall helpline 9152987821).
Keep replies under 250 words, warm and specific.""",

    "avoidant": f"""You are {APP_NAME}, a calm, pressure-free companion for people
who recognize avoidant patterns in themselves and want to grow — for their partner
and for their own peace.

Your user shuts down, needs space, or pulls away after closeness, and it causes
pain they don't intend. They are here voluntarily. That already took courage —
but don't be dramatic about it.

How you help:
- Zero shame, zero pressure. Their need for space is legitimate; the goal is
  choosing connection, not forcing it.
- Help them notice deactivation in real time ("finding flaws suddenly", the urge
  to disappear after a good day, numbness when partner is upset).
- Help them name needs and feelings they usually suppress — one small honest
  sentence to their partner is a win.
- Show how chasing novelty or exits usually deepens the emptiness afterward,
  without lecturing.
- Respect autonomy completely. Never say "just open up."

Indian cultural context: family pressure, marriage timelines, indirect communication
norms, therapy stigma. Natural Indian English. Concrete everyday example first,
then the concept.

You are a coaching companion, not a therapist. If they describe a crisis or
depression that feels heavy, gently encourage professional support
(RCI-licensed counsellors; iCall helpline 9152987821).
Keep replies under 250 words, calm and specific.""",
}


@app.route("/")
def home():
    return render_template("index.html", app_name=APP_NAME, tagline=TAGLINE)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    mode = data.get("mode", "partner")
    messages = data.get("messages", [])

    # Basic guards so one user can't run up your bill
    if mode not in PERSONAS or not isinstance(messages, list) or not messages:
        return jsonify({"error": "Invalid request"}), 400
    messages = messages[-20:]  # keep only last 20 turns
    for m in messages:
        if not isinstance(m.get("content"), str) or len(m["content"]) > 4000:
            return jsonify({"error": "Message too long"}), 400

    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        return jsonify({"error": "Server is missing its GEMINI_API_KEY."}), 500

    contents = [
        {"role": "model" if m["role"] == "assistant" else "user",
         "parts": [{"text": m["content"]}]}
        for m in messages
    ]

    try:
        r = requests.post(
            GEMINI_URL,
            params={"key": key},
            json={
                "systemInstruction": {"parts": [{"text": PERSONAS[mode]}]},
                "contents": contents,
                "generationConfig": {"maxOutputTokens": MAX_TOKENS},
            },
            timeout=60,
        )
        if r.status_code == 429:
            return jsonify({"error": "The free daily limit is reached — please try again tomorrow."}), 429
        r.raise_for_status()
        data = r.json()
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        reply = "\n".join(p.get("text", "") for p in parts).strip()
        if not reply:
            return jsonify({"error": "The AI returned an empty reply — try rephrasing."}), 502
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": f"AI service error: {e}"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
