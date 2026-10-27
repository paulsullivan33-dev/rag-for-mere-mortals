# Embeddings and Similarity

By the end of this chapter you can say
what an embedding is, how two texts
are compared once they are numbers,
and work the lab's stand-in version by
hand for one real word.

## Meaning as a list of numbers

An **embedding** is a piece of text
turned into a list of numbers — its
**vector** — by a model trained so
that texts with similar meanings get
similar lists. One widely used shape
of it: a vector of several hundred
numbers, none of them meaningful
alone, together forming a position in
a space where *near* means *about
the same thing*. "The belt should
move 8 to 10 mm" and "check the drive
belt tension" share almost no words,
but a good embedding model has read
enough text to place them close
together anyway. That is the trick
the whole field rests on: similarity
of meaning, made arithmetic.

Two vectors are compared by **cosine
similarity**: the cosine of the angle
between them. Pointing the same way
scores 1. Unrelated scores near 0.
The score is a ranking device, not a
probability — 0.61 does not mean 61%
likely correct; it means *closer
than the chunk that scored 0.09*.
Chapter 7's outputs are exactly
these scores.

## The lab's stand-in: TF-IDF

The lab cannot train or download an
embedding model, and does not pretend
to. In the embedding slot it uses
**TF-IDF**, a method from the 1970s
that you can verify with a pocket
calculator:

- **Term frequency (tf):** how many
  times a word appears in the chunk.
- **Document frequency (df):** in how
  many chunks the word appears at
  all.
- **Inverse document frequency
  (idf):** a rarity score,
  `ln((1 + N) / (1 + df)) + 1` for
  `N` chunks. A word in every chunk
  (like *machine* nearly is, here)
  scores near 1: it tells you little.
  A word in two chunks scores high:
  it is a fingerprint.
- A chunk's vector is its words'
  counts multiplied by their idf.

Worked from the lab's real index
(`rag-lab/transcripts/t02-build-index.txt`):
the set has 26 chunks. The word
*belt* appears in 2 of them, so its
idf is ln(27/3) + 1 ≈ **3.20**. In
the belt chunk, `bramble-mk2-manual#5`,
*belt* appears 5 times, giving a
stored weight of 5 × 3.20 = **15.99**.
In `bramble-mk2-manual#2` it appears
once: weight **3.20**. Both numbers
are rows in the store, and chapter 6
shows the query that reads them back.

Before scoring, the lab strips out a
short list of **stopwords** — *the,
of, should, what* and their kin —
words so common they carry no topic.
The list is in `ragcore.py`, short
and boring on purpose.

## What the stand-in cannot do

TF-IDF matches **shared words**,
weighted by rarity. It cannot match
meaning across different words:

- Ask about "belts" (plural) where
  the text says "belt", and that word
  contributes nothing; the lab has no
  stemming, no notion that the two
  are kin. (Chapter 10's question
  survives on its other words.)
- Ask "how do I stop the bench
  shaking?" and the troubleshooting
  chunk, which says *vibrates*, is a
  stranger to it.

A neural embedding handles both,
because it learned word *meanings*
from reading at scale. It also cannot
be checked with a pocket calculator,
its numbers explain nothing by
themselves, and when it misranks you
cannot open it up and see why. The
lab chose inspectability. The slot is
the same shape either way — a vector
per chunk, cosine to compare — and
everything after this chapter is
identical for both. That is the
honest trade, stated once, here.
