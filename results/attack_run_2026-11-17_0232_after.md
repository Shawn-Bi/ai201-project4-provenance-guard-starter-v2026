# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-17 02:32
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `a8a176e2-f588-4197-8199-72ca6f010d50` | unsure | 0.500 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `87c74f1a-9f00-4390-bacd-4d4fd1756e38` | unsure | 0.452 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `3cf70667-2160-4baa-bf80-267a5883ed9f` | unsure | 0.500 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `74af379d-9f74-464e-800a-b9b1f4534acf` | unsure | 0.561 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `af4dcb3b-c1ad-4e42-b4ba-8f0789722146` | human | 0.303 | HELD |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `7d48ae90-222a-444e-82ac-484e852038f3` | unsure | 0.467 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c59e4608-2549-447c-9dd8-660764593f05` | unsure | 0.500 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `861db87a-058c-4470-b84e-7ff6d747fcf1` | unsure | 0.377 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `5be37950-6b58-472f-8a94-06aa4439d878` | unsure | 0.500 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `193379a1-499e-4a23-92ea-0f93c4286bdc` | ai | 0.880 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `977ef0ba-51ad-4c40-90b3-2164af033ca8` | unsure | 0.560 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `79eac5e6-fc7d-4d5b-9921-d85cf0f2d9ea` | ai | 0.684 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `f12ad226-97a4-4729-a648-3019c4f1d560` | ai | 0.704 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `30e21ada-c658-4ff0-80d3-839a43b500df` | unsure | 0.500 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `a0b96de6-7a73-4475-a499-cbdce3ff18fd` | ai | 0.730 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `43cb3455-1959-4128-b469-95a698cb6d78` | unsure | 0.500 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `f4bb6d67-3215-4c71-906b-da2f7ff2a0ff` | unsure | 0.500 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `12ddb4db-68f6-415d-b58f-c3f7297d6445` | unsure | 0.374 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `fbd0f7cb-cd94-49e3-809a-e38718a7aeaa` | unsure | 0.398 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `f071c19b-72db-4c97-97ad-20f9324bab6d` | human | 0.220 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `5ac47979-72e9-4e2b-8cfa-711730130975` | unsure | 0.475 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c140849e-e0a0-42db-98ca-68b1f036b157` | unsure | 0.398 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `6e4f3db3-bfc2-479f-85f5-4041959c16d5` | unsure | 0.500 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `faad4aec-2054-4895-bbc6-3577af89e1ab` | unsure | 0.526 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `21a25bd6-956e-48b5-a987-f018722306ca` | unsure | 0.500 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `806d18c9-a7e4-4039-a993-491b5aea7d82` | unsure | 0.500 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `68cf8ad6-16bc-4914-b6b1-bd7dfed8336f` | unsure | 0.500 | HELD |
| MF06 | malformed | text is emoji only | 200 | `ed5b59b4-62c2-4fb6-be91-4667e2f10ed6` | unsure | 0.500 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `69e3e849-35ff-4fb0-8ca2-7231a655e8fb` | unsure | 0.500 | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `ec4fd741-3230-4153-965e-259dce3acc25` | unsure | 0.370 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `3f51ddeb-a344-441e-b641-9c98b570dc4e` | unsure | 0.500 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `148316d5-f0b0-4e10-8ab6-ba5c39baaa76` | unsure | 0.500 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1ba065c6-e1d4-4d10-bb1b-f8978258a317` | unsure | 0.500 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0982e1fb-a754-4d73-9627-6ce4d1f95cdf` | unsure | 0.500 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b5318332-0f74-46e4-b500-506a11bee467` | unsure | 0.500 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9dbba60d-5de8-445e-9a67-676fcca720d2` | unsure | 0.500 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## Verdicts

All 56 attacks judged: **11 BROKE**, **45 HELD**.

| Family | Attacks | BROKE | HELD |
|---|---|---|---|
| `evasion` | 10 | 7 | 3 |
| `false_positive` | 8 | 3 | 5 |
| `prompt_injection` | 6 | 1 | 5 |
| `malformed` | 20 | 0 | 20 |
| `flood_same_creator` | 12 | 0 | 12 |

Same judging rule as the first run (`attack_run_2026-11-17_0123.md`): an evasion is
BROKE when AI-derived text did not get the AI label; a false positive is BROKE
when genuine human text got the AI label; a malformed input is BROKE when the
service crashed or accepted what criterion 5 says must return 400; a flood is
HELD when the limit held. EV05 is HELD for the same reason as before: a person
rewrote it, and the system cannot measure how much.

Notes:

- **RQ10 and RQ11 (HELD, re-sent):** as in the first run, both came back `429`
  because earlier requests with no usable `creator_id` had used up that IP
  address's 5-per-minute allowance, so the handler never ran. After waiting 65
  seconds I sent each again on its own with the same body and content type.
  Both returned `400` (`invalid_body`). The table above keeps the original `429`.
