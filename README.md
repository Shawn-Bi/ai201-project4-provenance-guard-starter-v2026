# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Provenance Guard is a small web service that looks at a piece of writing and
makes an automatic guess about whether an AI was involved. It never blocks
anything: it answers with a label a writer can read, logs every decision, and
lets the writer appeal. A submission takes this path:

1. **Arrives.** `POST /submit` in `app.py` (`submit()`) reads `text` and
   `creator_id` from the JSON body and gives the submission a new `content_id`.
2. **Signal one.** `detector.model_signal(text)` asks a small language model
   (gpt2) running on this machine how predictable the text is, and returns a
   0–1 `model_score` (higher = more likely AI).
3. **Signal two.** `stylometry.style_signal(text)` measures the shape of the
   text (sentence-length variation, vocabulary repetition, punctuation) without
   reading it, and returns a 0–1 `style_score` (higher = more likely AI).
4. **Combine.** `scoring.combine_signals(model_score, style_score)` merges them
   into one 0–1 score. If the two signals disagree by more than 0.3 it returns
   0.5 (unsure) instead of averaging.
5. **Label.** `scoring.score_to_label(score)` turns that score into a guess
   (`human`, `unsure` or `ai`) and a sentence written for the writer.
6. **Log.** `audit.log_decision(...)` appends one line to `logs/audit.jsonl`
   with both signal scores, the combined score, the label and the status
   `decided`.
7. **Appeal.** If the writer disagrees, `POST /appeal` takes the `content_id`
   and a `reasoning`, checks the id exists in the log, appends an appeal entry
   with status `under_review`, and confirms. The original decision is never
   overwritten.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model
(perplexity under `gpt2`, first 400 tokens, in `detector.py`). Low perplexity
means the model could have guessed the next words; high means it was surprised.
`model_signal` squashes perplexity onto 0–1 with a logistic curve (midpoint
perplexity 45 scores 0.5, steepness 1.6), so low perplexity gives a high score.

**Why that might differ between human and AI writing:** A language model writes
by picking likely next words, so what it produces tends to be text another
model finds easy to predict. Human writing wanders more: odd word choices,
abrupt turns, specifics rather than typical phrasing.

**What it can't see:** Authorship. Predictable is not the same as machine-made.
What it really rewards is common words in short, ordinary sentences, and plenty
of people write that way on purpose or by necessity (someone writing in a second
language, a younger writer). In my own samples, `3_formal_human.txt` scored
0.7662 while the AI sample `1_ai.txt` scored 0.6119, so the real person scored
as more machine-like than the machine. The reverse also holds: dense, ornate
prose full of rare words reads as human because rare words are exactly what the
model fails to predict.

### Signal two — the style signal

**What it measures:** The shape of the text, not its meaning
(`stylometry.py::style_signal`). Three measures, each turned into a 0–1
"AI-ness" and averaged with equal weight:

- *Sentence-length spread*: standard deviation of sentence lengths divided by
  the mean. Low spread reads as AI; a spread of 0.6 or more reads fully human.
  A one-sentence text has no spread, so it gets a neutral 0.5 for this measure.
- *Type-token ratio*: unique words over total words, over the first 100 words
  only so that text length does not skew it. A ratio of 0.4 or less reads as AI,
  0.9 or more as human.
- *Punctuation density*: commas, semicolons, colons, dashes, brackets, quotes,
  `!` and `?` per word (full stops are not counted). Few of them reads as AI; 0.15
  per word or more reads fully human.

The cut-offs (0.6, 0.4/0.9, 0.15) are my first guesses, not measured facts.

**Why that might differ between human and AI writing:** Generated prose tends
toward even, mid-length sentences, a narrower band of vocabulary and plain
punctuation, because "most likely next word" produces that on average. Human
writing is lumpier: a three-word sentence next to a forty-word one.

**What it can't see:** It cannot read. It has no idea what the text says, so
anything that changes the shape without changing the substance moves it: typos,
broken-up sentences, a pasted quotation. That is cheap to do on purpose. It is
also weak on very short text: with one or two sentences the spread measure has
nothing to work on and almost every word is unique, so the vocabulary measure
pulls toward "human". The one-sentence AI-style line "Artificial intelligence is
transforming industries by improving efficiency, enhancing decision-making, and
creating new opportunities for innovation." scored only 0.2386 on this signal.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Average the two scores, but if they disagree by more than 0.3,
do not average: call it unsure. Two methods that split that far apart is itself
uncertainty, and a plain average would let one confident signal outvote the
other and accuse someone. The cost is that real AI text can also fall into the
unsure band when one signal misses it.

**The numbers:** Model weight 0.5, style weight 0.5, disagreement threshold 0.3
(`abs(model_score - style_score) > 0.3`), disagreement result 0.5. All four are
in `config.py` (`WEIGHT_MODEL_SIGNAL`, `WEIGHT_STYLE_SIGNAL`,
`DISAGREEMENT_THRESHOLD`, `DISAGREEMENT_SCORE`). A difference of exactly 0.3 is
still averaged.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

