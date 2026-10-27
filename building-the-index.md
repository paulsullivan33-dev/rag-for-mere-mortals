# Building the Index

By the end of this chapter you have
built the store — one SQLite database
holding every chunk and every weight
— and you can open it and check its
contents with your own queries.

## The build

From inside `rag-lab/`:

```bash
python3 build_index.py
```

The program chunks every document in
`docs/` (chapter 4's rules), computes
the TF-IDF weights (chapter 5), and
writes them into `rag.db`. The
recorded run
(`rag-lab/transcripts/t02-build-index.txt`)
reports:

```text
Stored 26 chunks
Stored 437 distinct terms
Stored 658 postings (term-in-chunk weights)
Database: rag.db (122880 bytes)
```

The whole knowledge of the system —
three documents, ready to be searched
— is a 120 KB file you can copy,
back up, or delete. Deleting it costs
nothing but a rebuild: the documents
are the truth, and the index is only
ever a snapshot of them (a fact
chapter 10 leans on).

## The three tables

**SQLite** is the database program
built into Python's standard library;
its database is a single file of
tables. The lab uses three:

| Table | One row is | Holds |
|---|---|---|
| `chunks` | a chunk | id, source document, position, vector length (norm), and the text itself |
| `idf` | a word | the word and its rarity weight |
| `postings` | a word in a chunk | the word, the chunk id, and the stored weight (count × idf) |

That is the entire schema. Anything a
big vector database does with more
ceremony, this does with three tables
a reader can dump and read.

## Check it yourself

The `sqlite3` command reads the file
directly:

```bash
sqlite3 rag.db "SELECT COUNT(*) FROM chunks;"
```

gives `26`. And the worked example
from chapter 5, read back from the
store itself:

```bash
sqlite3 rag.db "SELECT term, chunk_id, ROUND(weight, 2) \
  FROM postings WHERE term = 'belt' ORDER BY weight DESC;"
```

```text
belt|bramble-mk2-manual#5|15.99
belt|bramble-mk2-manual#2|3.2
```

The word *belt* lives in exactly two
chunks, weighted exactly as the
formula said. If a number in this
guide ever disagrees with your own
query, your query is right and the
guide is wrong — that is what the
store being inspectable *means*.

## What is not in the store

No answers. No questions. No model.
The store holds text and weights, and
nothing in it can write a sentence.
It also holds no history: rebuilding
replaces it wholesale, which is why
the lab's update procedure (chapter
10) is just "run the build again".
What the store cannot forgive is
being built from stale documents and
then trusted — the snapshot problem,
deferred to chapter 10 where it
belongs.