- **What changed from the first run:** only malformed inputs. All 13 that were
  BROKE (MF01, MF02, MF08, RQ01, RQ03, RQ04, RQ05, RQ07, RQ08, RQ09, RQ10,
  RQ11, RQ12) now return `400`. Every other attack has the same status, guess
  and score as before.

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "a8a176e2-f588-4197-8199-72ca6f010d50",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.1635,
  "style_score": 0.5185,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "87c74f1a-9f00-4390-bacd-4d4fd1756e38",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.45245,
  "model_score": 0.5943,
  "style_score": 0.3106,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "3cf70667-2160-4baa-bf80-267a5883ed9f",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6662,
  "style_score": 0.3003,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "74af379d-9f74-464e-800a-b9b1f4534acf",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.56125,
  "model_score": 0.6114,
  "style_score": 0.5111,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "af4dcb3b-c1ad-4e42-b4ba-8f0789722146",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3034,
  "model_score": 0.3212,
  "style_score": 0.2856,
  "label": "We think this was most likely written by you. Your post has been submitted.",
  "error": null,
  "verdict": "HELD"
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "7d48ae90-222a-444e-82ac-484e852038f3",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4668,
  "model_score": 0.5727,
  "style_score": 0.3609,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c59e4608-2549-447c-9dd8-660764593f05",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5862,
  "style_score": 0.2512,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "861db87a-058c-4470-b84e-7ff6d747fcf1",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.37734999999999996,
  "model_score": 0.2452,
  "style_score": 0.5095,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "5be37950-6b58-472f-8a94-06aa4439d878",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.7042,
  "style_score": 0.3202,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "193379a1-499e-4a23-92ea-0f93c4286bdc",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8802,
  "model_score": 0.9792,
  "style_score": 0.7812,
  "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "977ef0ba-51ad-4c40-90b3-2164af033ca8",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5601,
  "model_score": 0.6175,
  "style_score": 0.5027,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "79eac5e6-fc7d-4d5b-9921-d85cf0f2d9ea",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.68445,
  "model_score": 0.7387,
  "style_score": 0.6302,
  "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "f12ad226-97a4-4729-a648-3019c4f1d560",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7037500000000001,
  "model_score": 0.8051,
  "style_score": 0.6024,
  "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "30e21ada-c658-4ff0-80d3-839a43b500df",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8329,
  "style_score": 0.4911,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "a0b96de6-7a73-4475-a499-cbdce3ff18fd",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7297,
  "model_score": 0.8005,
  "style_score": 0.6589,
  "label": "Our system thinks AI may have been involved in writing this. This is an automatic guess and may be wrong. If you wrote it yourself, click Appeal and a person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "43cb3455-1959-4128-b469-95a698cb6d78",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8814,
  "style_score": 0.4539,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "f4bb6d67-3215-4c71-906b-da2f7ff2a0ff",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8816,
  "style_score": 0.5529,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "12ddb4db-68f6-415d-b58f-c3f7297d6445",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3742,
  "model_score": 0.3223,
  "style_score": 0.4261,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "fbd0f7cb-cd94-49e3-809a-e38718a7aeaa",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.39790000000000003,
  "model_score": 0.4625,
  "style_score": 0.3333,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "f071c19b-72db-4c97-97ad-20f9324bab6d",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2195,
  "model_score": 0.2044,
  "style_score": 0.2346,
  "label": "We think this was most likely written by you. Your post has been submitted.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "5ac47979-72e9-4e2b-8cfa-711730130975",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4746,
  "model_score": 0.5943,
  "style_score": 0.3549,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c140849e-e0a0-42db-98ca-68b1f036b157",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.3983,
  "model_score": 0.4998,
  "style_score": 0.2968,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "6e4f3db3-bfc2-479f-85f5-4041959c16d5",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6401,
  "style_score": 0.0714,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "faad4aec-2054-4895-bbc6-3577af89e1ab",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.52575,
  "model_score": 0.5583,
  "style_score": 0.4932,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "21a25bd6-956e-48b5-a987-f018722306ca",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "806d18c9-a7e4-4039-a993-491b5aea7d82",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "68cf8ad6-16bc-4914-b6b1-bd7dfed8336f",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "ed5b59b4-62c2-4fb6-be91-4667e2f10ed6",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "69e3e849-35ff-4fb0-8ca2-7231a655e8fb",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "ec4fd741-3230-4153-965e-259dce3acc25",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.36975,
  "model_score": 0.2395,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "3f51ddeb-a344-441e-b641-9c98b570dc4e",
  "creator_id": {
    "id": "x"
  },
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0492,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "148316d5-f0b0-4e10-8ab6-ba5c39baaa76",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "1ba065c6-e1d4-4d10-bb1b-f8978258a317",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "0982e1fb-a754-4d73-9627-6ce4d1f95cdf",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "b5318332-0f74-46e4-b500-506a11bee467",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "9dbba60d-5de8-445e-9a67-676fcca720d2",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell who wrote this. It will be shown normally and won't be flagged. If you have questions, you can appeal at any time.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```