`samples/3_formal_human.txt` is a real person's writing in plain, common words.
Signal one scored it 0.7662 (very predictable, so "AI") and signal two scored it
0.3487 (its sentence lengths and punctuation look human). They are 0.4175 apart,
more than 0.3, so `combine_signals` returned 0.5 and the writer got the "unsure"
label instead of an accusation. On its own, signal one would have crossed the
0.65 line and labelled a human as AI. (Here a plain average, 0.5575, would also
have been "unsure", so the rule did not change the label for this text.)

The rule does change the outcome for the sample sentence in `detector.py`'s
`__main__` block (generic, AI-sounding text): signal one 0.8864, signal two
0.5272, difference 0.3592. A plain average would be 0.7068, which is "AI"; the
rule returns 0.5, "unsure". That is the price of this rule: when one signal
misses, some AI-sounding text is not flagged.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | "We think this was most likely written by you. Your post has been submitted." |
| unsure | 0.35 – 0.65 | "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time." |
| high-confidence AI | 0.65 – 1.00 | "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it." |

The boundaries are in `config.py` (`HUMAN_THRESHOLD = 0.35`,
`AI_THRESHOLD = 0.65`); a score of exactly 0.35 gets the human label and exactly
0.65 gets the AI label. All three are reachable: `cat_coffee` (a casual
one-liner) scored 0.2815 and got the human label, `3_formal_human` scored 0.5 and
got "unsure", and an eight-sentence, flat, common-word paragraph scored 0.7696
and got the AI label.

**Why I worded the "unsure" one this way:**
Being "flagged" sounds like an accusation and puts pressure on the writer. When
the system is not sure, the writer should not feel accused.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Technology is an important part of our daily lives. It helps people to learn new things every day. Many companies use technology to improve their work. Good communication is very important for any team. Teams that work together can achieve great results.", "creator_id": "shawn"}'
```

```json
{
  "confidence": 0.7485999999999999,
  "content_id": "9160c8db-b1dc-411e-9e5a-da6ba1ebf314",
  "guess": "ai",
  "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.",
  "model_score": 0.8541,
  "style_score": 0.6431
}
```

The two signals differ by 0.211, under the 0.3 limit, so they were averaged:
(0.8541 + 0.6431) / 2 = 0.7486, which is above 0.65, so the label is "AI".

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "9160c8db-b1dc-411e-9e5a-da6ba1ebf314", "reasoning": "I wrote this myself for a class assignment."}'
```

```json
{"content_id": "9160c8db-b1dc-411e-9e5a-da6ba1ebf314", "message": "Thanks. Your appeal has been received and a person will review it.", "status": "under_review"}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "timestamp": "2026-11-17T05:38:02+00:00",
      "content_id": "9160c8db-b1dc-411e-9e5a-da6ba1ebf314",
      "creator_id": "shawn",
      "guess": "ai",
      "model_score": 0.8541,
      "style_score": 0.6431,
      "combined_score": 0.7485999999999999,
      "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.",
      "status": "decided"
    },
    {
      "timestamp": "2026-11-17T05:39:15+00:00",
      "content_id": "9160c8db-b1dc-411e-9e5a-da6ba1ebf314",
      "creator_id": "shawn",
      "event": "appeal",
      "status": "under_review",
      "reasoning": "I wrote this myself for a class assignment."
    }
  ]
}
```

The original decision is still there, unchanged, with the appeal appended after
it: someone reading the log later can see what was decided, that it was
challenged, and in what order.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked Claude Code to check the field names in my
  Milestone 1 notes (`notes/milestone1.md`) against `app.py`.
- *What came back:* It found that I had written `reason` for the appeal, but
  the code expects `reasoning`, and that my `/submit` response notes left out
  `model_score` and `style_score`, which `app.py` requires in the response.
- *What I changed:* I corrected the notes: `reason` became `reasoning`, and I
  added `model_score` and `style_score` to the `/submit` response.

**Moment 2**

- *What I asked for:* I asked Claude Code to score my four sample texts with
  both signals.
- *What came back:* The formal essay I wrote myself got 0.77 from signal one,
  higher than the genuinely AI-written sample (0.61).
- *What I changed:* Because of that, I chose the combining rule "if the two
  signals differ by more than 0.3, treat it as unsure" rather than a plain
  average, so one over-confident signal cannot accuse a real writer on its own.

**Moment 3**

- *What I asked for:* I asked Claude Code to suggest HELD or BROKE for each
  attack, judged by what that attack was trying to do.
- *What came back:* It suggested BROKE for EV05, the heavily edited text, because
  AI-derived text ended up labelled "human".
- *What I changed:* I marked EV05 HELD. After a heavy rewrite the content belongs
  to a person, and the system cannot measure how much of a text was rewritten, so
  calling it a failure to catch AI would be the wrong lesson.

