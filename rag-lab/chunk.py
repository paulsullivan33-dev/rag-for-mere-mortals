"""Show the chunking of the sample documents.

Run:  python3 chunk.py
Reads every .txt file in docs/ and prints the chunks it makes:
id, word count, and the opening words of each.
"""

from pathlib import Path

from ragcore import chunk_document

DOCS = Path(__file__).parent / "docs"


def main():
    total = 0
    for path in sorted(DOCS.glob("*.txt")):
        chunks = chunk_document(path.stem, path.read_text(encoding="utf-8"))
        total += len(chunks)
        print(f"{path.name}: {len(chunks)} chunks")
        for cid, text in chunks:
            words = text.split()
            opening = " ".join(words[:10])
            print(f"  {cid:<28} {len(words):>3} words  {opening}...")
        print()
    print(f"Total: {total} chunks")


if __name__ == "__main__":
    main()
