# Glossary

**Chunk** — one retrievable piece of
a document, cut by the chunking rules
and identified by an id such as
`bramble-mk2-manual#5` (chapter 4).

**Citation** — the chunk id an answer
attaches to a fact, naming the source
it claims to come from; the promise a
reader can check (chapters 8 and 11).

**Context window** — the maximum
amount of text a model can consider
in one request; the hard reason
documents are chunked and retrieved
rather than pasted whole (chapters 4
and 14).

**Cosine similarity** — the standard
comparison of two vectors: the cosine
of the angle between them, 1 for
identical direction, near 0 for
unrelated (chapter 5).

**Document frequency (df)** — the
number of chunks a word appears in;
the raw count behind idf (chapter 5).

**Embedding** — a text turned into a
list of numbers (a vector) so that
similar meanings land near each other
(chapter 5).

**Evaluation** — checking a system's
answers against a fixed set of
questions with known expected
outcomes (chapter 11).

**Grounded prompt** — the request
handed to the model: instructions to
answer only from the included
sources, the retrieved chunks with
their ids, and the question
(chapter 8).

**Hallucination** — a model stating
something false with complete
confidence, because it has no way to
know what it does not know
(chapter 1).

**Index** — see *store*.

**Inverse document frequency (idf)**
— a word's rarity weight,
`ln((1 + N) / (1 + df)) + 1` over `N`
chunks; rare words score high because
they identify a topic (chapter 5).

**Overlap** — words shared between
neighbouring chunks when a long block
is windowed, so a fact near a cut
survives whole in one chunk
(chapter 4).

**Retrieval** — ranking the chunks
against a question and carrying the
best few into the prompt (chapter 7).

**Stand-in** — this guide's
mechanical replacement for a language
model: it quotes the best-covering
retrieved sentence or refuses, and
cannot invent (chapter 9).

**Stopwords** — very common words
(*the, of, should*) removed before
scoring because they carry no topic
(chapter 5).

**Store** — the index file (here, one
SQLite database) holding the chunks
and their weights, ready to search
(chapter 6).

**TF-IDF** — term frequency × inverse
document frequency: the lab's
inspectable stand-in for a neural
embedding, scoring words by count and
rarity (chapter 5).

**Threshold** — the minimum score a
chunk must reach to be carried into
the prompt at all (chapter 7).

**Top-k** — how many of the
best-scoring chunks retrieval carries
forward (chapter 7).

**Vector** — a list of numbers
representing a text or a word's
weights; the thing cosine similarity
compares (chapter 5).