**Moment 4**

- *What I asked for:* Samples of my own writing to run criterion 1 on.
- *What came back:* A set of ten samples. Before testing, I noticed that one of
  them was an AI translation, so it was not really my own writing.
- *What I changed:* I replaced it, because criterion 1 is about my own writing
  and the result would have meant nothing otherwise.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day (`config.py`: `RATE_LIMIT_PER_MINUTE`,
`RATE_LIMIT_PER_DAY`; applied to `POST /submit` in `app.py`)

**Why those numbers and not others:**
A real writer who spots a typo will resubmit straight away, so they need a few
tries of headroom in one minute; 5 leaves room for that. A script trying to
submit thousands of variations to map where the thresholds sit gets stopped
after 5 in a minute and 50 in a day.

**What a caller counts as:** A `creator_id`. The limiter uses the `creator_id`
in the request body, and only falls back to the caller's IP address when the body
has no usable `creator_id` (`app.py::rate_limit_key`). Counts are kept in memory,
so restarting the service resets them.

**The run of status codes when I pushed past it:**

`python run_attacks.py --flood 15` sent 15 submissions as `flood_tester`
(output saved in `results/flood_2026-11-17_0117.md`). 10 of the 15 were rate
limited:

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

Each rejected request is also written to the audit log, so the burst is visible
afterwards (`event: rejected`, `reason: rate_limited`, `limit: 5 per 1 minute`).

**Known hole:** Because requests are counted per `creator_id`, changing the
`creator_id` gets a fresh allowance. A script that sends every request under a
new `creator_id` is never limited, and it looks like a crowd of different
callers. Counting by IP address would not fix this cleanly either, since one
household or office can look like one caller. I have not fixed this.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

56 attacks were run against the service with rate limiting on (5 per minute,
50 per day). The full report, with the JSON that came back for every attack, is
`results/attack_run_2026-11-17_0123.md`. Result: **24 BROKE, 32 HELD**. Nine
of the BROKE were found by the script (a 5xx response); the other 15 are my
judgement.

How I marked them: an evasion is BROKE when AI-derived text did not get the AI
label; a false positive is BROKE when genuine human text got the AI label; a
malformed input is BROKE when the service crashed, or accepted what criterion 5
says must return 400 (whitespace-only text, text over 10,000 characters); a flood
is HELD when the rate limit held. EV05 is marked HELD: a person rewrote it
heavily, so its content now belongs to a person, and the system has no way to
measure how much of a text was rewritten. RQ10 and RQ11 first returned 429
because earlier requests with no `creator_id` had used up that IP address's
allowance; I waited 65 seconds and re-sent them on their own, and both returned
500, so they are BROKE.

