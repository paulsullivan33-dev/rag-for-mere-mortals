"""Shared machinery for the RAG lab.

Everything here is the Python standard library on purpose: the
point of the lab is that each moving part of retrieval-augmented
generation can be seen working, with no framework in the way.

The parts, in pipeline order:

  chunk_text()  -- split a document into chunks
  tokenise()    -- split text into words for scoring
  TfidfIndex    -- the TF-IDF weights that stand in for embeddings
"""

import math
import re
from collections import Counter

# Words so common they carry almost no information about what a
# text is *about*. They are dropped before scoring. The list is
# deliberately small and boring; chapter 5 talks about it.
STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "at",
    "for", "by", "with", "from", "into", "is", "are", "was", "were",
    "be", "been", "it", "its", "this", "that", "these", "those",
    "i", "you", "he", "she", "we", "they", "me", "him", "us", "them",
    "my", "your", "his", "her", "our", "their", "do", "does", "did",
    "should", "would", "can", "could", "may", "might", "must",
    "shall", "will", "what", "when", "where", "who", "whom", "how",
    "why", "which", "if", "then", "than", "so", "as", "not", "no",
    "there", "here", "any", "all", "each",
}

WORD = re.compile(r"[a-z0-9]+")


def tokenise(text):
    """Lowercase word tokens, stopwords removed, order kept."""
    return [w for w in WORD.findall(text.lower()) if w not in STOPWORDS]


# --- chunking -----------------------------------------------------

MAX_WORDS = 70     # a chunk is at most about this many words
WINDOW = 60        # sliding window size for long blocks
OVERLAP = 12       # words shared between neighbouring windows
HEADING_WORDS = 6  # blocks this short are headings, not chunks


def chunk_document(name, text):
    """Split one document into chunks.

    Blocks are separated by blank lines. A short block is one
    chunk. A long block is cut into overlapping windows, so a
    fact that straddles a cut still appears whole in one chunk.

    A block of HEADING_WORDS or fewer words is treated as a
    heading and glued onto the block that follows it, so the
    heading's words travel with the text they name instead of
    forming a useless one-line chunk of their own.

    Returns a list of (chunk_id, text) pairs. Chunk ids look
    like "bramble-mk2-manual#7": document, then position.
    """
    raw_blocks = []
    for raw in text.split("\n\n"):
        block = " ".join(raw.split())
        if block:
            raw_blocks.append(block)

    blocks = []
    pending = []
    for block in raw_blocks:
        if len(block.split()) <= HEADING_WORDS:
            pending.append(block)
            continue
        if pending:
            block = ": ".join(pending + [block])
            pending = []
        blocks.append(block)
    blocks.extend(pending)

    chunks = []
    for block in blocks:
        words = block.split()
        if len(words) <= MAX_WORDS:
            chunks.append(block)
            continue
        start = 0
        while start < len(words):
            chunks.append(" ".join(words[start:start + WINDOW]))
            if start + WINDOW >= len(words):
                break
            start += WINDOW - OVERLAP
    return [(f"{name}#{i + 1}", c) for i, c in enumerate(chunks)]


# --- TF-IDF: the lab's stand-in for embeddings --------------------


class TfidfIndex:
    """Term weights for a set of chunks.

    Each chunk becomes a vector: one number per word, the word's
    count in the chunk multiplied by its inverse document
    frequency (idf) -- a measure of how rare, and therefore how
    informative, the word is across the whole set. Two texts are
    "similar" when their vectors point the same way (cosine
    similarity). Chapter 5 explains why this can stand in for a
    neural embedding, and where it cannot.
    """

    def __init__(self, chunks):
        """chunks: list of (chunk_id, text)."""
        self.chunk_ids = [cid for cid, _ in chunks]
        self.texts = dict(chunks)
        n = len(chunks)
        doc_freq = Counter()
        self.term_counts = {}
        for cid, text in chunks:
            counts = Counter(tokenise(text))
            self.term_counts[cid] = counts
            for term in counts:
                doc_freq[term] += 1
        self.idf = {
            term: math.log((1 + n) / (1 + df)) + 1.0
            for term, df in doc_freq.items()
        }
        # The weight an unseen word would get: the maximum, so a
        # question about something absent scores honestly badly.
        self.max_idf = math.log(1 + n) + 1.0
        self.vectors = {
            cid: {t: c * self.idf[t] for t, c in counts.items()}
            for cid, counts in self.term_counts.items()
        }
        self.norms = {
            cid: math.sqrt(sum(w * w for w in vec.values()))
            for cid, vec in self.vectors.items()
        }

    def idf_of(self, term):
        return self.idf.get(term, self.max_idf)

    def search(self, question, k=4):
        """Return the k best (chunk_id, cosine score), best first."""
        qcounts = Counter(tokenise(question))
        qvec = {t: c * self.idf_of(t) for t, c in qcounts.items()}
        qnorm = math.sqrt(sum(w * w for w in qvec.values()))
        if qnorm == 0:
            return []
        scored = []
        for cid in self.chunk_ids:
            vec = self.vectors[cid]
            dot = sum(w * vec.get(t, 0.0) for t, w in qvec.items())
            if dot > 0 and self.norms[cid] > 0:
                scored.append((cid, dot / (qnorm * self.norms[cid])))
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return scored[:k]


def split_sentences(text):
    """Split chunk text into sentences, keeping the punctuation."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]
