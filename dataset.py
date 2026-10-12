"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    # --- Part 3 fix: coverage gaps found in evaluation ---
    "hopeful",
    "proud",
    "fire",
    "smiling",
    "🔥",
    "🥹",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    # --- Part 3 fix: coverage gaps found in evaluation ---
    "nervous",
    "ugh",
    "😩",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    # --- My additions ---
    "Lowkey stressed but kind of proud of myself",
    "No cap, that concert was fire 🔥",
    "I absolutely love getting stuck in traffic",
    "ugh monday again 😩",
    "Got the job!!! can't stop smiling 🥹",
    "Excited for the trip but nervous about flying",
    "Going to the store later",
    "That movie was sick",
    "I'm fine 🙂",
    # --- Part 4 additions ---
    "What a great day, nothing could bring me down",
    "This homework is so boring, I can't focus",
    "Honestly not bad at all",
    "Waiting in line for an hour, love that for me 🙄",
    "Kinda sad it's over but so grateful for the memories",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    # --- My additions ---
    "mixed",     # "Lowkey stressed but kind of proud of myself"
    "positive",  # "No cap, that concert was fire 🔥"
    "negative",  # "I absolutely love getting stuck in traffic" (sarcasm)
    "negative",  # "ugh monday again 😩"
    "positive",  # "Got the job!!! can't stop smiling 🥹"
    "mixed",     # "Excited for the trip but nervous about flying"
    "neutral",   # "Going to the store later"
    "positive",  # "That movie was sick" (slang)
    "neutral",   # "I'm fine 🙂" (edge case, could be read as negative)
    # --- Part 4 additions ---
    "positive",  # "What a great day, nothing could bring me down"
    "negative",  # "This homework is so boring, I can't focus"
    "positive",  # "Honestly not bad at all" (negation)
    "negative",  # "Waiting in line for an hour, love that for me 🙄" (sarcasm)
    "mixed",     # "Kinda sad it's over but so grateful for the memories"
]

# Safety check: crash early with a clear message if the lists drift apart.
assert len(SAMPLE_POSTS) == len(TRUE_LABELS), (
    f"SAMPLE_POSTS has {len(SAMPLE_POSTS)} items but "
    f"TRUE_LABELS has {len(TRUE_LABELS)}"
)