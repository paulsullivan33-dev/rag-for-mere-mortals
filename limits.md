# Limits

By the end of this chapter you can
name what this machinery cannot do,
including the limits that no amount
of tuning removes. A RAG system
trusted past these lines will
eventually embarrass the trust.

## Retrieval can miss, quietly

The right chunk can exist and still
not surface: the question used
different words than the document
(chapter 5's synonym gap), the
chunking sawn the fact in half, or
the threshold filtered it out. The
system's defence is the refusal —
but a refusal reads the same whether
the fact was absent or merely
unfound. Chapter 16 is the working
list for telling the two apart.

## Prompts are requests, not fences

Everything chapter 8 asks of a model
— use only the sources, cite, refuse
in the set words — is an instruction,
and a real model can disobey
instructions: summarising from its
own knowledge, attaching a citation
to a claim the chunk does not make,
answering the near-miss question for
the wrong machine. The lab's stand-in
cannot do these things, which is
precisely its limitation as evidence:
it proves the pipeline, not a model's
behaviour inside it. The audit
habits of chapter 11 are not optional
decoration on a real deployment; they
are the compensating control for this
limit.

## Grounding is not truth

The citation proves the answer came
from the chunk. It cannot prove the
chunk was right. Documents carry
errors, old editions, and one
person's confident mistake, and RAG
reproduces all of it in a level voice
with a reference attached — arguably
more persuasively than the original.
The defence is editorial, not
technical: a document set worth
asking questions of is worth keeping
correct, and chapter 12 names the
jobs that are really document-repair
jobs.

## The snapshot is always ageing

Between rebuilds, the index is a
photograph of a set that may already
have moved. Everything in chapter 10
mitigates this; nothing removes it.
A system that answers about live
things — stock, schedules, prices —
through a periodic snapshot will
sometimes answer about the past, with
citations.

## Scale is a different country

The lab's design — TF-IDF weights, a
SQLite file, every chunk scored for
every question — is a teaching rig,
honest up to a few thousand chunks.
Real document sets run to millions;
their stores are dedicated vector
databases, their embeddings neural,
their thresholds and chunkers tuned
against large test sets, and their
failures correspondingly harder to
inspect. The concepts in this guide
transfer. The code does not, and is
not offered as if it does.

## Your documents, your questions

Finally, the boundary that is a
feature: the lab keeps documents and
questions on one machine. Sending
either to a hosted model means the
chunks in every prompt — the most
relevant passages of your documents,
selected for relevance — travel to
someone else's computer, along with
what you asked about them. Sometimes
that trade is worth making. Chapter
14's rule is only that it be made
knowingly: the privacy of a RAG
system is decided by where its model
lives.
