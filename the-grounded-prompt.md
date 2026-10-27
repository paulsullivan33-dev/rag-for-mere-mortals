# Writing the Grounded Prompt

By the end of this chapter you can
write the request that turns a
general language model into a
document-bound answerer, and you can
say what each line of it is for.

## The shape

A **prompt** is the full text handed
to the model: not just the question,
but everything the model is given to
work with. The **grounded prompt**
has three parts — instructions,
sources, question — and the lab's
template, used verbatim by `ask.py`,
is short enough to print whole:

```text
Answer the question using only the sources below.
Do not use any other knowledge.
Cite the source id for every fact you state, like this: [source: manual#3]
If the sources do not contain the answer, reply with exactly:
The documents do not say.

Sources:
[source: bramble-mk2-manual#5] Checking the belt: Check the belt
tension every 40 hours of running. ...

Question: How often should I check the belt tension?
Answer:
```

## The three instructions that matter

**Use only the sources.** Without
this line, a model treats the chunks
as a hint and tops them up from its
training — fluent, uncited, and
uncheckable. With it, the chunks are
the whole allowed world. (A model can
still disobey; chapter 15 is honest
about that. The instruction's job is
to make disobedience a visible
breach, not a grey area.)

**Cite every fact, by id.** Each
source in the prompt carries its
chunk id, and the instruction demands
the id back in the answer. This is
what converts an answer from an
assertion into a claim you can audit:
open chunk `bramble-mk2-manual#5` and
check whether it really says 40
hours. Chapter 11 runs that audit as
a procedure.

**Refuse in exactly these words.**
"If the sources do not contain the
answer, reply with exactly: *The
documents do not say*." The exactness
matters twice over. A human reader
recognises the refusal instantly,
with no hedging to interpret; and a
program can detect it with a string
comparison, which is how the lab's
test set (chapter 11) and any real
monitoring work. A refusal that comes
out as a paragraph of apologies is a
refusal that downstream code cannot
see.

## What the prompt leaves out

No personality, no preamble about
being an AI, no examples. Not because
those are wrong — a real deployment
may add examples of good answers,
which genuinely help — but because
this guide's method is to add one
thing at a time and keep what earns
its place. The three instructions
above are the ones the honesty rule
of chapter 1 requires. Everything
else is taste, and taste should be
tested (chapter 11 again), not
assumed.

## The prompt is a contract

Read the template once more as what
it is: a contract offered to the
model. The system's side of it is
retrieval — *we will put the right
text in front of you*. The model's
side is grounding — *use only this
text, show your working, and admit
it when the text is not enough*. The
lab's stand-in keeps the contract
perfectly because it can do nothing
else. A real model keeps it
imperfectly, which is why the
contract is written to be audited
rather than trusted.
