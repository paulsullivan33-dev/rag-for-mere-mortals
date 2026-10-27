"""Retrieval only: show the ranked chunks for a question.

Run:  python3 search.py "your question here"
Reads rag.db (build it first with build_index.py) and prints
the best-matching chunks with their cosine scores, best first.
No answer is produced -- this is the stage chapter 7 is about:
the model, whatever it is, can only use what retrieval finds.
"""

import sqlite3
import sys
from pathlib import Path

from ragcore import TfidfIndex

DB = Path(__file__).parent / "rag.db"


def load_index():
    con = sqlite3.connect(DB)
    chunks = [
        (cid, text)
        for cid, text in con.execute("SELECT id, text FROM chunks ORDER BY position")
    ]
    con.close()
    return TfidfIndex(chunks)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return
    question = sys.argv[1]
    index = load_index()
    print(f"Question: {question}")
    print()
    for rank, (cid, score) in enumerate(index.search(question), start=1):
        text = index.texts[cid]
        opening = " ".join(text.split()[:14])
        print(f"{rank}. {cid}  score {score:.3f}")
        print(f"   {opening}...")
    print()


if __name__ == "__main__":
    main()