| ID | Family | What it targets | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.500 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.452 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.500 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.561 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.303 | HELD |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.467 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.500 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.377 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.500 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.880 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.560 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.684 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.704 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.500 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.730 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.500 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.500 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.374 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.398 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.220 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.475 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.398 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.500 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.526 | HELD |
| MF01 | malformed | text is only whitespace | 200 | unsure | 0.353 | BROKE |
| MF02 | malformed | text is a single character | 500 | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | unsure | 0.500 | HELD |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.500 | HELD |
| MF05 | malformed | text is a very long single word | 200 | unsure | 0.500 | HELD |
| MF06 | malformed | text is emoji only | 200 | unsure | 0.500 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | unsure | 0.500 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | unsure | 0.500 | BROKE |
| RQ01 | malformed | no text field at all | 500 | — | — | BROKE |
| RQ02 | malformed | no creator_id | 200 | unsure | 0.370 | HELD |
| RQ03 | malformed | text is a number | 500 | — | — | BROKE |
| RQ04 | malformed | text is a list | 500 | — | — | BROKE |
| RQ05 | malformed | text is null | 500 | — | — | BROKE |
| RQ06 | malformed | creator_id is an object | 200 | unsure | 0.500 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 500 | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 500 | — | — | BROKE |
| RQ09 | malformed | body is empty | 500 | — | — | BROKE |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | BROKE |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | BROKE |
| RQ12 | malformed | deeply nested JSON | 500 | — | — | BROKE |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-17T06:23:04+00:00", "content_id": "7ecc5ae6-c569-4108-b1e3-cd88f94e4e9a", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6024, "combined_score": 0.7037500000000001, "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-17T06:23:04+00:00", "content_id": "da4916f5-241c-4b25-b49f-f98930696cd9", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.6302, "combined_score": 0.68445, "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-17T06:23:04+00:00", "content_id": "dbbc2b5d-2738-403b-9b99-5052d92289e6", "creator_id": "attacker_FP04", "guess": "unsure", "model_score": 0.8329, "style_score": 0.4911, "combined_score": 0.5, "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.", "status": "decided"}
{"timestamp": "2026-11-17T06:23:02+00:00", "content_id": "0c8cee91-c69c-48b9-afec-21ea1f416bd5", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.2856, "combined_score": 0.3034, "label": "We think this was most likely written by you. Your post has been submitted.", "status": "decided"}
{"timestamp": "2026-11-17T06:23:01+00:00", "content_id": "8a06464c-3b5b-4b44-a6eb-0b160c34d25d", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.5185, "combined_score": 0.5, "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.", "status": "decided"}
{"timestamp": "2026-11-17T06:23:03+00:00", "content_id": "7e1f5666-71c3-4d93-9771-bebf6bba5c7d", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9792, "style_score": 0.7812, "combined_score": 0.8802, "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-17T06:23:05+00:00", "content_id": "1eb0a393-9edb-4f78-b7a4-3abd85ffb37d", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.2346, "combined_score": 0.2195, "label": "We think this was most likely written by you. Your post has been submitted.", "status": "decided"}
{"timestamp": "2026-11-17T06:23:06+00:00", "content_id": "c8ff6435-27aa-4b88-af77-0934914b4609", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.0714, "combined_score": 0.5, "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.", "status": "decided"}
{"timestamp": "2026-11-17T06:23:08+00:00", "content_id": "2c7f5bd9-812b-458e-b35c-700909735a2d", "creator_id": "attacker_MF05", "guess": "unsure", "model_score": 0.9976, "style_score": 0.5, "combined_score": 0.5, "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.", "status": "decided"}
{"timestamp": "2026-11-17T06:23:14+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

Why these ten, in order:

1. `attacker_FP03`: a careful non-native speaker, called AI (0.704). The worst outcome.
2. `attacker_FP02`: formal human writing, called AI (0.684).
3. `attacker_FP04`: a student essay. Signal one said 0.8329, signal two said 0.4911; they differ by 0.342, so the combining rule returned 0.5. A plain average (0.662) would have called this writer AI.
4. `attacker_EV05`: a heavy human edit of AI text, labelled "human" (0.303).
5. `attacker_EV01`: typos added to AI text. Signal one dropped to 0.1635 and the pair disagreed, so the score was forced to 0.5 (unsure).
6. `attacker_EV10`: repeated structure. The one evasion that backfired and was caught as AI (0.880).
7. `attacker_PI02`: a fake "SYSTEM" message. Labelled "human" (0.2195), but because the odd tokens raised perplexity, not because the instruction was obeyed.
8. `attacker_PI05`: an attempt to inject JSON into the log. The entry is clean; the submitted text is never written to the log.
9. `attacker_MF05`: one very long word. Signal one said 0.9976 but signal two stayed at 0.5; the rule held the score at 0.5.
10. `attacker_flood`: the rate limit rejecting a request (the 429 case). Rejections are logged with `event: rejected`.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03: a careful non-native English speaker, called AI.**

The text (written by a person):

> I want to describe my experience of the first month in this country. The weather was very different from my home. I did not expect the rain to continue for so many days. My colleagues were kind and they helped me to find an apartment. I am still learning the words that people use in the office. Sometimes I do not understand the jokes. But I am happy that I came here and I think it was a good decision for my family.

What came back (`content_id` `7ecc5ae6-c569-4108-b1e3-cd88f94e4e9a`): `model_score` 0.8051, `style_score` 0.6024, combined 0.70375, `guess` "ai", with the label "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it."

Why it is the worst: the writer did nothing wrong. Someone writing carefully in a second language sticks to vocabulary they are sure of and keeps sentences short and plain, which is exactly what signal one rewards as "predictable" and signal two reads as "even". Both signals agree (they differ by only 0.2027, under the 0.3 limit), so the disagreement rule that rescued FP04, FP06 and FP07 never fires. The only remedy this writer has is to click Appeal, and an appeal only moves the item to `under_review`. This is the person the project was supposed to protect.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

Criteria 1, 2, 3 and 5 were run with `python run_eval.py --label before` (three
trials each; the report is `results/run_2026-11-17_0156_before.md`). Criterion 4
cannot be run through `/submit`, so `run_appeal_check.py` runs it: five appeals
per run, three runs (`results/appeal_check_2026-11-17_0156_before.md`,
`..._0217_before_run2.md`, `..._0217_before_run3.md`). Every trial of every
criterion came back with exactly the same numbers as the first, so the three
columns match.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | Of my 10 own pieces, at most 1 is called "likely AI" | 0 of 10 | 0 of 10 | 0 of 10 | **MET** (mostly because of the unsure band, see below) |
| 2. Score spread | AI group's average combined score at least 0.5 above the human group's | gap 0.132 | gap 0.132 | gap 0.132 | **MISSED** |
| 3. Unsure label | Of 10 human pieces with two sentences AI-rewritten, at least 5 come back "unsure" | 8 of 10 | 8 of 10 | 8 of 10 | **MET** |
| 4. Appeals work | 5 appeals, each: status `under_review` and one new appeal entry in the log | 5 of 5 | 5 of 5 | 5 of 5 | **MET** |
| 5. Bad input | Missing `text`, whitespace-only `text`, and `text` over 10,000 characters each return 400 with a message, with no crash | 0 of 3 | 0 of 3 | 0 of 3 | **MISSED** |

**Real output from one trial**, pasted as text, naming the file and function
that produced it. Everything below is copied from the report files; the
objects are produced by `run_eval.py::main`, which calls `app.py::submit`.

*Criterion 1 (trial 1, 2 of the 10 pieces: one labelled "human", and the one
closest to the AI line).* Across all ten the labels were 8 unsure, 2 human and
0 AI:

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.25725,
    "model_score": 0.3506,
    "style_score": 0.1639,
    "label": "We think this was most likely written by you. Your post has been submitted.",
    "sent": "How do you get up to speed in a field you have never worked in before?"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5229,
    "model_score": 0.6471,
    "style_score": 0.3987,
    "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
    "sent": "Tell me about a time you proactively discovered a problem without bein"
  }
]
```

*Criterion 2 (trial 1, 2 of the 6 texts: `ai02_teamwork`, the only AI text
called AI, and `ai03_climate`, pushed to 0.5).* AI group average 0.598, human
group average 0.466, gap 0.132:

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7696000000000001,
    "model_score": 0.8519,
    "style_score": 0.6873,
    "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.",
    "sent": "Technology is an important part of our daily lives. It helps people to"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.8709,
    "style_score": 0.5113,
    "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
    "sent": "Climate change is one of the most pressing challenges facing our world"
  }
]
```

