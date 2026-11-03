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
- Offline pages + offline chatbot: core pages and keyword answers work without internet, covering transport, payments, emergencies, and jobs, with verified answers naming their source
- Money tracker: income, spending and savings goals, stored in your browser, with optional AI explanations of monthly totals (totals only, notes never leave the browser)
- 4-language UI: English, Nepali, Vietnamese and Burmese
- Dark mode

## How LifeBridge uses Meta AI

- The **muse-spark-1.3** vision model reads the notice photo and its Japanese text.
- The model must reply in strict JSON with 17 fields (`what`, `why`, `importance`, `next_steps`, `deadline`, `amount`, `staff_phrase`, `staff_phrase_meaning`, `staff_reading`, `staff_variations`, `payment_methods`, `consequences`, `markers`, `payment_codes`, `payment_steps`, `check`, `deadline_date`) — the due date always comes back as `YYYY-MM-DD`.
- Follow-up chat sends the photo again with the explanation and the earlier questions, so every question stays about the same notice.
- The prompt forbids guessing: unclear amounts and dates come back empty with a note to check, never invented.
- Answers come in 5 languages: English, Nepali, Vietnamese, Burmese and Japanese.

## Accuracy check
| Letter | Type | Deadline correct | Amount correct | Notes |
|---|---|---|---|---|
| Water and sewer bill (Shiki City) | Real letter | Yes | Yes | Nov 16, 2026 / 2,304 yen |
| Road repair notice | Real letter | N/A (information only) | N/A | Date and time correct, said "not a payment" |
| National Health Insurance payment slip | Synthetic sample | Yes | Yes | Did not confuse the barcode expiry date with the deadline |
| National Pension exemption rejected | Synthetic sample | N/A | N/A | Said the exemption was rejected, payment is still needed, and the 3-month appeal window |
| Water bill auto-debit failed | Synthetic sample | Yes | Yes | Nov 25, 2026 / 3,520 yen |
Real letters were tested with personal details covered. Synthetic samples are fictional (見本市, 見本 太郎) and labeled 見本.

## Speed (real iPhone tests on home Wi-Fi)
- Scan: about 11–27 s (most 11–21 s). Before tuning reasoning_effort: 28–37 s.
- Follow-up answer: 6–8 s. Before: about 19 s.

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

- Screenshots: *coming soon* (synthetic samples or the built-in sample notice only, never a real letter)
- Demo video: *coming soon*
- Live demo: *coming soon*
