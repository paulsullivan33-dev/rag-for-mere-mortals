# RAG for Mere Mortals

Ask a language model a question about
your own documents — a manual, a pile
of meeting minutes, a club's records —
and it will answer fluently whether or
not it has ever seen them, because
fluent answers are what it makes. **RAG
— retrieval-augmented generation** —
changes the arrangement: first a
**retriever** finds the passages in
your documents that bear on the
question, then the model writes its
answer from those passages, in front of
you, with its sources named. The model
stops being an oracle and becomes a
student in an open-book exam.

This guide builds that arrangement for
real, in plain Python with nothing to
install: documents cut into **chunks**,
chunks turned into numbers and kept in
a small searchable **store**, questions
matched against the store, and the best
chunks assembled with the question into
a **grounded prompt**. It covers the
whole craft around the pipeline too —
chunk sizes, freshness, how to test
whether answers are honest, and when
RAG is simply the wrong tool.

The rule that governs everything here
is stated in chapter 1 and enforced
throughout: **an answer built from
retrieved text must cite the chunk each
fact came from, and when the documents
hold no answer, "the documents do not
say" is a correct answer — the correct
one.** A system that cannot say that
sentence is a storyteller with your
filing cabinet open beside it.

The lab behind this guide ran the real
pipeline: **Python 3.12.3**, standard
library only, against three invented
documents — a model boat club's
newsletter and regatta rules, and the
workshop manual for an invented bench
polisher. Against them it chunked the
set into 26 chunks, built a SQLite
store of their word weights, ranked
chunks for real questions, assembled
grounded prompts, and answered: four
questions answered from the correct
chunk with citations, and two traps —
a machine model that does not exist in
the documents, and a winner nobody
recorded — refused in the set words. A
fourth document was then added and the
index rebuilt, turning a third refusal
into a cited answer, and a fixed set
of nine test questions was scored end
to end.

What the lab could not do, it did not
fake. The final step of a production
RAG system is a language model, and
the build machine had no model server
reachable — the check is recorded in
the lab's transcripts — so the lab's
answering step is a small mechanical
**stand-in** that quotes the retrieved
sentence or refuses, labelled as a
stand-in wherever it appears. It
proves the machinery around the model
and is honest that it cannot prove
the model. Chapter 9 shows the exact,
small swap that puts a real local
model (Ollama) in the stand-in's
place, and marks it documented-only.
`criteria.md` keeps the full ledger of
what was run and what was only read.

## What this guide covers

- [**What RAG is**](what-rag-is.md) —
  the open-book exam, why models
  hallucinate about your documents,
  and the honesty rule everything
  else hangs on
- [**The moving parts**](the-moving-parts.md) —
  documents, chunks, embeddings, the
  store, retrieval, the grounded
  prompt, the model — and which part
  holds what when it breaks
- [**Setting up the lab**](setting-up-the-lab.md) —
  Python and nothing else, the lab's
  layout, and the three invented
  documents you will interrogate
- [**Chunking and why size matters**](chunking.md) —
  blocks, headings, windows and
  overlap, and the three ways a bad
  cut ruins a fact
- [**Embeddings and similarity**](embeddings-and-similarity.md) —
  meaning as numbers, cosine
  similarity, and the TF-IDF stand-in
  worked by hand from the real index
- [**Building the index**](building-the-index.md) —
  one SQLite file, three tables, and
  queries you can run to check the
  guide's own numbers
- [**Retrieval and ranking**](retrieval-and-ranking.md) —
  ranked chunks with scores, top-k and
  the threshold, and retrieval as the
  ceiling of the whole system
- [**Writing the grounded prompt**](the-grounded-prompt.md) —
  the three instructions that matter:
  only the sources, cite everything,
  refuse in exact words
- [**Asking questions end to end**](asking-questions.md) —
  one question with nothing hidden,
  the mechanical stand-in examined,
  the three outcomes, and the
  documented-only swap to a real model
- [**Keeping the index fresh**](keeping-the-index-fresh.md) —
  a refusal turned into an answer by
  a rebuild, and why changed facts
  are harder than new ones
- [**Judging answer quality**](judging-answer-quality.md) —
  a nine-question test set with known
  answers, the three verdicts, and
  questions designed to tempt the
  system into inventing
- [**When RAG is the wrong tool**](when-rag-is-wrong.md) —
  corpora too small to need it,
  questions that need all of it, and
  jobs that are writing, not recall
- [**Recipes**](recipes.md) — a manual
  on the workbench, what-did-we-decide
  over minutes, scheduled rebuilds,
  and questions that retrieve well
- [**The neighbours**](the-neighbours.md) —
  fine-tuning, long context, plain
  search, and hosted upload-a-file
  chatbots: what each does that RAG
  doesn't
- [**Limits**](limits.md) — quiet
  retrieval misses, prompts as
  requests rather than fences,
  grounding without truth, and the
  ageing snapshot
- [**Troubleshooting**](troubleshooting.md) —
  the refusal that should not have
  happened, the citation that does
  not support its claim, and the
  stale index wearing a fresh face
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Training or fine-tuning a model (a
neighbour, chapter 14, with its own
guide in this series), and building
embedding models of your own.
Production vector databases and
million-chunk deployments are
characterised in chapter 15, not
taught: the lab is deliberately a
teaching rig whose every number can
be checked by hand. Hosted
question-answering services are
discussed as a trade in chapter 14,
not configured. And no chapter helps
you present retrieved text as more
certain than it is — the citation
rule points the other way.

## How to use this guide

Read chapter 1 for the model and the
rule, and chapter 2 before building
anything — knowing which part holds
what turns later confusion into a
named problem. Chapters 3 to 9 build
the pipeline one stage at a time,
each stage runnable on its own; do
not skip chapter 8, because the
grounded prompt is where the honesty
rule becomes machinery. Chapter 11's
test set is the part to keep when the
lab is long deleted: grow it from
every bad answer you ever meet. The
lab's code is `rag-lab/`, its
transcripts are
`rag-lab/transcripts/`, and its
distilled commands are
`examples/commands.txt`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Ollama for Mere Mortals](https://paulsullivan33-dev.github.io/ollama-for-mere-mortals/)
- [Open WebUI for Mere Mortals](https://paulsullivan33-dev.github.io/open-webui-for-mere-mortals/)
- [LLM Evaluation for Mere Mortals](https://paulsullivan33-dev.github.io/llm-evaluation-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/rag-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/rag-for-mere-mortals/blob/main/LICENSE-CODE).
