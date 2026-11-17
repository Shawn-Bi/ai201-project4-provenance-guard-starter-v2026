"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

from pathlib import Path

_SAMPLES = Path(__file__).parent / "samples"


def _read(path):
    return Path(path).read_text(encoding="utf-8").strip()


# Ten pieces I wrote myself (criterion 1), and three of them again as the
# "clearly human" group for criterion 2.
HUMAN_FILES = sorted((_SAMPLES / "human").glob("*.txt"))
HUMAN_TEXTS = [_read(p) for p in HUMAN_FILES]

# Three clearly AI-written pieces (criterion 2).
AI_TEXTS = [_read(p) for p in sorted((_SAMPLES / "ai").glob("*.txt"))]

# The three of mine used for criterion 2: a casual message and two narratives.
MY_THREE = [_read(_SAMPLES / "human" / name)
            for name in ("2_casual_human.txt", "h05.txt", "h07.txt")]

# Criterion 3: each of the ten human pieces with two sentences replaced by a
# polished, generic rewrite in the style an AI assistant produces. Each pair is
# (original sentence, rewrite). The original must appear in the file exactly.
AI_REWRITES = {
    "h01.txt": [
        ("At first, we were very relaxed, thinking we had plenty of time; we even ate snacks and chatted.",
         "Initially, the team maintained a relaxed approach, believing that ample time was available to complete the work."),
        ("We completed the demo on time and the core workflow worked.",
         "The team successfully delivered the demo on schedule, with the core workflow functioning as intended."),
    ],
    "h02.txt": [
        ("We could not keep delaying.",
         "Further delays were not a viable option for the organization."),
        ("The plan was adopted, the phased launch proceeded on schedule without a large-scale rollback, and customers received a clear timeline.",
         "The proposal was approved, enabling a smooth phased launch that met its timeline and provided customers with clear expectations."),
    ],
    "h03.txt": [
        ("I needed to produce a first version ready for review within two weeks.",
         "The objective was to deliver a review-ready initial version within a two-week timeframe."),
        ("The first version passed review.",
         "The initial version successfully passed the review process."),
    ],
    "h04.txt": [
        ("My approach was to contain the damage first, identify the cause, and then restore performance.",
         "The strategy involved containing the impact, identifying the root cause, and restoring optimal performance."),
        ("The metrics returned to their pre-change levels that same day.",
         "Key metrics returned to their previous levels within the same day."),
    ],
    "h05.txt": [
        ("She was very cautious and wanted to personally review every pull request (PR).",
         "She adopted a cautious approach and preferred to personally review each pull request (PR)."),
        ("This adjustment worked.",
         "This adjustment proved highly effective in improving collaboration."),
    ],
    "h06.txt": [
        ("I listened carefully to the feedback, shadowed restaurant cashiers during peak hours, and analyzed call-duration data.",
         "I carefully considered the feedback, observed restaurant cashiers during peak hours, and analyzed call-duration data to gain deeper insights."),
        ("So I rewrote the system prompts to be direct, efficient, and responsive.",
         "Consequently, I redesigned the system prompts to be direct, efficient, and highly responsive."),
    ],
    "h07.txt": [
        ("I remember when I was a channel sales manager at Vanke Real Estate.",
         "In my role as a channel sales manager at Vanke Real Estate, I encountered a situation that required proactive attention."),
        ("Fortunately, the back-office technical team got the workflow running before the event began the next day, so partners' interests and the company's reputation were not affected.",
         "Thanks to the dedicated efforts of the technical team, the workflow was restored before the event, safeguarding both partner interests and the company's reputation."),
    ],
    "h08.txt": [
        ("It was especially challenging with older couples running takeout restaurants.",
         "This task proved particularly challenging when working with older couples who operate takeout restaurants."),
        ("Restaurant owners understood the concept on the spot, gained a clearer understanding of how the product would be implemented, and felt more confident in it.",
         "Restaurant owners quickly grasped the concept, developed a clearer understanding of the implementation process, and expressed greater confidence in the product."),
    ],
    "h09.txt": [
        ("A nonnegotiable rule was that the system would provide explainable reasons only, with final decisions remaining with humans.",
         "A critical principle was that the system would offer explainable reasoning exclusively, ensuring that final decisions remained with human reviewers."),
        ("The prototype has a demo and code, but it has not been clinically validated.",
         "While the prototype includes a working demo and codebase, it has not undergone clinical validation."),
    ],
    "2_casual_human.txt": [
        ("What do you think?",
         "What are your thoughts on this plan?"),
        ("Do you know anywhere that has both brands available to try?",
         "Are you aware of any location that offers both brands for hands-on trials?"),
    ],
}


def _mixed(name):
    text = _read(_SAMPLES / "human" / name)
    for original, rewrite in AI_REWRITES[name]:
        assert original in text, f"{name}: sentence not found: {original[:40]}"
        text = text.replace(original, rewrite, 1)
    return text


MIXED_TEXTS = [_mixed(p.name) for p in HUMAN_FILES]


SCENARIOS = [
    {
        # Criterion 1: of my ten pieces, at most 1 is called AI.
        "name": "my own writing",
        "criterion": 1,
        "texts": HUMAN_TEXTS,
    },
    {
        # Criterion 2: the AI group's average combined score is at least 0.5
        # above the human group's. The first three texts are the AI group, the
        # last three are mine; run_eval records them in this order.
        "name": "score spread",
        "criterion": 2,
        "texts": AI_TEXTS + MY_THREE,
    },
    {
        # Criterion 3: of ten human pieces with two sentences rewritten by AI,
        # at least five come back "unsure".
        "name": "mixed edits",
        "criterion": 3,
        "texts": MIXED_TEXTS,
    },
    # Criterion 4 (five appeals) cannot be run through /submit alone: it needs
    # an appeal against a real content_id. It is tested by hand with
    # run_appeal_check.py, which is a separate script. Saying so is part of the
    # write-up.
    {
        # Criterion 5: three bad inputs, each with a creator_id. Each should
        # return 400 and a short message, and the service must not crash.
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},                       # no text field
            {"text": "   \n   ", "creator_id": "eval_bad_blank"},     # only whitespace
            {"text": "The quick brown fox jumps over the lazy dog. " * 300,
             "creator_id": "eval_bad_huge"},                          # over 10,000 characters
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