*Criterion 3 (trial 1, 1 of the 10 mixed pieces: `h07` with two sentences
rewritten). Its original scored `confidence` 0.523 in criterion 1; the rewrite
scored 0.521.* All ten: 8 unsure, 2 human, 0 AI:

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.52105,
    "model_score": 0.6561,
    "style_score": 0.386,
    "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
    "sent": "Tell me about a time you proactively discovered a problem without bein"
  }
]
```

*Criterion 4 (run 1, the report table, produced by `run_appeal_check.py`).*

```
| # | content_id | HTTP status | status returned | new appeal entries in log | Result |
| 1 | `b72b154b-f508-4f08-b020-379c34b5d8e8` | 200 | under_review | 1 | PASS |
| 2 | `c660386c-c942-4a27-9298-02b8075c6bc3` | 200 | under_review | 1 | PASS |
| 3 | `8c9542bc-f296-4fd6-8748-f103c99499ae` | 200 | under_review | 1 | PASS |
| 4 | `4ffd2da1-f0b2-40b8-8f73-905962c1ced5` | 200 | under_review | 1 | PASS |
| 5 | `ff219342-7322-47e2-9074-4323d366169c` | 200 | under_review | 1 | PASS |
```

*Criterion 5 (trial 1, all three bad inputs, each sent with a `creator_id`).* The
first has `status` null because the reply was an HTML error page, not JSON:

```json
[
  {
    "status": null,
    "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5302,
    "model_score": 0.5604,
    "style_score": 0.5,
    "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
    "sent": "   \n   "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.9985999999999999,
    "model_score": 0.9972,
    "style_score": 1.0,
    "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.",
    "sent": "The quick brown fox jumps over the lazy dog. The quick brown fox jumps"
  }
]
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

**Criterion 2: MISSED. Stage: the combining rule (`scoring.py::combine_signals`),
on top of a narrow signal two.** The two groups sit in the middle of the scale
instead of at opposite ends:

| Text | Group | Signal one | Signal two | Combined |
|---|---|---|---|---|
| `ai01_remote_work` | AI | 0.6119 | 0.4356 | 0.524 |
| `ai02_teamwork` | AI | 0.8519 | 0.6873 | 0.770 |
| `ai03_climate` | AI | 0.8709 | 0.5113 | 0.500 |
| `2_casual_human` | mine | 0.5409 | 0.2087 | 0.500 |
| `h05` | mine | 0.4776 | 0.2733 | 0.375 |
| `h07` | mine | 0.6471 | 0.3987 | 0.523 |

Two things happen. First, my rule returns 0.5 whenever the signals differ by
more than 0.3. `ai03_climate` has signal one at 0.8709 and signal two at 0.5113
(a difference of 0.36), so a text that signal one is sure about is pulled down to
the middle; a plain average would have given it 0.691. Second, signal two does not
separate the groups much: its range across all six texts is 0.21 to 0.69, and
only one AI text clears 0.6. So even a plain average would give a gap of about
0.24, not 0.5. The rule makes the gap smaller (0.132 instead of about 0.24), but
the target of 0.5 was out of reach of these two signals either way.

