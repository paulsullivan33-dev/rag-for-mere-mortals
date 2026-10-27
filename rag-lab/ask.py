"""Ask a question, end to end.

Run:  python3 ask.py "your question here"

The pipeline, exactly as chapters 7 to 9 describe it:

  1. Retrieve the best-matching chunks from rag.db.
  2. Assemble the grounded prompt: the honesty instructions,
     the chunks (each labelled with its id), the question.
     The prompt is printed in full -- it is the same text a
     real model would receive.
  3. A "model" produces the answer.

Step 3 in this lab is a STAND-IN, and it is labelled as one.
There is no language model in the lab. The stand-in does,
openly and mechanically, what the prompt asks a model to do:
it picks the sentence from the retrieved chunks that best
covers the question's informative words, quotes it, and cites
its chunk. If no sentence covers enough of the question, it
answers with the refusal the prompt prescribes:

    The documents do not say.

A real model (chapter 9 shows the swap, using a local model
server) writes freer answers from the same prompt -- and can
also wander off it, which is why chapter 11 exists. The
stand-in's virtue is that it cannot invent: every word of its
answer is a quotation.
"""

import sqlite3
import sys
from collections import Counter
from pathlib import Path

from ragcore import TfidfIndex, split_sentences, tokenise

DB = Path(__file__).parent / "rag.db"

RETRIEVAL_MIN = 0.05   # a chunk scoring below this is not a source
COVER_MIN = 0.5        # a sentence must cover this much of the question

PROMPT_TEMPLATE = """\
Answer the question using only the sources below.
Do not use any other knowledge.
Cite the source id for every fact you state, like this: [source: manual#3]
If the sources do not contain the answer, reply with exactly:
The documents do not say.

Sources:
{sources}

Question: {question}
Answer:"""


def load_index():
    con = sqlite3.connect(DB)
    chunks = [
        (cid, text)
        for cid, text in con.execute("SELECT id, text FROM chunks ORDER BY position")
    ]
    con.close()
    return TfidfIndex(chunks)


def stand_in_answer(index, question, sources):
    """The honest mechanical "model": quote or refuse.

    Scores every sentence in the sources by how much of the
    question's informative weight it covers (idf-weighted).
    Unseen question words count at the maximum weight, so a
    question about an absent thing scores badly -- as it should.
    """
    qterms = Counter(tokenise(question))
    if not qterms:
        return "The documents do not say."
    total = sum(index.idf_of(t) for t in qterms)
    best = None
    for cid, text in sources:
        for sentence in split_sentences(text):
            sterms = set(tokenise(sentence))
            shared = [t for t in qterms if t in sterms]
            if len(shared) < 2:
                continue
            coverage = sum(index.idf_of(t) for t in shared) / total
            if best is None or coverage > best[0]:
                best = (coverage, sentence, cid)
    if best is None or best[0] < COVER_MIN:
        return "The documents do not say."
    _, sentence, cid = best
    return f"{sentence}\n[from {cid}]"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return
    question = sys.argv[1]
    index = load_index()

    hits = [
        (cid, score)
        for cid, score in index.search(question)
        if score >= RETRIEVAL_MIN
    ]
    sources = [(cid, index.texts[cid]) for cid, _ in hits]

    print("Retrieved:")
    if hits:
        for cid, score in hits:
            print(f"  {cid}  score {score:.3f}")
    else:
        print("  (nothing above the retrieval threshold)")
    print()

    source_block = "\n".join(
        f"[source: {cid}] {text}" for cid, text in sources
    ) or "(no sources)"
    prompt = PROMPT_TEMPLATE.format(sources=source_block, question=question)
    print("--- The grounded prompt (what a real model would receive) ---")
    print(prompt)
    print("--- End of prompt ---")
    print()
    print("Stand-in answer (mechanical, not a language model):")
    print(stand_in_answer(index, question, sources))


if __name__ == "__main__":
    main()
