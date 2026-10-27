# Setting Up the Lab

By the end of this chapter you have
the lab folder on your machine, you
know what every file in it is for,
and you have run the first tool and
seen it work.

## What you need

Python 3 and nothing else. The lab
uses only the Python **standard
library** — the modules that ship
with Python — so there is nothing to
install and no environment to manage.
Check your version:

```bash
python3 --version
```

The lab was built and run on Python
**3.12.3**; any recent Python 3 will
do. The transcript is
`rag-lab/transcripts/t00-versions.txt`.

## The layout

```text
rag-lab/
  ragcore.py             chunking and scoring, shared
  chunk.py               show the chunks
  build_index.py         build the store, rag.db
  search.py              retrieval only, ranked chunks
  ask.py                 the whole pipeline, end to end
  docs/                  the documents being asked about
    bramble-mk2-manual.txt
    harbourlight-newsletter.txt
    millpond-regatta-rules.txt
  workshop-notice-june.txt   a fourth document, added in chapter 10
  transcripts/           the recorded runs this guide quotes
```

Four small programs face outward,
one per stage of the pipeline, all of
them reading the same shared core.
That shape is deliberate: when a
stage misbehaves you can run just
that stage and look at what it does,
which is how the chapters proceed.

## The documents

The questions in this guide are asked
about three invented documents:

- A **workshop manual** for the
  Bramble Mk II bench polisher — an
  invented machine, specified in
  enough detail (belt tensions, oil
  grades, part numbers) that questions
  about it have exactly one right
  answer each.
- A **club newsletter** for the
  Harbourlight Model Boat Club —
  meetings, dues, and the date of the
  spring regatta.
- The **regatta rules** — classes,
  safety, and when the prizes are
  presented.

Invented documents are a deliberate
choice, not a shortage. Their facts
are known completely, so a wrong
answer is provably wrong; and nothing
in the lab is modelled on any real
club, machine, or person. When you
build your own version, your real
documents take this folder's place —
chapter 13 has the recipes.

## A first run

From inside `rag-lab/`:

```bash
python3 chunk.py
```

This reads every document in `docs/`,
splits it into chunks (chapter 4
explains the rules), and prints them.
The last line is the smoke test:

```text
Total: 26 chunks
```

Check: your run ends with that total,
and the per-document counts above it
read 12, 8, and 6. The full recorded
run is
`rag-lab/transcripts/t01-chunking.txt`.
Twenty-six chunks is the entire
world, for this lab: everything the
system can ever answer about is in
those twenty-six pieces of text.