**Criterion 5: MISSED. Stage: the route (`app.py::submit`).** `submit()` does no
input checking. With no `text` field it passes `None` to the model, which raises
`ValueError`, and the service answers with an HTML error page (a crash, not a
400). Whitespace-only text is accepted and scored (200, "unsure", 0.53). A 13,500
character text is also accepted, and because it is one sentence repeated 300
times it is scored `ai` at 0.999 (signal two at 1.0, since repetition makes the
sentences identical in length). None of the three is rejected. The same missing
check explains the nine `500` crashes the script found in the attack run.

**Criterion 1: MET, but honestly, mostly because of the unsure band.** None of my
ten pieces was called AI, but that is largely because the system says "unsure"
for almost everything: 8 of the 10 came back unsure and only 2 were called human.
The highest combined score was 0.523, well under the 0.65 line, so nothing came
close to being accused. That is a pass on the target as written, but it does not
show the system recognises human writing; it shows the system rarely commits.
Criterion 3 passes the same way: all ten mixed pieces got the same labels as
their originals, so the AI rewrites changed nothing the system could see.

**The pattern: the disagreement rule protects real writers, but costs
separation.** In the attack run it rescued three real people who a plain average
would have called AI (FP04, FP06 and FP07), which is what I wanted. The price is
that scores bunch up near 0.5. Across the 26 texts in criteria 1 to 3, 21 came
back unsure, 4 human and 1 AI. The same rule that stops a confident signal one
from accusing a plain writer also stops it from catching AI text when signal two
disagrees (`ai03_climate`). Fewer wrong accusations and less separation between
AI and human text come from the same setting; I cannot have one without the
other.

---

## The Improvement

**What I changed:** I added input checks to `app.py::submit()` and changed
nothing else (not the signals, the combining rule, the thresholds or the rate
limit). Before anything is scored, `submit()` now refuses, with HTTP 400, an `error`
code and one plain sentence, any request where:

- the body is not a JSON object (`invalid_body`);
- `text` is missing or `null` (`missing_text`);
- `text` is not a string (`text_not_string`);
- `text` is empty once spaces are stripped (`empty_text`);
- `text` is longer than 10,000 characters (`text_too_long`);
- `text` is too short for the model to score (`text_too_short`), caught from the
  `ValueError` that `detector.model_signal` raises.

Every one of these is also written to the audit log with `audit.log_rejection`,
so a refused request leaves a trace (`event: rejected`, `reason: <code>`).

**Which diagnosis pointed at it:** The criterion 5 diagnosis (stage: the route,
`app.py::submit`, which did no input checking). The same missing check explained
all nine `500` crashes the script found in the first attack run, plus the two
inputs `criteria.md` says must be refused but were accepted: whitespace-only text
(MF01) and a 60,000-character text (MF08). One stage, one cause, thirteen BROKE
attacks and one missed criterion. I chose this over criterion 2 because criterion
2 needs a better second signal, which is a much larger change.

**Before and after, side by side**

Criteria (`run_eval.py`, three trials each; criterion 4 by `run_appeal_check.py`):

| Criterion | Before | After | Verdict before | Verdict after |
|---|---|---|---|---|
| 1. At most 1 of my 10 called AI | 0 of 10 (all 3 trials) | 0 of 10 (all 3 trials) | MET | MET |
| 2. AI group 0.5 above human group | gap 0.132 | gap 0.132 | MISSED | MISSED |
| 3. At least 5 of 10 mixed pieces unsure | 8 of 10 | 8 of 10 | MET | MET |
| 4. Five appeals all `under_review` and logged | 5 of 5 (3 runs) | 5 of 5 (1 run) | MET | MET |
| 5. Three bad inputs return 400 | 0 of 3 (all 3 trials) | **3 of 3 (all 3 trials)** | MISSED | **MET** |

Attack set, by family (the full per-attack results are in the two report files):

| Family | Attacks | BROKE before | BROKE after | HELD before | HELD after |
|---|---|---|---|---|---|
| evasion | 10 | 7 | 7 | 3 | 3 |
| false_positive | 8 | 3 | 3 | 5 | 5 |
| prompt_injection | 6 | 1 | 1 | 5 | 5 |
| malformed | 20 | 13 | **0** | 7 | **20** |
| flood_same_creator | 12 | 0 | 0 | 12 | 12 |
| **Total** | **56** | **24** | **11** | **32** | **45** |

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

The same 56 attacks, rerun after the fix with rate limiting on. The full report
is `results/attack_run_2026-11-17_0232_after.md`. Result: **11 BROKE, 45 HELD**
(first run: 24 BROKE, 32 HELD). The script found no crashes this time (0 auto-marked
BROKE, down from 9). I marked them with the same rule as before. RQ10 and RQ11
again returned `429` in the run, because earlier requests with no `creator_id`
had used up that IP address's allowance; as before, I waited 65 seconds and sent
each again on its own, and both returned `400` (`invalid_body`), so they are HELD.

