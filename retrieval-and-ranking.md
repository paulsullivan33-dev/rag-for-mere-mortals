# Retrieval and Ranking

By the end of this chapter you can run
retrieval on its own, read a ranking,
and judge whether the chunk that
should have won did.

## Retrieval, isolated

`search.py` performs retrieval and
nothing else — no prompt, no answer:

```bash
python3 search.py "belt tension"
```

The question is turned into a vector
with the same weights the index was
built with, every chunk is scored by
cosine similarity, and the best are
printed (transcript
`rag-lab/transcripts/t03-search.txt`):

```text
1. bramble-mk2-manual#5  score 0.611
   Checking the belt: Check the belt tension every 40 hours...
2. bramble-mk2-manual#2  score 0.093
   About this machine: The Bramble Mk II is a bench polisher...
```

The right chunk wins by a wide
margin, because *belt* and *tension*
are rare words concentrated in it.
Ask about the regatta and the ranking
shows retrieval doing discrimination
work across documents:

```text
1. harbourlight-newsletter#5  score 0.499   (the announcement)
2. millpond-regatta-rules#1   score 0.301   (the rules' title)
3. harbourlight-newsletter#1  score 0.257   (the newsletter's title)
4. harbourlight-newsletter#2  score 0.120   (the secretary's letter)
```

The announcement wins; the titles
follow it home on the strength of
the word *regatta* alone.

## Top-k and the threshold

Two dials shape what reaches the
prompt:

- **Top-k** — how many chunks are
  carried forward. The lab takes the
  best **4**. A bigger k catches more
  strays and spends more of the
  context window; a smaller k is
  tidier and more fragile.
- **The threshold** — a floor score,
  in the lab **0.05**, below which a
  chunk is not carried at all, even
  if k is not yet full. It is the
  difference between "the four least
  irrelevant chunks" and "the chunks
  with any real claim to relevance".
  When nothing clears the floor,
  retrieval hands the prompt *no
  sources* — and the honest answer
  becomes possible (chapter 9).

Scores are comparative, not absolute:
0.05 is a lab-sized floor for a
26-chunk world, not a constant of
nature. Big stores retune it against
a test set (chapter 11).

## The ceiling

Retrieval is the ceiling of the whole
system. The model — real or stand-in
— sees only what retrieval carried
into the prompt. If the belt chunk
had ranked fifth, the belt question
would have no good outcome available:
not a wrong answer, note, but a
refusal, which is the system working
as designed. Every RAG failure you
will ever debug reduces to one of
two: the right chunk was not
retrieved, or it was retrieved and
the answer still went wrong. The
first is this chapter's fault. The
second is chapter 11's subject.

Check: run
`python3 search.py "life jacket pontoon"`.
One chunk clears the list —
`millpond-regatta-rules#4` at 0.444 —
because three rare words all live in
the safety paragraph and nowhere
else. Retrieval is at its best when
the question uses the documents' own
vocabulary; chapter 16 is about what
to do when the reader does not know
that vocabulary yet.
