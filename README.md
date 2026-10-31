# Customer Feedback Analyzer (Sentiment and Data Masking)

## Overview

A robust text-processing pipeline designed for customer-care and support operations. It cleans raw customer messages, extracts and masks sensitive personally identifiable information (PII) such as emails, phone numbers, and credit card numbers without regular expressions, performs lexicon-based sentiment analysis with negation handling, visualizes top keyword frequencies using ASCII text bars, and screens for spam.

---

## Real-World Scenario

Customer-care centers receive thousands of product reviews, feedback entries, and support tickets daily. To maintain operational efficiency, preserve data privacy compliance (e.g., GDPR, PCI-DSS), and gauge customer satisfaction, organizations require automated tools that:
1. **Clean raw text** and standardize inputs.
2. **Protect customer privacy** by masking sensitive details (payment cards, contact numbers, email identities) before persistence.
3. **Gauge customer mood** (Positive, Negative, or Neutral) and quantify confidence.
4. **Identify trending topics** and top keywords.
5. **Filter spam** and malicious or promotional communications.

---

## Syllabus & Concepts Covered

- **Strings & Slicing**: Substring extraction, step-less slicing, negative indexing, boundaries, and safe slicing.
- **String Methods**: `.strip()`, `.lower()`, `.replace()`, `.split()`, `.find()`, `.rfind()`, `.isdigit()`, `.isalpha()`, `.isupper()`, `.ljust()`.
- **Control Flow & Conditional Statements**: Multi-way branching (`if`-`elif`-`else`), compound boolean expressions.
- **Looping Constructs**: `for` loops, `while` input validation loops, range iterations, sliding window techniques.
- **Data Structures**: Lists, tuples, sets (for $O(1)$ lookups of sentiment and stop words), and dictionaries (frequency counting).
- **PEP 8 Compliance**: Clean naming conventions, docstrings, modular formatting, and type safety principles.

---

## Key Features

### 1. Data Masking & PII Extraction (Without Regex)
- **Email Detection & Masking**: Identifies valid email addresses by parsing usernames, domains, and top-level domain (TLD) extensions using `.find()`, `.rfind()`, and string slices. Retains the first letter of the name and masks the remainder with `*` (e.g., `riya.sharma@example.com` $\rightarrow$ `r**********@example.com`).
- **Phone Number Masking**: Identifies 10-digit phone numbers and masks all but the last 4 digits (e.g., `9876543210` $\rightarrow$ `******3210`).
- **Credit Card Masking**: Identifies 16-digit card numbers and replaces the first 12 digits with asterisks (e.g., `4111111111111234` $\rightarrow$ `************1234`).
- **Sanitized Content Extraction**: Strips extracted secrets from the analytical text so numbers and email strings do not skew keyword counts or sentiment scores.

### 2. Text Cleaning & Normalization
- Strips leading and trailing whitespace.
- Normalizes text to lower-case.
- Normalizes contractions by removing apostrophes (e.g., `don't` $\rightarrow$ `dont`, `wasn't` $\rightarrow$ `wasnt`).
- Strips punctuation symbols and collapses multiple whitespace characters into single spaces.

### 3. Sentiment Scoring with Negation
- Uses dedicated sets for `POSITIVE` and `NEGATIVE` words for $O(1)$ lookup performance.
- Evaluates negation words (`not`, `no`, `never`, `dont`, `isnt`, `wasnt`, `didnt`) directly preceding a sentiment word via safe look-behind slicing (`words[i-1:i]`).
  - Converts `"not good"` from positive (+1) to negative (-1).
  - Converts `"not bad"` from negative (-1) to positive (+1).
- Classifies mood as **Positive**, **Negative**, or **Neutral**.
- Calculates confidence score percentage: $\text{Confidence} = \text{round}\left(\frac{\text{dominant\_score}}{\text{total\_sentiment\_words}} \times 100\right)\%$.

### 4. Keyword Frequency Dictionary & Visual Text Bar
- Tallies occurrence of all words with length $> 2$, filtering out common `STOP_WORDS`.
- Stores frequencies in a dictionary: `counts[word] = counts.get(word, 0) + 1`.
- Sorts and extracts the **Top 5** keywords.
- Displays an ASCII frequency bar (e.g., `recommend | # 1`).

### 5. Multi-Rule Spam Filter
Evaluates messages across three independent heuristic rules:
1. **Excessive Capitalization**: Flags messages where length $\ge 10$ and $> 50\%$ of letters are uppercase.
2. **Repeated Characters**: Uses a sliding 4-character window to detect 4 identical consecutive characters (e.g., `!!!!!` or `Soooooo`).
3. **Suspicious Keywords & Links**: Identifies promotional or phishing terms (`winner`, `prize`, `lottery`, `click`, `claim`, `urgent`, `http`).
- **Classification**:
  - **Spam**: 2 or more rules triggered.
  - **Suspicious**: 1 rule triggered.
  - **Clean**: 0 rules triggered.

---

## 10 Slicing Operations Reference

As per the technical requirements, the project utilizes at least 10 explicit slicing operations:

