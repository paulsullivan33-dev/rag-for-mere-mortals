# Keeping the Index Fresh

By the end of this chapter you have
watched a question go from refused to
answered purely because the index was
rebuilt, and you can state the rule
that governs every RAG system you
will ever run: **answers can only be
as fresh as the last build.**

## The demonstration

The lab ships a fourth document
outside `docs/`:
`workshop-notice-june.txt`, a notice
saying where the spare drive belts
for the polisher are kept. The index
has never seen it. Ask where they
are (transcript
`rag-lab/transcripts/t05-freshness.txt`):

```bash
python3 ask.py "Where are the spare drive belts kept?"
```

*The documents do not say.* Correct —
for the documents the index holds.
Now admit the notice and rebuild:

```bash
cp workshop-notice-june.txt docs/
python3 build_index.py
```

The build reports 27 chunks (was
26), 447 terms (was 437): the notice
became chunk `workshop-notice-june#1`.
Ask the same question again:

```text
... spare BP-114 drive belts and FP-150 felt pads for the
workshop polisher are kept in the grey cabinet by the
door of the shed.
[from workshop-notice-june#1]
```

Nothing about the question, the
pipeline, or the rules changed. The
only event was a rebuild. Freshness
is not a feature of the retriever or
the model; it is a property of the
snapshot, and snapshots are the
operator's job.

## New facts are easy; changed facts are not

Adding a document adds knowledge the
system lacked. *Changing* a fact is
subtler. Suppose the regatta moves
from 14 June to 21 June and someone
adds a correction notice without
touching the newsletter. Now two
chunks disagree, retrieval may carry
either or both, and the answer
depends on which one the model
believes. The grounded prompt cannot
settle a contradiction between its
own sources.

The disciplines that work are dull
ones:

- **Edit the source, not around it.**
  A corrected newsletter replaces the
  old one, so the set holds one date.
  Correction notices are how archives
  end up lying in two voices.
- **One source of truth per fact.**
  If the date lives in the newsletter,
  the rules sheet should point at the
  newsletter, not repeat the date.
- **Rebuild fully, at this scale.**
  The lab's rebuild takes a fraction
  of a second and replaces the store
  wholesale, so there is no partial
  state to reason about. Large systems
  index incrementally, which is an
  optimisation, not a different
  discipline: the question is still
  *what snapshot is live, and how old
  is it?*

## A freshness habit

Make the rebuild part of the act of
editing: document changed, index
rebuilt, same sitting. Chapter 13
includes a scheduled rebuild for
document sets that change in places
you do not control. And when an
answer surprises you, *stale index*
belongs on the suspect list before
*broken retriever* — chapter 16 puts
it there, in order.
