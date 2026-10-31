# LifeBridge Lens

Understand Japanese official notices: scan a paper notice with your phone and
get a plain-language explanation, follow-up answers, and saved deadlines.

## What was built during the hackathon vs pre-existing

- **Pre-existing (not judged):** the LIFEGO guide website — guide articles,
  home, search, saved pages and settings. It is kept separately at
  https://github.com/Binod-in/lifebridge-japan and none of its code is in
  this repo.
- **Built this week (everything in this repo):** the Lens explainer
  (`explain.html` + `server.py`), the deadlines page (`dates.html`), the
  money tracker (`tracker.html`), the landing page (`index.html`), the
  offline chatbot (`chatbot.js`), translations (`i18n.js`), the offline
  service worker (`sw.js`), the new stylesheet, and the test suite.

## Features

- Lens: photograph a Japanese notice and get a plain-language explanation
- Communication tutor: every scan includes a staff phrase with hiragana reading, read-aloud, and practice sentences
- Follow-up chat: ask questions about the same notice, with memory of earlier questions
- Save deadline: check the due date and add it to My Deadlines in one tap
- Offline pages + offline chatbot: core pages and keyword answers work without internet
- Money tracker: income, spending and savings goals, stored in your browser, with optional AI explanations of monthly totals (totals only, notes never leave the browser)
- 4-language UI: English, Nepali, Vietnamese and Burmese
- Dark mode

## How LifeBridge uses Meta AI

- The **muse-spark-1.3** vision model reads the notice photo and its Japanese text.
- The model must reply in strict JSON with 17 fields (`what`, `why`, `importance`, `next_steps`, `deadline`, `amount`, `staff_phrase`, `staff_phrase_meaning`, `staff_reading`, `staff_variations`, `payment_methods`, `consequences`, `markers`, `payment_codes`, `payment_steps`, `check`, `deadline_date`) — the due date always comes back as `YYYY-MM-DD`.
- Follow-up chat sends the photo again with the explanation and the earlier questions, so every question stays about the same notice.
- The prompt forbids guessing: unclear amounts and dates come back empty with a note to check, never invented.
- Answers come in 5 languages: English, Nepali, Vietnamese, Burmese and Japanese.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edit .env and set META_API_KEY (never commit .env)
python server.py
```

Then open http://127.0.0.1:5000/. The AI features need `META_API_KEY`,
everything else works without it.

LB_API_TOKEN (optional) only blocks casual scripts. It is sent to every
browser via `/lb-config.js`, so it is NOT a secret and NOT real
authentication.

## Run the tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover tests -v
```

Tests use mocked AI replies and need no API key.

## Project status

- Screenshots: *coming soon*
- Demo video: *coming soon*
- Live demo: *coming soon*
