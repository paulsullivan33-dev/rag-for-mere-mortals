# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's traffic is the lab talking to itself.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 13 names what the tool
   cannot do: clients that pin their certificates, traffic that
   is not HTTP, programs that never use a proxy, the CA as a
   liability, the recordings as secrets, and the legal edge
   around intercepting anything that is not yours.
8. **The ethics rule is in the text, early.** Chapter 1 and the
   README state the rule plainly — *your traffic, your
   machines, or explicit permission* — before any procedure
   depends on it, and later chapters point back to it where the
   tooling would make crossing the line easy.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.7 GB Ubuntu 24.04 sandbox
running Python **3.12.3**. The lab (`rag-lab/`) uses only the
Python standard library — there was nothing to install. All
transcripts live in `rag-lab/transcripts/`; the pipeline is
`ragcore.py` (chunking and TF-IDF) with four small faces:
`chunk.py`, `build_index.py`, `search.py`, `ask.py`.

Run for real, with transcripts as evidence:

- Chunking of the three sample documents under the guide's
  rules (blank-line blocks, headings of six words or fewer
  glued to the following block, 70-word cap, 60/12 windowing
  for long blocks): 26 chunks — 12 manual, 8 newsletter,
  6 rules (t01).
- Building the index into a SQLite store and reading it back
  with the sqlite3 command: 26 chunks, 437 distinct terms,
  658 postings, and the worked TF-IDF example verified from
  the store itself (the word *belt*: idf 3.20; weight 15.99
  in `bramble-mk2-manual#5`, 3.20 in `#2`) (t02).
- Retrieval rankings for three questions, including the
  cross-document discrimination of "spring regatta" and the
  single-hit "life jacket pontoon" (t03).
- Asking end to end: six questions with the grounded prompt
  printed in full — four answered from the correct chunk
  with citation, two refused with the exact refusal sentence
  (the Bramble Mk III near miss, and the unrecorded regatta
  winner) (t04).
- Freshness: a question refused, a fourth document added,
  the index rebuilt (26 to 27 chunks), and the same question
  answered from the new chunk with its citation (t05).
- The nine-question answer-quality test set of chapter 11:
  seven expected answers with the expected citations, two
  expected refusals, no invented answers (t07).

Documented only — described from documentation and reasoning,
not run, and the text does not claim otherwise:

- **The real-model swap of chapter 9.** Replacing the
  stand-in with a language model served by Ollama (a local
  `POST /api/chat` carrying the same grounded prompt) is
  presented as the documented integration it is. No model
  server was reachable from the build machine: the check is
  recorded in t06 — the connection to `localhost:11434` was
  refused (curl exit 7) and a known model-serving address on
  the local network was likewise unreachable (curl exit 52).
  Every answer quoted in this guide therefore comes from the
  lab's mechanical stand-in, which the chapters label as one
  wherever it appears. The stand-in proves the pipeline —
  chunking, retrieval, prompt assembly, citation, refusal —
  and cannot prove a real model's behaviour inside it;
  chapters 11 and 15 say exactly that.
- **Neural embeddings.** Chapter 5 explains what an
  embedding model computes and contrasts it with the lab's
  TF-IDF stand-in, whose weights *were* computed and
  verified. No embedding model was run; no similarity score
  in this guide comes from one.
- **Scale.** Chapter 15's remarks about thousands to
  millions of chunks, dedicated vector databases, and
  incremental indexing are characterisations of the field,
  not measurements. The verified system is 26 chunks, and
  nothing in the guide presents it as more.
- **Hosted services** (chapter 14's upload-and-ask
  chatbots) are characterised, not used; no document left
  the build machine.

Fixtures are this guide's own and deliberately generic: an
invented model boat club, its newsletter and regatta rules,
the workshop manual for an invented bench polisher, and a
workshop notice. No example is modelled on any real person,
club, machine, network, or organisation — which is what
makes the test set's expected answers provable rather than
plausible.
