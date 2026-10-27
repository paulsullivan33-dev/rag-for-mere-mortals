# The Neighbours

By the end of this chapter you can
place RAG among its three closest
relatives — fine-tuning, long
context, and plain search — and say
what each does that RAG does not, and
vice versa.

## Fine-tuning: teach the model

**Fine-tuning** trains a model
further on examples you supply, and
the training changes the model
itself. What it is good at is
*behaviour*: a house style, a reply
format, the knack of a specialised
task. What it is bad at is *facts you
can point to*: knowledge baked in by
training arrives without citations,
cannot be checked against a source,
and goes stale the day the facts
change — retraining is the only
rebuild. RAG is the opposite shape:
the model stays general, the
documents stay editable, and every
answer can be audited to a chunk.

The two compose more often than they
compete. A fine-tuned model that has
learned your house style can still
answer from retrieved chunks. But if
the problem is "the model does not
know our documents", fine-tuning is
the expensive answer to a question
RAG answers by lunchtime. (This
series treats the teaching side in
*LoRA Fine-Tuning for Mere Mortals*.)

## Long context: hand over everything

Modern models accept very large
prompts. If your whole document set
fits in the context window with room
to spare, you can skip retrieval
entirely: paste everything, ask the
question. It is simpler, it cannot
suffer a retrieval miss, and for a
small, stable set it may be the right
engineering.

The costs scale with honesty about
size. Every question pays to process
the whole set again. Models also
attend unevenly across very long
prompts — the middle of a huge
context is where facts go to be
overlooked. RAG is what long context
turns into when the set outgrows the
window, the budget, or the model's
attention: choose the few chunks that
matter, and spend the window on
them.

## Plain search: no model at all

A text search — `grep`, your editor's
find, a desktop search tool — answers
"where is X mentioned?" exactly, with
no machinery that can misunderstand.
When the reader intends to read the
passage anyway, search is not the
primitive option; it is the correct
one, and RAG's answer is a summary
they did not need.

What RAG adds over search is the
written answer: gathered, phrased,
and cited, for readers who need the
fact rather than the passage. What
search keeps over RAG is certainty:
it returns every occurrence, verbatim,
including the one a ranking would
have left at position five. Know
which of the two your question
actually wants.

## Hosted chatbots with upload buttons

The same shape as this guide's lab,
run on someone else's computer: you
upload documents, a service chunks
and indexes them, its model answers.
Convenient, often good, and a
decision about your documents — they
leave your machine, live under
someone else's retention policy, and
answer through a pipeline you cannot
inspect or test the way chapter 11
tests this one. For public documents
that may be a fine trade. For
anything private, the local version
in this guide — or a local front end
such as the one in *Open WebUI for
Mere Mortals* — keeps the documents,
and the questions, at home.
