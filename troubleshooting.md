# Troubleshooting

By the end of this chapter you can
take the four ways this system
usually misbehaves and work each one
in order, from the cheapest cause to
the dearest.

## "The documents do not say" — but they do

The refusal is honest and wrong: the
fact is in the set, the answer never
surfaced. Work it in this order:

1. **Stale index.** Did the document
   change after the last build?
   Rebuild (chapter 10) and ask
   again. This is the commonest cause
   and the cheapest check.
2. **Retrieval missed.** Run
   `search.py` with the question. If
   the right chunk is absent from the
   ranking, the question's words and
   the document's words have parted
   company — ask again using the
   document's own nouns (chapter 13's
   pattern), and check where the
   chunk ranked.
3. **The fact is sawn in half.** Read
   the chunk itself
   (`sqlite3 rag.db "SELECT text FROM chunks WHERE id = '...';"`).
   If the answer straddles a chunk
   boundary, the chunking is the bug:
   adjust the block, or accept that
   this fact needs a hand-made chunk.
4. **Coverage, not retrieval.** If
   `search.py` ranks the right chunk
   first but `ask.py` still refuses,
   the stand-in's answerer found no
   single sentence covering enough of
   the question — the answer is spread
   across sentences, which is exactly
   the case a real model handles and
   the stand-in, by design, does not.
   Note it as a known stand-in limit
   (chapter 9), not a pipeline fault.

## The answer cites the wrong chunk

Open the cited chunk and read it. If
the claim is not there, the answer is
**unsupported** (chapter 11) and does
not ship. Usual causes: two chunks
share the question's rare words (a
heading glued to the wrong block can
do this), or a real model decorating
an answer with a plausible citation.
Tighten top-k, and re-run the test
set before trusting the change.

## Everything refuses

- `rag.db` missing or built from the
  wrong folder: every score is
  nothing because there is nothing to
  score. Rebuild from inside
  `rag-lab/` and confirm the build
  prints your documents' names.
- An empty `docs/` after a tidy-up:
  the build succeeds on zero
  documents and the system then
  honestly refuses everything. The
  build output's chunk count is the
  tell — check it is not zero.

## The answer is the old version of a fact

The index is a snapshot and you are
reading the photograph, not the
scene. Rebuild (chapter 10). If it
keeps happening, the set changes
faster than your habit: schedule the
rebuild (chapter 13) or reconsider
whether this data suits RAG at all
(chapter 12).

## A real model invents despite the prompt

Documented behaviour of real models,
not run in this lab (chapter 9 says
why): the prompt's instructions are
requests, and models under pressure
to be helpful sometimes comply with
the question instead. The working
countermeasures are smaller source
sets (lower top-k, so there is less
to stray from), a lower temperature
if the server exposes one, and —
above all — the chapter 11 test set
run after every change, with the
near-miss question watched by name.
A model that fails the near miss
does not get deployed on the strength
of the seven it passed.