| # | Code Slice | Context / Description |
|---|------------|-----------------------|
| **1** | `name = token[:at]` | Extracts email username before `@` |
| **2** | `domain = token[at + 1:]` | Extracts email domain after `@` |
| **3** | `ending = domain[domain.rfind(".") + 1:]` | Extracts the top-level domain (TLD) extension |
| **4** | `hidden = name[:1] + "*" * (len(name) - 1)` | Retains only the first character of the email username |
| **5** | `token[at:]` | Preserves `@` and domain while appending to masked username |
| **6** | `"******" + token[-4:]` | Extracts the last 4 digits of a 10-digit phone number |
| **7** | `"*" * 12 + token[-4:]` | Extracts the last 4 digits of a 16-digit credit card number |
| **8** | `before = words[i - 1:i]` | Safe 1-word look-behind for negation (avoids index errors when `i = 0`) |
| **9** | `top_five = pairs[:5]` | Extracts the top 5 sorted keyword tuples |
| **10** | `chunk = text[k:k + 4]` | 4-character sliding window for repeated character spam detection |

---

## Assessment Criteria Mapping (5 Marks)

| Assessment Item | Marks | Implementation Details |
|-----------------|:-----:|------------------------|
| **1. Text cleaning and word splitting** | 1 | Whitespace normalization, `.lower()`, apostrophe stripping, punctuation removal, single-spaced tokenization. |
| **2. Sentiment scoring with negation** | 1 | Set-based lookup (`POSITIVE`, `NEGATIVE`), look-behind negation reversal (`NEGATIONS`), confidence calculation. |
| **3. Keyword frequency (dictionary)** | 1 | Dictionary frequency counting, `STOP_WORDS` filtering, length check ($> 2$), ASCII bar visualization. |
| **4. Extraction and masking using slicing** | 1 | Extraction and masking of email addresses, 10-digit phone numbers, and 16-digit card numbers with explicit slicing operations (no regex). |
| **5. Spam rules, tests and PEP 8** | 1 | 3-factor spam detection, 15 comprehensive automated test cases (100% pass rate), PEP 8 formatting, complete docstrings. |
| **Total** | **5 / 5** | |

---

## Test Suite (15 Test Cases)

The application includes 15 built-in test cases covering diverse real-world customer interactions:

| # | Sample Message Type | Tested Capability | Expected Mood |
|:-:|---------------------|-------------------|:-------------:|
| 1 | Standard positive feedback | Multi-keyword positive sentiment | Positive |
| 2 | Damaged item complaint | Negative keywords (`broken`, `rude`, `refund`) | Negative |
| 3 | Direct negation (`not good`) | Negation flip handling | Negative |
| 4 | Neutral delivery update | Neutral mood with 100% confidence | Neutral |
| 5 | Contact info with phone & email | Masking email & 10-digit phone | Negative |
| 6 | Payment failure with credit card | 16-digit card number masking | Negative |
| 7 | Negated negative (`not bad`) | Negation flip handling to positive | Positive |
| 8 | Spam lottery message | Capitalization, repeated chars, links | Neutral (Spam) |
| 9 | Elongated praise (`Soooooo happy`) | Positive sentiment + repeated char alert | Positive (Suspicious) |
| 10 | Negated support (`not helpful`) | Compound negative sentences | Negative |
| 11 | Mixed sentiment review | Balanced positive/negative (50% confidence) | Neutral |
| 12 | Combined contact details | Masking both email and phone simultaneously | Positive |
| 13 | Multiple contractions (`don't`, `isn't`) | Contraction cleaning & negation chaining | Negative |
| 14 | Successful payment confirmation | Card masking with positive review | Positive |
| 15 | Repeated punctuation alert (`!!!!!`) | Card/phone extraction + punctuation spam check | Negative (Suspicious) |

---

## How to Run

### Prerequisites
- Python 3.10 or higher.
- Standard Python libraries only (no third-party dependencies required).

### Execution

```bash
python CUSTOMER_FEEDBACK_ANALYSIS.py
```

### Usage
- **Run Built-in Test Suite**: Press <kbd>Enter</kbd> at the prompt to run all 15 automated validation test cases.
- **Analyze Custom Message**: Enter any text up to 500 characters and press <kbd>Enter</kbd>.

---

## Sample Output

```text
Type a message (or press Enter for the 15 samples): 

------------------------------------------------------------
Original : Please call me on 9876543210 about my order, the delivery was late.My email is riya.sharma@example.com
Cleaned  : please call me on about my order the delivery was late my email is
Sentiment: Negative - 100% confidence
Top keywords:
  please        | # 1
  order         | # 1
  late          | # 1
  email         | # 1
  delivery      | # 1
E-mails  : ['riya.sharma@example.com']
Phones   : ['9876543210']
Cards    : 0 found
Spam     : Clean []
STORED   : Please call me on ******3210 about my order, the delivery was late.My email is r**********@example.com
Test     : PASS

------------------------------------------------------------
Original : CLICK HERE NOW!!!! You are a WINNER. CLAIM YOUR PRIZE at http://win-big.example
Cleaned  : click here now you are a winner claim your prize at http win big example
Sentiment: Neutral - 100% confidence
Top keywords:
  winner        | # 1
  win           | # 1
  prize         | # 1
  http          | # 1
  here          | # 1
E-mails  : []
Phones   : []
Cards    : 0 found
Spam     : Spam ['many capital letters', 'repeated characters', "suspicious word 'click'"]
STORED   : CLICK HERE NOW!!!! You are a WINNER. CLAIM YOUR PRIZE at http://win-big.example
Test     : PASS

============================================================
Tests passed: 15 of 15
```

---

## File Structure

```text
python_project/
├── CUSTOMER_FEEDBACK_ANALYSIS.py  # Main script with analysis logic and test suite
└── README.md                      # Project documentation and rubric mapping
```

