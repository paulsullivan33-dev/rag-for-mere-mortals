"""Build the index: chunk the documents, weight the words,
and store both in a SQLite database, rag.db.

Run:  python3 build_index.py
Rebuilding is the whole update procedure: run it again whenever
the documents change and the index is fresh (chapter 10).
"""

import sqlite3
from pathlib import Path

from ragcore import TfidfIndex, chunk_document

HERE = Path(__file__).parent
DOCS = HERE / "docs"
DB = HERE / "rag.db"


def main():
    chunks = []
    for path in sorted(DOCS.glob("*.txt")):
        found = chunk_document(path.stem, path.read_text(encoding="utf-8"))
        chunks.extend(found)
        print(f"{path.name}: {len(found)} chunks")

    index = TfidfIndex(chunks)

    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript(
        """
        CREATE TABLE chunks (
            id       TEXT PRIMARY KEY,
            source   TEXT NOT NULL,
            position INTEGER NOT NULL,
            norm     REAL NOT NULL,
            text     TEXT NOT NULL
        );
        CREATE TABLE idf (
            term TEXT PRIMARY KEY,
            idf  REAL NOT NULL
        );
        CREATE TABLE postings (
            term     TEXT NOT NULL,
            chunk_id TEXT NOT NULL,
            weight   REAL NOT NULL,
            PRIMARY KEY (term, chunk_id)
        );
        """
    )
    for position, (cid, text) in enumerate(chunks):
        source = cid.rsplit("#", 1)[0]
        con.execute(
            "INSERT INTO chunks VALUES (?, ?, ?, ?, ?)",
            (cid, source, position, index.norms[cid], text),
        )
    con.executemany(
        "INSERT INTO idf VALUES (?, ?)", sorted(index.idf.items())
    )
    rows = [
        (term, cid, weight)
        for cid, vec in index.vectors.items()
        for term, weight in vec.items()
    ]
    con.executemany("INSERT INTO postings VALUES (?, ?, ?)", rows)
    con.commit()

    print(f"Stored {len(chunks)} chunks")
    print(f"Stored {len(index.idf)} distinct terms")
    print(f"Stored {len(rows)} postings (term-in-chunk weights)")
    print(f"Database: {DB.name} ({DB.stat().st_size} bytes)")
    con.close()


if __name__ == "__main__":
    main()
