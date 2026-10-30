"""Customer Feedback Analyzer (Sentiment and Data Masking).

Steps for every message:
  1. Find e-mails, phone numbers and card numbers, then mask them
  2. Clean the text and split it into words
  3. Score the sentiment (with negation like "not good")
  4. Count keywords and show the top five
  5. Check for spam

# ---------------------------------------------------------------
# Word lists (sets)
# ---------------------------------------------------------------
POSITIVE = {"good", "great", "excellent", "amazing", "love", "like",
            "happy", "fast", "quick", "helpful", "perfect", "smooth",
            "recommend", "nice", "best", "friendly", "comfortable"}
NEGATIVE = {"bad", "poor", "terrible", "awful", "worst", "slow",
            "broken", "disappointed", "late", "rude", "useless",
            "horrible", "damaged", "problem", "crashing", "flimsy",
            "refund", "failed", "hate"}
NEGATIONS = {"not", "no", "never", "dont", "didnt", "doesnt", "isnt",
             "wasnt", "cant", "wont"}
STOP_WORDS = {"the", "and", "was", "for", "this", "that", "with", "but",
              "very", "are", "you", "your", "can", "will", "from",
              "not", "all", "our", "been", "too", "its", "here", "now"}
SUSPICIOUS = {"winner", "prize", "lottery", "click", "claim", "bitcoin",
              "giveaway", "urgent", "password", "otp"}

PUNCTUATION = "!\"#$%&()*+,-./:;<=>?@[\\]^_`{|}~"

# ---------------------------------------------------------------
# 15 sample messages: tuples of (message, expected sentiment)
# ---------------------------------------------------------------
SAMPLES = [
    ("I absolutely love this phone! The battery is great and delivery "
     "was fast. Highly recommend.", "Positive"),
    ("Terrible experience. The screen arrived broken and support was "
     "rude. I want a refund.", "Negative"),
    ("The product is not good. It stopped working after two days.",
     "Negative"),
    ("Package arrived on Tuesday. Box was medium sized.", "Neutral"),
    ("Please call me on 9876543210 about my order, the delivery was "
     "late. My email is riya.sharma@example.com", "Negative"),
    ("I paid with card 4111111111111234 but the payment failed twice. "
     "Very disappointed, please refund.", "Negative"),
    ("Great value, not bad at all, the sound is excellent!", "Positive"),
    ("CLICK HERE NOW!!!! You are a WINNER. CLAIM YOUR PRIZE at "
     "http://win-big.example", "Neutral"),
    ("Soooooo happy with the service!!! Support was helpful and "
     "friendly.", "Positive"),
    ("The app is slow and keeps crashing. Not helpful support either, "
     "never solved my problem.", "Negative"),
    ("Okay product. Some features are good but the battery is bad.",
     "Neutral"),
    ("Contact me at amit_k99@shop-mail.example or 9123456780 for the "
     "invoice. Thanks, great service.", "Positive"),
    ("I don't like the colour, it isn't comfortable and the strap is "
     "flimsy. Wasn't happy.", "Negative"),
    ("Card 5500000000000004 was charged once. Smooth checkout and "
     "quick delivery!", "Positive"),
    ("Customer care is useless!!!!! Worst service ever, call me on "
     "9012345678", "Negative"),
]

# ---------------------------------------------------------------
# Menu with input validation
# ---------------------------------------------------------------
to_check = []   # list of (message, expected) tuples

print("=== Customer Feedback Analyzer ===")
while True:
    print("\n1) Analyse my own message")
    print("2) Run the 15 sample messages (with tests)")
    print("3) Quit")
    choice = input("Choose 1, 2 or 3: ").strip()

    if choice == "1":
        while True:
            typed = input("Type or paste a message: ")
            if typed.strip() == "":
                print("Message is empty. Try again.")
            elif len(typed) > 500:
                print("Message is too long (max 500 characters).")
            else:
                break
        to_check.append((typed, ""))
        break
    elif choice == "2":
        to_check = SAMPLES
        break
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please enter 1, 2 or 3.")

# Dictionary to count the results
tally = {"Positive": 0, "Neutral": 0, "Negative": 0}
spam_count = 0
tests_passed = 0
tests_run = 0
number = 0

# ---------------------------------------------------------------
# Analyse each message
# ---------------------------------------------------------------
for message, expected in to_check:
    number += 1
    text = message.strip()

    # ===========================================================
    # Step 1: extract and mask e-mails, phones and cards
    # ===========================================================
    emails = []
    phones = []
    cards = []
    masked = text    # safe copy that will be stored
    content = text   # copy with secrets removed, used for analysis

    for token in text.split():
        token = token.strip(".,!?;:")   # remove sentence punctuation

        if "@" in token:
            at = token.find("@")
            name = token[:at]                          # SLICE 1
            domain = token[at + 1:]                    # SLICE 2
            ending = domain[domain.rfind(".") + 1:]    # SLICE 3
            if (name != "" and domain.find(".") > 0
                    and len(ending) >= 2 and ending.isalpha()):
                emails.append(token)
                # hide the middle of the name: first + stars + last
                if len(name) > 2:
                    hidden = name[0] + "*" * len(name[1:-1]) + name[-1]
                else:                                   # SLICE 4
                    hidden = name[0] + "*" * (len(name) - 1)
                masked = masked.replace(token, hidden + token[at:])
                content = content.replace(token, " ")   # SLICE 5

        elif token.isdigit() and len(token) == 10:
            phones.append(token)
            # show only the last four digits
            masked = masked.replace(token, "******" + token[-4:])
            content = content.replace(token, " ")       # SLICE 6

        elif token.isdigit() and len(token) == 16:
            cards.append(token)
            # show only the last four digits: ************1234
            masked = masked.replace(token, "*" * 12 + token[-4:])
            content = content.replace(token, " ")       # SLICE 7

    # ===========================================================
    # Step 2: clean the text
    # ===========================================================
    cleaned = content.strip().lower()
    cleaned = cleaned.replace("'", "")        # don't -> dont
    for symbol in PUNCTUATION:
        cleaned = cleaned.replace(symbol, " ")
    words = cleaned.split()                   # list of words
    cleaned = " ".join(words)                 # single spaces only

    # ===========================================================
    # Step 3: sentiment score with negation
    # ===========================================================
    positive = 0
    negative = 0
    for index in range(len(words)):
        word = words[index]
        if word in POSITIVE:
            score = 1
        elif word in NEGATIVE:
            score = -1
        else:
            continue

        # SLICE 8: the word just before (empty list for the first word)
        previous = words[index - 1:index]
        if len(previous) == 1 and previous[0] in NEGATIONS:
            score = -score        # "not good" counts as negative

        if score == 1:
            positive += 1
        else:
            negative += 1

    total = positive + negative
    if total == 0:
        mood = "Neutral"
        confidence = 100.0
    elif positive == negative:
        mood = "Neutral"
        confidence = 50.0
    elif positive > negative:
        mood = "Positive"
        confidence = round(positive / total * 100, 1)
    else:
        mood = "Negative"
        confidence = round(negative / total * 100, 1)
    tally[mood] += 1

    # ===========================================================
    # Step 4: keyword frequency
    # ===========================================================
    counts = {}    # dictionary: word -> how many times
    for word in words:
        if len(word) < 3 or word in STOP_WORDS:
            continue
        counts[word] = counts.get(word, 0) + 1

    pairs = []
    for word in counts:
        pairs.append((counts[word], word))
    pairs.sort(reverse=True)    # biggest count first
    top_five = pairs[:5]        # SLICE 9: keep only the first five

    # ===========================================================
    # Step 5: spam check
    # ===========================================================
    spam_points = 0
    reasons = []

    # Rule 1: many capital letters
    letters = 0
    capitals = 0
    for ch in text:
        if ch.isalpha():
            letters += 1
            if ch.isupper():
                capitals += 1
    if letters >= 10 and capitals / letters > 0.5:
        reasons.append("many capital letters")
        spam_points += 1

    # Rule 2: same character four times in a row (sooooo, !!!!)
    for k in range(len(text) - 3):
        chunk = text[k:k + 4]       # SLICE 10: four characters
        if (chunk[0] == chunk[1] == chunk[2] == chunk[3]
                and (chunk[0].isalpha() or chunk[0] in "!?$")):
            reasons.append("repeated characters")
            spam_points += 1
            break

    # Rule 3: suspicious words or web links
    hits = []
    for word in words:
        if word in SUSPICIOUS:
            hits.append(word)
    if "http" in text.lower() or "www." in text.lower():
        hits.append("link")
    if len(hits) > 0:
        reasons.append("suspicious words: " + ", ".join(hits))
        spam_points += 1
        if len(hits) >= 2:
            spam_points += 1

    if spam_points >= 2:
        spam_level = "Spam"
        spam_count += 1
    elif spam_points == 1:
        spam_level = "Suspicious"
    else:
        spam_level = "Clean"

    # ===========================================================
    # Show the report
    # ===========================================================
    print("\n" + "-" * 60)
    print("Message", number)
    print("Original :", text)
    print("Cleaned  :", cleaned)
    print("Sentiment:", mood, "(" + str(confidence) + "% confidence)")
    print("Top keywords:")
    for count, word in top_five:
        print("  " + word.ljust(14) + "| " + "#" * count + " " + str(count))
    print("E-mails  :", emails)
    print("Phones   :", phones)
    print("Cards    :", len(cards), "found")
    if len(reasons) > 0:
        print("Spam     :", spam_level, "-", "; ".join(reasons))
    else:
        print("Spam     :", spam_level)
    print("STORED   :", masked)

    # Test result (only for the sample messages)
    if expected != "":
        tests_run += 1
        if mood == expected:
            tests_passed += 1
            print("Test     : PASS (expected", expected + ")")
        else:
            print("Test     : FAIL (expected", expected, "but got",
                  mood + ")")

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------
if len(to_check) > 1:
    print("\n" + "=" * 60)
    print("SUMMARY of", len(to_check), "messages")
    for label in tally:
        print(" ", label.ljust(9), "|", tally[label])
    print("  Spam      |", spam_count)
    print("Tests passed:", tests_passed, "of", tests_run)
