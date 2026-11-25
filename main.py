#!/usr/bin/env python3
"""Dad Joke Showdown — one dad joke, written to /output/entry.txt.

The program scores a small slate of original candidate jokes against the
judge's five criteria (dad-joke fit, clean pun, freshness, tightness,
reads aloud) and writes the winner. The joke must be at most 200
characters, plain UTF-8 text, no trailing explanation.
"""

import os
import sys

# Each candidate: (text, pun, fresh, tight, aloud) scored 0-10.
# Weights follow the judge's order: pun first, then fresh, tight, aloud.
CANDIDATES = [
    (
        "The electrician charged me $200 to change a lightbulb. "
        "I was shocked - but he said that's just the current rate.",
        9, 8, 9, 9,
    ),
    (
        "I asked the plumber why he is always so calm. "
        "He said, 'I just go with the flow.'",
        8, 5, 9, 9,
    ),
    (
        "My wife asked me to stop impersonating a flamingo. "
        "I had to put my foot down.",
        8, 6, 8, 9,
    ),
    (
        "I told my suitcase there would be no vacation this year. "
        "Now I'm dealing with emotional baggage.",
        7, 7, 8, 8,
    ),
    (
        "I asked the librarian for a book on paranoia. "
        "She whispered, 'They're right behind you.'",
        6, 7, 8, 8,
    ),
]

WEIGHTS = (5, 4, 3, 2)  # pun, fresh, tight, aloud


def score(candidate):
    _, pun, fresh, tight, aloud = candidate
    return sum(w * s for w, s in zip(WEIGHTS, (pun, fresh, tight, aloud)))


# The two sibling entries for this bounty, kept out of the slate on purpose:
# agen997's lawn joke and hayunkarimun's clock joke. The winner must never
# be byte-identical to either of them.
FORBIDDEN = (
    "I told the lawn I'd mow it. It said, 'Cut it out — I'm already short.'",
    "Why did the clock go to therapy? It had too much time on its hands.",
)


def pick_winner():
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    for candidate in ranked:
        text = candidate[0]
        if text not in FORBIDDEN:
            return text
    raise SystemExit("no allowed candidate left")


def main():
    joke = pick_winner()
    if not (1 <= len(joke) <= 200):
        sys.exit(f"joke is {len(joke)} chars, must be 1-200")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(joke)
    print(joke)
    print(f"({len(joke)} chars)")


if __name__ == "__main__":
    main()
