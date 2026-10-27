# Asking Questions End to End

By the end of this chapter you have
run the whole pipeline on real
questions, read a complete exchange
with nothing hidden, and you know
exactly which part of it a real model
replaces.

## One question, whole

```bash
python3 ask.py "What oil should I use for the polisher bearings?"
```

`ask.py` prints its work at every
stage (transcript
`rag-lab/transcripts/t04-ask.txt`).
Retrieval first:

```text
Retrieved:
  bramble-mk2-manual#6  score 0.477
  harbourlight-newsletter#6  score 0.158
  bramble-mk2-manual#9  score 0.145
  bramble-mk2-manual#1  score 0.134
```

The oiling chunk — manual #6 — leads,
with three weaker neighbours behind
it on the strength of shared words
like *polisher*. Those four chunks
become the sources in the grounded
prompt, printed in full (chapter 8's
template, filled in). Then the
answer:

```text
Oiling and brushes: Oil the bearings every 100 hours of
running, using two drops of light machine oil, ISO VG 32,
in the oil cup at each end of the spindle.
[from bramble-mk2-manual#6]
```

The answer is the manual's own
sentence, quoted, with its source
named. Every fact in it — 100 hours,
two drops, ISO VG 32 — can be checked
against chunk #6 in seconds.

## The stand-in, examined

There is no language model in that
exchange, and the output says so on
its face: "Stand-in answer
(mechanical, not a language model)".

The **stand-in** (`ask.py`, function
`stand_in_answer`) does mechanically
what the prompt asks a model to do.
It splits the retrieved chunks into
sentences. It scores each sentence by
how much of the question's
informative weight it covers — the
idf of the question words it
contains, divided by the idf of all
the question's words, with words
absent from the whole set counting at
the maximum weight. If the best
sentence covers at least half the
question's weight and shares at least
two of its words, the stand-in quotes
it and cites its chunk. Otherwise it
answers with the prompt's exact
refusal: *The documents do not say.*

Two of the transcript's six questions
exist to exercise that refusal:

- "What is the spindle speed of the
  Bramble **Mk III**?" The documents
  describe the Mk II. Retrieval
  happily surfaces the Mk II
  specification chunk — and the
  stand-in still refuses, because
  *iii*, a word appearing nowhere in
  the documents, drags the coverage
  below the line. A question about an
  absent thing *should* score badly;
  the arithmetic makes it so.
- "Who won the spring regatta last
  year?" The regatta chunk retrieves,
  the word *won* appears in no chunk,
  and the answer is again the
  refusal.

A real model is stronger than the
stand-in — it can combine two chunks,
rephrase, and convert units — and
weaker in one specific way: it can
invent, fluently, where the stand-in
structurally cannot. Keep both halves
of that sentence. Chapter 11 is the
discipline for the second half.

## The three outcomes

Every question a RAG system meets
ends in one of three ways:

| Outcome | Meaning | Lab example |
|---|---|---|
| Answered, with citation | A chunk held the fact and the answer used it | The oil question, above |
| Refused | No chunk held it, and the system said so | The Mk III question |
| Answered anyway | No chunk held it, and the system wrote something regardless | **Never acceptable** — the failure the rule exists to prevent |

The third row is the only disgrace
available to this machinery, and the
whole design — the prompt's exact
refusal, the citation demand, the
test set — is arranged to make it
visible when it happens.

## Swapping in a real model (documented only)

The stand-in occupies one function.
Replacing it with a real local model
— served by **Ollama**, the subject
of its own guide in this series — is
a small change: take the prompt
string `ask.py` already assembles,
and post it to the model server
instead of scoring sentences:

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3:4b",
  "stream": false,
  "messages": [
    {"role": "user", "content": "<the grounded prompt, verbatim>"}
  ]
}'
```

The reply's `message.content` is the
answer. Nothing upstream changes:
same chunks, same store, same prompt,
same citation rule to audit against.

**This swap is documented-only in
this guide, and labelled as such
wherever it matters.** The build
machine had no model server
reachable: the check
(`rag-lab/transcripts/t06-model-server-check.txt`)
shows the connection to
`localhost:11434` refused, and a
known model-serving address on the
local network unreachable from the
sandbox as well. So no transcript in
this guide shows a real model's
answer, and no chapter claims one.
What is verified here is everything
the prompt carries to that boundary —
which, in a RAG system, is most of
the machine.