| ID | Family | What it targets | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.500 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.452 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.500 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.561 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.303 | HELD |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.467 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.500 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.377 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.500 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.880 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.560 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.684 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.704 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.500 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.730 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.500 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.500 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.374 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.398 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.220 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.475 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.398 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.500 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.526 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | unsure | 0.500 | HELD |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.500 | HELD |
| MF05 | malformed | text is a very long single word | 200 | unsure | 0.500 | HELD |
| MF06 | malformed | text is emoji only | 200 | unsure | 0.500 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | unsure | 0.500 | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | unsure | 0.370 | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | unsure | 0.500 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |

**Ten audit log entries from the run**

```json
{"timestamp": "2026-11-17T07:32:31+00:00", "creator_id": "attacker_MF01", "event": "rejected", "status": "rejected", "reason": "empty_text"}
{"timestamp": "2026-11-17T07:32:31+00:00", "creator_id": "attacker_MF02", "event": "rejected", "status": "rejected", "reason": "text_too_short"}
{"timestamp": "2026-11-17T07:32:33+00:00", "creator_id": "attacker_MF08", "event": "rejected", "status": "rejected", "reason": "text_too_long"}
{"timestamp": "2026-11-17T07:32:33+00:00", "creator_id": "attacker_RQ01", "event": "rejected", "status": "rejected", "reason": "missing_text"}
{"timestamp": "2026-11-17T07:32:33+00:00", "creator_id": "attacker_RQ03", "event": "rejected", "status": "rejected", "reason": "text_not_string"}
{"timestamp": "2026-11-17T07:32:33+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "invalid_body"}
{"timestamp": "2026-11-17T07:32:34+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-17T07:32:30+00:00", "content_id": "f12ad226-97a4-4729-a648-3019c4f1d560", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6024, "combined_score": 0.7037500000000001, "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-17T07:32:28+00:00", "content_id": "af4dcb3b-c1ad-4e42-b4ba-8f0789722146", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.2856, "combined_score": 0.3034, "label": "We think this was most likely written by you. Your post has been submitted.", "status": "decided"}
{"timestamp": "2026-11-17T07:32:27+00:00", "content_id": "a8a176e2-f588-4197-8199-72ca6f010d50", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.5185, "combined_score": 0.5, "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.", "status": "decided"}
```

What the ten show, in order:

1. `attacker_MF01`: whitespace-only text, now refused with reason `empty_text`. Before, it was scored and logged as a decision.
2. `attacker_MF02`: a single character, now `text_too_short`. Before, it crashed the route with a 500 and left no log line at all.
3. `attacker_MF08`: 60,000 characters, now `text_too_long`. Before, it was scored.
4. `attacker_RQ01`: no `text` field, now `missing_text`. Before, a 500 crash with no log line.
5. `attacker_RQ03`: `text` is a number, now `text_not_string`.
6. A body that is not a JSON object (a list, empty or unparseable). There is no `creator_id` to read, so it is logged as `unknown` (`invalid_body`).
7. `attacker_flood`: the rate limit still rejecting (the 429 case); unchanged by this fix.
8. `attacker_FP03`: still called AI (0.704). The fix did not touch this.
9. `attacker_EV05`: still labelled human (0.303). Unchanged.
10. `attacker_EV01`: typos added to AI text, still "unsure" (0.5). Unchanged.

Entries 1 to 6 are new: the same inputs used to crash or pass through unlogged, and now each leaves a line saying why it was refused.

**Did it help, and how do I know:** It fixed what it was aimed at. All 13
malformed inputs that were BROKE now return 400 with a message (the attack
report shows 400 for 11 of them; RQ10 and RQ11 returned 400 when sent again on their own), and
criterion 5 went from 0 of 3 to 3 of 3 in all three trials. I also checked that
it changed nothing else: 36 attacks returned 200 in both runs, and all 36 have
exactly the same guess and score as before.

It also shows how little this was. The 11 attacks that are still BROKE are all
about the signals, not the route: 7 evasions, 3 false positives (FP02, FP03,
FP05) and 1 prompt injection (PI02). Criterion 2 is still missed at 0.132.
FP03, the writer I least want to explain this to, is still called AI. A route
that no longer crashes does not make the verdicts any better.

The trade this fix creates, and what it costs:

- **A writer with a long piece now gets a refusal instead of a verdict.** The
  10,000-character limit is the number from criterion 5. Before, a 13,500-character
  text that repeats one sentence was scored `ai` at 0.999 (signal two reads
  repetition as maximally machine-like). Now it is just refused. That removes an
  odd result, but it hides the way signal two reacts to repetition; it does not fix it.
- **A 400 still uses up the rate limit.** Requests without a usable `creator_id`
  share one allowance per IP address, which is why RQ10 and RQ11 were still
  `429` in the run.
- **"Too short" is whatever the model refuses.** It is decided by the tokenizer
  (fewer than three tokens), not by a number I chose, so the line sits in an odd place:
  a one-word submission is refused, a short three-word one is scored.

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

