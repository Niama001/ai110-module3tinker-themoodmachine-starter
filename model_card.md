# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

I built and evaluated both and compared them on the same dataset.

## 1. Model Overview

**Model type:**  
I compared both models: the rule based classifier and the ML classifier.

**Intended purpose:**  
Classify short, social-media-style text messages as one of four moods: positive, negative, neutral, or mixed.

**How it works (brief):**  
The rule based model lowercases the text, splits it into tokens (words, emoticons, and emojis), and looks each token up in a positive word list and a negative word list. Each positive hit adds 1 and each negative hit subtracts 1. If a negation word ("not", "never", "can't", etc.) comes directly before a sentiment word, that word's effect is flipped. If the text has both a positive hit and a negative hit it is labeled "mixed". Otherwise a score above 0 is "positive", below 0 is "negative", and 0 is "neutral".

The ML model is trained on the labeled posts in `dataset.py`. It learns which words tend to appear with which labels, and then predicts a label for new text based on those learned patterns. [Verify the exact vectorizer and classifier in `ml_experiments.py` and name them here.]

## 2. Data

**Dataset description:**  
`SAMPLE_POSTS` has 20 posts. The starter had 6. I added 9 in Part 1 and 5 more in Part 4. Label counts: 7 positive, 6 negative, 4 mixed, 3 neutral.

**Labeling process:**  
I labeled each new post by the overall feeling I thought the writer meant, not just by which words appeared. For example, "I absolutely love getting stuck in traffic" is labeled negative because I read it as sarcasm. Posts with two opposing feelings joined by "but" are labeled mixed.

Hard or debatable labels:
- "I'm fine 🙂" is labeled neutral, but could reasonably be negative (passive-aggressive) or positive.
- "That movie was sick" is labeled positive, but "sick" could also mean ill.
- "This is fine" (from the starter) is labeled neutral, but could be sarcasm.

**Important characteristics of your dataset:**  
- Contains slang ("lowkey", "no cap", "fire", "sick") and emojis (🔥 😩 🥹 🙂 🙄)
- Includes two sarcasm posts (traffic, and "love that for me 🙄")
- Includes four mixed-feeling posts
- Includes short, ambiguous messages ("This is fine", "I'm fine 🙂")

**Possible issues with the dataset:**  
- It is very small (20 posts), so one post can change results a lot.
- Slightly imbalanced: only 3 neutral and 4 mixed posts.
- All of the posts were written by me, in one voice, so the slang reflects one narrow slice of casual English.
- Several posts were added after I saw the model fail on them, so the dataset is shaped by the model's weaknesses rather than being a neutral sample.

## 3. How the Rule Based Model Works

**Your scoring rules:**  
- Each positive-list word is +1, each negative-list word is -1 (all words weighted equally).
- **Enhancement: negation handling.** If the token right before a sentiment word is in a negation set, the word's score flips ("not happy" is -1, "not bad" is +1, "not nervous" is +1).
- **Mixed rule:** if there is at least one positive hit and at least one negative hit, the label is "mixed" instead of letting the scores cancel to "neutral".
- **Emoji handling:** emojis are kept as their own tokens, and I added a few to the word lists (🔥 🥹 as positive, 😩 as negative).
- **Word list fix (Part 3):** after evaluation I added missing words: positive (`hopeful`, `proud`, `fire`, `smiling`) and negative (`nervous`, `ugh`).

**Strengths of this approach:**  
- Fully traceable: every prediction can be explained token by token with `explain()`.
- Handles simple negation ("I am not happy about this" is correctly negative).
- Handles plain, clearly worded text well ("Today was a terrible day").

**Weaknesses of this approach:**  
- Words not in the lists score 0, so unfamiliar slang and emojis are invisible. Before my word-list fix, accuracy was 0.47 on the first 15 posts; after it, 0.87.
- It cannot detect sarcasm: "I absolutely love getting stuck in traffic" is predicted positive because "love" is the only word that hits a list.
- It ignores context, so one word has one meaning. Adding `fire` fixed "that concert was fire 🔥" but now "the building is on fire" is also predicted positive.
- Negation only looks one token back, so something like "not very happy" would not be caught. [Test this to confirm before keeping the sentence.]
- "sick" is left out of the lists on purpose because it is positive in one sentence and negative in another, so "That movie was sick" is predicted neutral.

## 4. How the ML Model Works

**Features used:**  
Bag of words using CountVectorizer. Each post is turned into a vector of word counts, and the classifier learns which words go with which labels. It ignores word order and context.

**Training data:**  
Trained on `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py`, the same data used to score the rule based model.

**Training behavior:**  
Accuracy was 1.00 with 15 posts and stayed at 1.00 with 20 posts. It learned both sarcasm posts because I labeled them, even though the rule based model failed on them. On sentences that were not in the dataset, it got about 2 of 5 right (see Evaluation).

