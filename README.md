# Your Own AI App for Avoidant Relationships (₹0 to run)

This is your app — like Gemini or ChatGPT, but built only for avoidant
relationships, for both sides:
  💗 people who love an avoidant
  🌱 avoidants who want to grow

Users just open the link and chat. No key, no login, no payment — exactly
like the Gemini app. Your free Gemini key stays hidden on the server.

──────────────────────────────────────────────
STEP 1 — Get your free Gemini key (5 minutes)
──────────────────────────────────────────────
1. Open aistudio.google.com and sign in with your Google account
2. Click "Get API key" → "Create API key"
3. Copy the key (starts with AIza) and save it in your Notes app

──────────────────────────────────────────────
STEP 2 — Name your app (1 minute)
──────────────────────────────────────────────
Open app.py in Notepad. Near the top, change:
    APP_NAME = "Bandhan AI"
to your own name. Save. That's your trademark on every screen.

──────────────────────────────────────────────
STEP 3 — Put it on the internet (30 minutes, all free)
──────────────────────────────────────────────
A) Make a free account at github.com
B) Click "+" → "New repository" → name it anything → Create
C) Click "uploading an existing file" → drag ALL files from this
   folder in (app.py, requirements.txt, README.md, and the
   templates folder's index.html — GitHub upload keeps folders if
   you drag the whole folder) → Commit changes
D) Make a free account at render.com (sign in with GitHub — easiest)
E) Click "New" → "Web Service" → choose your repository
F) Fill in only these boxes:
      Build Command:  pip install -r requirements.txt
      Start Command:  gunicorn app:app
G) Scroll to "Environment Variables" → Add:
      Key:   GEMINI_API_KEY
      Value: (paste your AIza key)
H) Click "Deploy Web Service" and wait ~5 minutes

You'll get a link like  yourname.onrender.com
Open it on your phone. That's YOUR AI, live on the internet. 🎉
Anyone you share the link with can chat instantly — no key needed.

──────────────────────────────────────────────
(Optional) Test on your laptop first
──────────────────────────────────────────────
In the folder, open Command Prompt and type:
    pip install -r requirements.txt
    set GEMINI_API_KEY=AIza-your-key-here
    python app.py
Then open http://localhost:5000 in Chrome.

──────────────────────────────────────────────
Costs & limits (honest version)
──────────────────────────────────────────────
- Hosting: ₹0 (Render free tier — the app "sleeps" when unused, so the
  first message after a gap takes ~30 seconds to wake up. Normal.)
- AI: ₹0 (Gemini free tier — a limited number of chats per day total,
  fine for you + a small circle. If it says the daily limit is reached,
  it resets next day.)
- When your app grows popular, you upgrade Gemini to paid — that's a
  good problem, and it means people love what you built.

──────────────────────────────────────────────
Making the name legally yours (later)
──────────────────────────────────────────────
- Buy the domain (yourname.in, ~₹500/yr on Hostinger/GoDaddy) and
  connect it in Render settings
- Register the trademark at ipindia.gov.in (Class 42, ~₹4,500 for
  individuals) once you're sure of the name

──────────────────────────────────────────────
Safety already built in
──────────────────────────────────────────────
- Crisis language gently redirects users to iCall (9152987821) and
  RCI-licensed counsellors
- The AI never diagnoses anyone, never villainizes either partner
- Message limits protect your free daily quota
