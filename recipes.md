# Recipes

Small jobs, whole. Each assumes the
lab of chapters 3 to 9 and works with
the documents you put in `docs/`.

## A manual on the workbench

The lab's own arrangement, pointed at
a real machine: save the manual as
text (from the maker's PDF, a
scanner, or the support site) into
`docs/`, run `python3 build_index.py`,
and ask it questions at the bench:

```bash
python3 ask.py "What size is the oil seal on the output shaft?"
```

Keep the manufacturer's wording where
you can — retrieval rewards the
documents' own vocabulary (chapter
7), and part numbers, being rare
words with high idf, retrieve
beautifully.

## What did we decide?

Point the lab at a folder of meeting
minutes — one file per meeting, named
by date. Questions like "When did we
agree to replace the roof?" work
because minutes record decisions in
plain sentences, and the citation
takes you back to the meeting that
made the decision. When two meetings
decided differently, chapter 10's
rule applies: the later file is a
new document, not a contradiction the
system can resolve for you — read
both citations.

## Add a document, in full

Chapter 10 compressed to the two
commands that are the whole
procedure:

```bash
cp new-document.txt docs/
python3 build_index.py
```

Then ask one question only the new
document can answer, and check it
answers with the new chunk's
citation. That question is your
receipt that the rebuild happened.

## A scheduled rebuild

For a document set that changes on
other people's schedules, rebuild
without being asked. On a Linux
machine, a line in your crontab
(`crontab -e`):

```text
15 6 * * 1 cd /home/you/rag-lab && python3 build_index.py >> build.log 2>&1
```

rebuilds at 06:15 every Monday and
keeps a log. Adjust the path and the
hour; the point is that freshness
stops depending on memory.

## Questions that retrieve well

A pattern, learned from the test set:

- **One fact per question.** "When is
  the regatta and what are the dues?"
  splits retrieval two ways and
  grounds neither well. Ask twice.
- **Use the documents' nouns.**
  "Belt tension" beats "the stretchy
  part", because similarity here is
  built from shared words.
- **Name the thing.** "What oil does
  the *polisher* need?" out-retrieves
  "What oil does it need?" — pronouns
  carry no weight in any vector.

## A reading list from citations

Every answer the lab gives ends in a
citation. Collect them over a
session and you have, for free, the
list of passages that actually
mattered — usually a tenth of the
document set. That list is the
sensible order in which to read the
documents properly, if reading them
properly is where the questions were
leading all along.
