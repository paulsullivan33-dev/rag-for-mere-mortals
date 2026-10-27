# The Moving Parts

By the end of this chapter you can
name every part of a RAG system, say
what each part holds, and — when an
answer goes wrong — say which part to
suspect first.

A RAG system is a pipeline of seven
parts. Data flows one way when you
prepare the documents, and another way
when you ask a question.

| Part | What it holds | Chapter |
|---|---|---|
| Documents | The source texts, exactly as written | 3 |
| Chunks | The documents, cut into retrievable pieces | 4 |
| Embeddings | Each chunk as a list of numbers, its meaning in numeric form | 5 |
| The store | Chunks plus their numbers, kept in a searchable index | 6 |
| Retrieval | The ranking that picks the few chunks a question needs | 7 |
| The grounded prompt | Instructions, the chosen chunks, the question, as one request | 8 |
| The model | The writer, which answers from the prompt | 9 |

## The two journeys

**Preparation** happens once per
version of your documents. Each
document is split into chunks. Each
chunk is turned into an **embedding**
— a list of numbers in which chunks
about similar things get similar
numbers. Chunks and numbers go into
the **store**, which in this guide is
one small SQLite database file.

**Asking** happens per question. The
question is embedded the same way,
the store is searched for the chunks
whose numbers lie closest to the
question's, and the best few are
retrieved. They are pasted into the
grounded prompt with instructions to
answer from them and cite them. The
model reads that prompt and writes.

## Embeddings, and the lab's stand-in

Real embeddings come from a small
neural network trained to place texts
with similar *meaning* near each
other, even when they share no words.
Chapter 5 explains the idea properly.

The lab uses an older, fully
inspectable method in the same slot:
**TF-IDF**, which scores words by how
often they appear in a chunk and how
rare they are across the whole set.
Its vectors can be printed, checked
with a pocket calculator, and stored
in three small tables you can query
by hand. It cannot recognise synonyms
— chapter 5 is plain about that —
but every other part of the pipeline
behaves identically either way:
chunking does not care where the
numbers came from, neither does the
store, the prompt, or the rule about
citations. When your own system swaps
in a real embedding model, only one
part changes.

## Who holds what, when it breaks

- The **documents** hold the truth —
  all of it the system will ever have.
  A fact missing here cannot be
  retrieved, only invented, and the
  rule from chapter 1 exists to make
  sure it is not.
- The **chunks** hold the grain. Too
  big, and retrieval drags in pages of
  near-misses; too small, and a fact
  is sawn in half across two chunks
  and neither half retrieves (chapter
  4).
- The **embeddings** hold the notion
  of *similar*. When the right chunk
  exists but never surfaces, the
  suspicion lands here and on the
  vocabulary of the question (chapter
  7).
- The **store** holds a snapshot.
  Edit a document without rebuilding
  and the system answers from the old
  text, confidently (chapter 10).
- **Retrieval** holds the ceiling.
  The model cannot cite what it never
  saw: if the right chunk is not in
  the prompt, the best possible
  outcome is an honest refusal.
- The **prompt** holds the behaviour.
  Citations happen because the prompt
  demands them in a checkable form
  (chapter 8).
- The **model** holds the pen. Given
  good chunks it can still summarise
  badly or stray; chapter 11 is how
  you catch it.