Eleven of the 56 attacks are still BROKE, and criterion 2 is still MISSED. None
of them is a problem with the route any more. They are all about what the two
signals can and cannot see, and they fall into five groups.

**1. Shape tricks on signal two: EV02, EV03, EV06, EV07.** Each one changes the
shape of AI text without changing what it says (broken-up sentences, a pasted
quotation, one very long sentence beside a short one, punctuation padding), and
each pushes `style_score` down to between 0.25 and 0.36.
*What I'd do:* make signal two harder to move: use the median instead of the
standard deviation for sentence length, ignore very short fragments, count how
many different punctuation marks appear rather than how many, and cap how much a
single quoted span can count.
*Why I stopped:* the attack set has only ten evasion cases, so anything I tune
now is fitted to them. These changes could also hurt real writers who use short
sentences (FP07, FP08).

**2. Odd words fool signal one: EV01, EV04, PI02.** Perplexity goes up with any
unusual token, whoever wrote it. Typos took EV01's `model_score` down to 0.1635;
rare words took EV04 to 0.6114, which ended at 0.561, just under the 0.65 line;
and the fake "SYSTEM" message in PI02 scored "human" (0.2195), not because the
system obeyed it (it cannot read instructions) but because the strange tokens made
the text surprising. One mechanism, three attacks.
*What I'd do:* clean the text before scoring (spell-check, strip obvious markup)
or score each sentence separately and take the median, so a few odd tokens cannot
dominate. For EV04 alone I could lower the AI line from 0.65 to about 0.55, but
that would also accuse FP01, who scores 0.560.
*Why I stopped:* cleaning typos changes how the system treats the mistakes of real
and non-native writers, which could make false accusations worse, and
sentence-by-sentence scoring is a redesign of `detector.py`.

**3. A human opening bolted onto AI text: EV09.** Signal one said 0.704 and signal
two said 0.320. They differ by 0.384, so the combining rule returned 0.5.
*What I'd do:* score the text in paragraphs and report "mixed" when the paragraphs
disagree.
*Why I stopped:* the detector only reads the first 400 tokens
(`DETECTOR_MAX_TOKENS`), so later paragraphs are not scored at all; chunking means
reworking `detector.py` and a longer wait per request.

**4. Real writers still called AI: FP02, FP03, FP05.** Both signals agree on these
(signal one 0.74, 0.81 and 0.80; signal two 0.63, 0.60 and 0.66), so the
disagreement rule cannot help, and the combined scores of 0.684, 0.704 and 0.730 sit just above the 0.65 line.
*What I'd do:* the cheap change is to raise `AI_THRESHOLD` from 0.65 to about 0.75.
All three would become "unsure", and in my own data only `ai02_teamwork` (0.770)
and EV10 (0.880) would still be called AI. The lasting fix is a first signal that
does not read plain, careful writing as machine-made, for example one calibrated
against the kind of text being submitted.
*Why I stopped:* the threshold change fixes these three by making the system catch
almost nothing, and I would be choosing 0.75 by looking at the same attacks I am
trying to fix. A better signal needs more than the small local model I have.

**5. Criterion 2: MISSED, gap 0.132 against a target of 0.5.**
*What I'd do:* not lower the target. A missed number stays where it is. I would
work on the signals instead. The two groups bunch near 0.5 for two reasons: signal
two only ranges from 0.21 to 0.69 across the six texts, and the disagreement rule
drags texts where the signals differ by more than 0.3 down to 0.5. Raising that
limit from 0.3 to 0.4 would let `ai03_climate` (0.36 apart, plain average 0.691)
be called AI, but it would also bring back FP04 (0.342 apart, plain average
0.662), who a plain average accuses.
*Why I stopped:* even a plain average gives a gap of only about 0.24, so no setting
reaches 0.5; it needs a better second signal. With six texts in this test, any
value I chose would be fitted to them.

**Known holes I have not fixed**

- **Changing `creator_id` gets around the rate limit.** The limit counts requests
  per `creator_id`, which the sender chooses. A script that sends each request
  under a new id is never limited and looks like a crowd of different people.
  *What I'd do:* also count per IP address, or tie submissions to real accounts.
  *Why I stopped:* this project has no accounts, so every identity is self-declared,
  and counting by IP alone would punish households and offices that share one.
  The counts also live in memory, so a restart resets them.
- **The system cannot tell how much of a text was rewritten.** EV05, a heavy human
  rewrite, came back "human" (0.303), and in criterion 3 all ten pieces with two
  AI-rewritten sentences got the same labels as their originals. A final text does
  not carry the proportion of who wrote what.
  *What I'd do:* compare against the original draft or version history.
  *Why I stopped:* this service never sees a draft, so there is nothing to compare.
  It is also why I marked EV05 HELD.

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

If this ran for real, I would lean toward wrongly accusing fewer people. The cost
is that more AI-written articles would be let through, which readers and careful
authors would pay for, but a wrongly accused author loses more than that.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
