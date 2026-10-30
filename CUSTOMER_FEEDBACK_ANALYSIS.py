"""Customer Feedback Analyzer (Sentiment and Data Masking).
For each message the program:
  1. finds and masks e-mails, phone numbers and card numbers
  2. cleans the text and splits it into words
  3. scores the sentiment (with negation like "not good")
  4. counts keywords and shows the top five
  5. checks for spam
"""
# Word lists (sets)
POSITIVE = {"good", "great", "excellent", "love", "like", "happy",
            "fast", "quick", "helpful", "smooth", "recommend",
            "friendly", "comfortable"}
NEGATIVE = {"bad", "terrible", "worst", "slow", "broken", "disappointed",
            "late", "rude", "useless", "problem", "crashing", "flimsy",
            "refund", "failed"}
NEGATIONS = {"not", "no", "never", "dont", "isnt", "wasnt", "didnt"}
STOP_WORDS = {"the", "and", "was", "for", "this", "that", "with", "but",
              "very", "are", "you", "your", "not", "our", "its", "now"}
SUSPICIOUS = {"winner", "prize", "lottery", "click", "claim", "urgent"}
PUNCTUATION = "!\"#$%&()*+,-./:;<=>?@[\\]^_`{|}~"

# 15 sample messages: tuples of (message, expected sentiment)
SAMPLES = [
    ("I absolutely love this phone! The battery is great and delivery was fast. Highly recommend.", "Positive"),
    ("Terrible experience. The screen arrived broken and support was rude. I want a refund.", "Negative"),
    ("The product is not good. It stopped working after two days.",
     "Negative"),
    ("Package arrived on Tuesday. Box was medium sized.", "Neutral"),
    ("Please call me on 9876543210 about my order, the delivery was late.My email is riya.sharma@example.com", "Negative"),
    ("I paid with card 4111111111111234 but the payment failed twice.Very disappointed, please refund.", "Negative"),
    ("Great value, not bad at all, the sound is excellent!", "Positive"),
    ("CLICK HERE NOW!!!! You are a WINNER. CLAIM YOUR PRIZE at http://win-big.example", "Neutral"),
    ("Soooooo happy with the service!!! Support was helpful and friendly.", "Positive"),
    ("The app is slow and keeps crashing. Not helpful support either,never solved my problem.", "Negative"),
    ("Okay product. Some features are good but the battery is bad.",
     "Neutral"),
    ("Contact me at amit_k99@shop-mail.example or 9123456780 for the invoice. Thanks, great service.", "Positive"),
    ("I don't like the colour, it isn't comfortable and the strap is flimsy. Wasn't happy.", "Negative"),
    ("Card 5500000000000004 was charged once. Smooth checkout and quick delivery!", "Positive"),
    ("Customer care is useless!!!!! Worst service ever, call me on 9012345678", "Negative"),
]
# Input: type your own message, or press Enter to run the samples
while True:
    typed = input("Type a message (or press Enter for the 15 samples): ")
    if len(typed) <= 500:
        break
    print("Too long! Please use at most 500 characters.")

if typed.strip() == "":
    to_check = SAMPLES
else:
    to_check = [(typed, "")]

passed = 0
tested = 0

for message, expected in to_check:
    text = message.strip()

    # ---------- 1. Extract and mask ----------
    emails = []
    phones = []
    cards = []
    masked = text    # safe copy to store
    content = text   # copy without secrets, used for analysis

    for token in text.split():
        token = token.strip(".,!?;:")
        if "@" in token:
            at = token.find("@")
            name = token[:at]                         # SLICE 1
            domain = token[at + 1:]                   # SLICE 2
            ending = domain[domain.rfind(".") + 1:]   # SLICE 3
            if name != "" and "." in domain and ending.isalpha():
                emails.append(token)
                hidden = name[:1] + "*" * (len(name) - 1)   # SLICE 4
                masked = masked.replace(token, hidden + token[at:])
                content = content.replace(token, " ")       # SLICE 5
        elif token.isdigit() and len(token) == 10:
            phones.append(token)
            masked = masked.replace(token, "******" + token[-4:])  # SL 6
            content = content.replace(token, " ")
        elif token.isdigit() and len(token) == 16:
            cards.append(token)
            masked = masked.replace(token, "*" * 12 + token[-4:])  # SL 7
            content = content.replace(token, " ")

    # ---------- 2. Clean the text ----------
    cleaned = content.strip().lower()
    cleaned = cleaned.replace("'", "")        # don't -> dont
    for symbol in PUNCTUATION:
        cleaned = cleaned.replace(symbol, " ")
    words = cleaned.split()                   # list of words
    cleaned = " ".join(words)                 # single spaces only

    # ---------- 3. Sentiment ----------
    positive = 0
    negative = 0
    for i in range(len(words)):
        score = 0
        if words[i] in POSITIVE:
            score = 1
        elif words[i] in NEGATIVE:
            score = -1
        else:
            continue
        before = words[i - 1:i]   # SLICE 8: the word before (if any)
        if len(before) == 1 and before[0] in NEGATIONS:
            score = -score        # "not good" becomes negative
        if score == 1:
            positive += 1
        else:
            negative += 1

    total = positive + negative
    if positive > negative:
        mood = "Positive"
        confidence = round(positive * 100 / total)
    elif negative > positive:
        mood = "Negative"
        confidence = round(negative * 100 / total)
    else:
        mood = "Neutral"
        confidence = 100 if total == 0 else 50

    # ---------- 4. Keyword frequency ----------
    counts = {}
    for word in words:
        if len(word) > 2 and word not in STOP_WORDS:
            counts[word] = counts.get(word, 0) + 1

    pairs = []
    for word in counts:
        pairs.append((counts[word], word))
    pairs.sort(reverse=True)
    top_five = pairs[:5]          # SLICE 9: first five only

    # ---------- 5. Spam check ----------
    reasons = []

    letters = 0
    capitals = 0
    for ch in text:
        if ch.isalpha():
            letters += 1
        if ch.isupper():
            capitals += 1
    if letters >= 10 and capitals > letters / 2:
        reasons.append("many capital letters")

    for k in range(len(text) - 3):
        chunk = text[k:k + 4]     # SLICE 10: four characters
        if chunk[0] == chunk[1] == chunk[2] == chunk[3]:
            if chunk[0].isalpha() or chunk[0] == "!":
                reasons.append("repeated characters")
                break

    for word in words:
        if word in SUSPICIOUS or word == "http":
            reasons.append("suspicious word '" + word + "'")
            break

    if len(reasons) >= 2:
        spam = "Spam"
    elif len(reasons) == 1:
        spam = "Suspicious"
    else:
        spam = "Clean"

    # ---------- Report ----------
    print("\n" + "-" * 60)
    print("Original :", text)
    print("Cleaned  :", cleaned)
    print("Sentiment:", mood, "-", str(confidence) + "% confidence")
    print("Top keywords:")
    for count, word in top_five:
        print("  " + word.ljust(14) + "| " + "#" * count + " " + str(count))
    print("E-mails  :", emails)
    print("Phones   :", phones)
    print("Cards    :", len(cards), "found")
    print("Spam     :", spam, reasons)
    print("STORED   :", masked)

    if expected != "":
        tested += 1
        if mood == expected:
            passed += 1
            print("Test     : PASS")
        else:
            print("Test     : FAIL (expected", expected + ")")

if tested > 0:
    print("\nTests passed:", passed, "of", tested)
