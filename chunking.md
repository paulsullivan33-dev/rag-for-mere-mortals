# Chunking and Why Size Matters

By the end of this chapter you can
split a document into chunks that
keep facts whole, and you can predict
what goes wrong when chunks are too
big or too small.

## Why chunk at all

Two reasons, one hard and one
practical.

The hard reason: a model reads its
prompt through a **context window** —
a fixed maximum amount of text it can
consider at once. A whole library
does not fit, and even a whole manual
crowds out the question. Retrieval
has to choose *pieces*.

The practical reason: retrieval is a
ranking of pieces. Ask about belt
tension and the system compares your
question against each chunk. If the
belt procedure shares a chunk with
the safety rules and the parts list,
that chunk is about everything and
therefore about nothing in
particular; it ranks weakly for every
question. A chunk earns its ranking
by being about one thing.

## The lab's rules

The lab chunks as plainly as it can
(`ragcore.py`, function
`chunk_document`):

- Split the document into **blocks**
  at blank lines. Most documents are
  already written in blocks —
  paragraphs, sections, items.
- A block of six words or fewer is a
  **heading**, and it is glued onto
  the block that follows it, so its
  words travel with the text they
  name: the manual's belt chunk
  begins `Checking the belt:` and
  continues with the procedure
  itself.
- A block of up to 70 words is one
  chunk.
- A longer block is cut into sliding
  **windows** of 60 words, stepping
  48 words at a time, so neighbouring
  chunks **overlap** by 12 words.

Each chunk gets an **id** made of the
document's name and its position —
`bramble-mk2-manual#5` is the fifth
chunk of the manual. The id is the
chunk's address for the rest of the
guide: the store keeps it, retrieval
returns it, and answers cite it.

## What the numbers look like

Running `python3 chunk.py` (transcript
`rag-lab/transcripts/t01-chunking.txt`)
gives 26 chunks: 12 from the manual,
8 from the newsletter, 6 from the
rules. They run from one line — the
manual's title — to 69 words. The
belt procedure, heading included, is
a single 62-word chunk,
`bramble-mk2-manual#5`, and every
sentence of it is about the belt.
That is what a good chunk looks like.

## Too big, too small, sawn in half

- **Too big.** A 500-word chunk that
  contains the belt procedure among
  nine other facts retrieves for all
  of them and wins for none; and when
  it does reach the prompt it spends
  the context window on text the
  question never asked about.
- **Too small.** Single sentences as
  chunks lose their surroundings.
  "Replace it when it is shorter than
  6 mm" is a fine fact whose chunk no
  longer says what *it* is (a carbon
  brush) or when to look (at 500
  hours).
- **Sawn in half.** The worst cut is
  through the middle of a fact: one
  chunk ends "...check the tension
  every" and the next begins "40
  hours..." Neither retrieves well
  and neither answers whole. This is
  what overlap is for: a fact near a
  cut appears entire in the next
  window over. Overlap costs store
  size and buys insurance.

Real systems chunk with more
sophistication — by heading
structure, by sentence, with token
counters instead of word counters —
but every scheme is negotiating the
same three failures. The lab's rules
are the negotiation at its simplest,
and the chapters ahead show their
consequences in real retrieval
scores.

Check: in the chunk listing, find
`harbourlight-newsletter#5`. It is
the regatta announcement — heading,
date, place, and registration time
in one chunk — because the newsletter
happens to paragraph that way. That
chunk is why the question "When is
the spring regatta?" has a clean
answer in chapter 9.
