# What RAG Is

By the end of this chapter you can say
what RAG is, why asking a language model
about your own documents fails without
it, and what rule keeps the answers
honest.

A **language model** — the program
behind chatbots such as the ones you
may have used — writes by predicting
text. It learned from an enormous pile
of other people's documents. Your
documents were not in the pile. Ask it
what your workshop manual says about
belt tension and it does not think *I
do not know this manual*; it produces
a fluent, plausible answer anyway,
because producing fluent text is the
whole of its training. When a model
states something false with complete
confidence, that is called a
**hallucination**, and no amount of
politeness in the question prevents
it. The model is not lying. It simply
has no way to know what it does not
know.

**RAG — retrieval-augmented
generation** — fixes this by changing
what the model is given. Before the
model writes anything, a **retriever**
searches your documents for the
passages that bear on the question,
and those passages are pasted into the
request alongside it. The model is no
longer answering from memory. It is
answering from the page in front of
it, like a student in an open-book
exam:

1. You ask a question.
2. The retriever finds the few
   passages — **chunks** — most
   relevant to it.
3. The chunks and the question are
   assembled into one request, the
   **grounded prompt**.
4. The model writes an answer using
   those chunks.
5. The answer names the chunks it
   used, so you can check.

Each step is a separate piece of
machinery, and each can fail in its
own way. That is good news: a failure
you can locate is a failure you can
fix. Chapter 2 names the pieces.

## The honesty rule, stated early

Everything in this guide hangs on one
rule, and it is not fine print:

> **An answer must say where it came
> from. Every fact is cited to the
> chunk it came from — and when the
> documents hold no answer, "the
> documents do not say" is a correct
> answer. The correct one.**

The citation is not decoration. It is
a promise you can verify: open the
chunk, and the fact is either there
or it is not. Chapter 11 builds a
small test set that checks exactly
this, including questions designed to
tempt the system into inventing. A
system that says *the documents do
not say* when it should is not
broken; it is the whole point.

## The lab, honestly labelled

This guide builds the whole pipeline
for real, in `rag-lab/`, using only
the Python standard library — no
framework, nothing to install beyond
Python itself. The documents are
invented: a model boat club's
newsletter and regatta rules, and the
workshop manual for a bench polisher
that does not exist. The questions
have definite answers, so every claim
the chapters make can be checked
against the transcripts in
`rag-lab/transcripts/`.

One part is a stand-in, and the guide
never hides it. A working language
model needs a model server; the build
machine for this guide had none
reachable (chapter 9 shows the check
and its result). So the lab's final
step — the "model" — is a small
mechanical program that does openly
what the grounded prompt asks a model
to do: quote the retrieved sentence
that answers the question, cite it,
or refuse. It cannot write freely,
and it cannot invent. Chapter 9 shows
the exact swap that replaces it with
a real local model, and labels that
swap documented-only, because it was
not run here. What the stand-in
proves is that the machinery around
the model — chunking, retrieval, the
prompt, the refusals — works. That
machinery is most of RAG.

## What RAG is not

RAG is not training. Nothing about
the model changes; you are handing it
a book, not educating it (chapter 14
contrasts this with fine-tuning).
RAG is not a search engine on its
own: search finds passages, and a
person still reads them; RAG adds a
written answer on top — and chapter
14 says plainly when search alone is
the better tool. And RAG is not a
truth machine. It grounds answers in
your documents. If your documents are
wrong, the answers will be faithfully,
citably wrong (chapter 15).
