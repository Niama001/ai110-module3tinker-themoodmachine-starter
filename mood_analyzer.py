# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
import string
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS

# Matches, in order of priority:
#   1. simple emoticons like :) :-( ;)
#   2. words (letters/digits, keeping apostrophes so "can't" stays whole)
#   3. any other single non-space symbol (this is how emojis get captured)
TOKEN_PATTERN = re.compile(r"[:;]-?[()dp]|[a-z0-9']+|[^\w\s]")

# Words that flip the meaning of the sentiment word right after them.
NEGATIONS = {
    "not", "never", "no", "cannot",
    "can't", "cant", "don't", "dont", "won't", "wont",
    "isn't", "wasn't", "aren't", "didn't", "doesn't",
}


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Steps:
          - Strip whitespace and lowercase everything
          - Remove invisible emoji variation selectors (U+FE0F)
          - Split into words, emoticons, and emojis with a regex
          - Drop plain punctuation tokens like "!" "," "."
        """
        cleaned = text.strip().lower().replace("\ufe0f", "")
        raw_tokens = TOKEN_PATTERN.findall(cleaned)

        tokens = [t for t in raw_tokens if t not in string.punctuation]

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def _analyze_tokens(self, tokens: List[str]) -> Tuple[int, List[str], List[str]]:
        """
        Shared scoring helper used by score_text, predict_label, and explain.

        Returns (score, positive_hits, negative_hits).

        Enhancement: negation handling. If the token immediately before a
        sentiment word is in NEGATIONS, the word's effect is flipped:
          "not happy" -> -1, "not bad" -> +1
        """
        score = 0
        positive_hits: List[str] = []
        negative_hits: List[str] = []

        for i, token in enumerate(tokens):
            negated = i > 0 and tokens[i - 1] in NEGATIONS
            label = f"{tokens[i - 1]} {token}" if negated else token

            if token in self.positive_words:
                if negated:
                    score -= 1
                    negative_hits.append(label)
                else:
                    score += 1
                    positive_hits.append(label)
            elif token in self.negative_words:
                if negated:
                    score += 1
                    positive_hits.append(label)
                else:
                    score -= 1
                    negative_hits.append(label)

        return score, positive_hits, negative_hits

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.
        Enhancement: simple negation handling (see _analyze_tokens).
        """
        tokens = self.preprocess(text)
        score, _, _ = self._analyze_tokens(tokens)
        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the text into a mood label.

        Mapping:
          - both positive AND negative hits -> "mixed"
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        Why the mixed rule looks at hits instead of the score: one positive
        word and one negative word cancel out to a score of 0, which would
        look "neutral". Checking for hits on both sides catches that.
        """
        tokens = self.preprocess(text)
        score, positive_hits, negative_hits = self._analyze_tokens(tokens)

        if positive_hits and negative_hits:
            return "mixed"
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        Uses the same helper as score_text, so the explanation always
        matches the real score (including negation).
        """
        tokens = self.preprocess(text)
        score, positive_hits, negative_hits = self._analyze_tokens(tokens)

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )