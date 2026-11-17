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



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