**Strengths and weaknesses:**  
- Strength: it learns patterns from labels automatically, with no word lists to maintain, and it can pick up sarcasm if it has labeled examples.
- Weakness: it overfits. Its 1.00 is accuracy on the data it trained on, which does not show how it handles new text.
- Weakness: its mistakes are harder to explain. For example, "this homework is so boring" was predicted positive, possibly because "so" appeared in positive training posts ("so much", "So excited"). This is my guess; I did not inspect the model's weights.

## 5. Evaluation

**How you evaluated the model:**  
I ran both models on the labeled posts in `dataset.py` and compared their predictions to `TRUE_LABELS`. I also tried five sentences that are not in the dataset.

| | 15 posts (after word-list fix) | 20 posts |
|---|---|---|
| Rule based | 0.87 | 0.80 |
| ML | 1.00 | 1.00 |

Important: the ML number is training accuracy (same data for training and testing), and I picked the word-list additions after looking at these same posts, so neither number is a clean test.

On five unseen sentences, the rule based model got 3 right and the ML model got about 2 right:

| Sentence | Rule based | ML | My label |
|---|---|---|---|
| I hate waiting in line | negative | negative | negative |
| what a great day | positive | negative | positive |
| this homework is so boring | negative | positive | negative |
| I love sitting in traffic | positive | negative | negative (sarcasm) |
| the building is on fire | positive | positive | negative |

**Examples of correct predictions:**  
- "I am not happy about this" (rule based: negative). Tokens: `i, am, not, happy, about, this`. "happy" is positive, but the preceding "not" flips it to -1, so the label is negative.
- "Lowkey stressed but kind of proud of myself" (rule based: mixed). "stressed" is a negative hit and "proud" is a positive hit, so the mixed rule fires.
- "I absolutely love getting stuck in traffic" (ML: negative). Correct, but likely because I labeled this exact post, not because the model understands sarcasm.

**Examples of incorrect predictions:**  
- "I absolutely love getting stuck in traffic" (rule based: positive, true: negative). Only "love" hit a list (+1), so the score is +1. The model has no way to see the contradiction with "stuck in traffic".
- "Waiting in line for an hour, love that for me 🙄" (rule based: positive, true: negative). Same failure as above; the 🙄 emoji is not in the lists.
- "Kinda sad it's over but so grateful for the memories" (rule based: negative, true: mixed). "grateful" is not in the positive list, so only "sad" hit.
- Difference between the models: the rule based model's errors trace to a missing word or missing context, while the ML model's errors on unseen sentences ("what a great day" predicted negative) trace to having seen almost no examples of those words.

## 6. Limitations

- The dataset is tiny (20 posts), so the ML model cannot generalize and the rule based word lists cover only a small vocabulary.
- Neither model reliably detects sarcasm. The rule based model fails on it by design; the ML model only gets the sarcasm posts I labeled.
- The rule based model depends on exactly the words I put in the lists, and the same word always counts the same way regardless of context ("fire").
- Accuracy numbers are on the same data used to build the models, so they overstate how well either would do on new text.
- It only handles short posts in English.

## 7. Ethical Considerations

- **Misclassifying distress:** a message like "I'm fine 🙂" can hide real distress. A model that reads it as neutral could miss someone who needs support. Mood detection should not be used to make decisions about a person's wellbeing without human review.
- **Overt bias (style):** In my evaluation, nearly every early miss was on informal language (slang, emojis, casual phrasing), while formal wording like "Today was a terrible day" worked from the start. That means this model serves people who write in a standard, formal style better than people who write in slang or other community-specific language. The same word can also carry different meanings across communities ("sick", "fire"), which a single fixed word list cannot capture. I documented this and did not fix it. My own word lists reflect only the slang I know, which is a narrow slice of English.
- **Privacy:** analyzing people's personal messages for mood raises consent and privacy concerns.

### Covert compliance: what my AI assistant did

During the lab, the assistant I used wrote some of the code and word-list changes. What it flagged on its own: that "sick" is ambiguous and should be left out of the lists, that "fire" could misfire in other contexts, that choosing words from my own test posts inflates the score (overfitting), and that the ML model's 1.00 is only training accuracy. What it did not flag: that the word lists and example posts reflect a narrow slice of English slang, or whether words like "fire" and "lowkey" read differently across communities. It also wrote the logic and word lists itself instead of having me justify them.

## 8. Ideas for Improvement

- Add many more labeled posts, from more than one writer and in more language styles.
- Hold out a real test set, so accuracy is measured on posts the model did not train on.
- Use TF-IDF instead of raw word counts for the ML model.
- Look back further than one token for negation, so "not very happy" is handled.
- Add weighted words (for example "hate" stronger than "annoyed") and more emoji handling, including 🙄.
- Try a small neural network or transformer model, which can handle context like sarcasm better than word counts.