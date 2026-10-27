# Judging Answer Quality

By the end of this chapter you have a
small, fixed set of test questions
with known right answers, a way to
score any answer against them, and
the habit that catches made-up
answers before a reader has to.

## Why a test set

A RAG system can be changed in a
dozen places — chunking, threshold,
prompt, model — and every change can
quietly improve one answer and break
another. Impressions will not catch
that. A **test set** will: the same
questions, asked after every change,
scored the same way every time.
Checking a system's answers against
known expectations like this is
**evaluation**, and a small honest
one beats a large vague one.

## The lab's nine questions

The lab's set (transcript
`rag-lab/transcripts/t07-answer-tests.txt`)
was chosen to cover the outcomes of
chapter 9 — seven questions the
documents answer, and two they must
refuse:

| # | Question | Expected |
|---|---|---|
| 1 | What oil should I use for the polisher bearings? | ISO VG 32 sentence, from manual #6 |
| 2 | How often should I check the belt tension? | Every 40 hours, from manual #5 |
| 3 | When is the spring regatta? | Saturday 14 June, from newsletter #5 |
| 4 | How much are the club dues for adults? | 24 dollars, from newsletter #4 |
| 5 | What should I do if the polisher vibrates? | Balanced wheel, tight bolts, from manual #9 |
| 6 | When are the prizes presented? | 4 in the afternoon, from rules #6 |
| 7 | What are the four racing classes? | Sail, steam, electric fast, electric scale, from rules #2 |
| 8 | What is the spindle speed of the Bramble Mk III? | **Refusal** — no Mk III exists in the set |
| 9 | Who won the spring regatta last year? | **Refusal** — no winner is recorded |

Run result, as recorded: **seven
answered with the expected citation,
two refused, zero invented.** The
stand-in's mechanical nature makes a
clean sweep plausible; treat any
future change that breaks a row as a
regression, by definition.

## Scoring an answer

Each answer gets one of three
verdicts:

- **Grounded.** Every fact in the
  answer is in the cited chunk, and
  the citation names that chunk. This
  is a hand check: open the chunk
  (chapter 6 showed how to read the
  store) and find the claim. Thirty
  seconds per answer, no tooling.
- **Unsupported.** The answer states
  something its citation does not
  contain — or cites nothing. This
  is the polite name for a made-up
  answer, and it is the failure the
  whole design exists to expose. A
  citation that does not support its
  claim is worse than no citation:
  it borrows the chunk's authority
  for a claim the chunk never made.
- **Refused.** Scored against the
  expectation, not absolutely: a
  refusal where an answer exists is
  a **miss** (retrieval or coverage
  failed somewhere upstream); a
  refusal where none exists is a
  **correct refusal**, the system
  behaving exactly as chapter 1's
  rule demands.

## Tempting the system on purpose

Questions 8 and 9 are the soul of
the set, and your own sets need
their like:

- **The near miss** (question 8):
  everything about it is retrievable
  except the one thing asked — right
  manual, right topic, wrong model
  of machine. Systems fail here by
  answering for the Mk II and letting
  the reader assume the Mk III. If
  your set has no near miss, it is
  not testing honesty, only recall.
- **The plausible absence**
  (question 9): a winner *must* have
  existed, the documents discuss the
  event at length, and a model that
  likes complete stories will supply
  a name. Absence of a record is the
  fact; the refusal is the correct
  reporting of it.

## Living with the set

Grow it from real use. Every time a
reader reports a bad answer, the
question that produced it joins the
set with its expected verdict, and
the fix is not done until the whole
set passes. When you swap in a real
model (chapter 9), the set becomes
more important, not less: the
stand-in cannot invent, a model can,
and the set is how you find out
whether yours does.
