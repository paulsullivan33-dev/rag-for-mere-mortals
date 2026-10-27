# When RAG Is the Wrong Tool

By the end of this chapter you can
look at a job and say whether RAG
fits it — and name the simpler tool
when it does not. Reaching for RAG by
default is the most common way this
machinery disappoints people.

## The corpus fits in your head

If the whole document set is three
short files, *read them*. The lab
itself is nearly this case: its 26
chunks exist to make the machinery
visible, not because a newsletter
needs an index. RAG earns its keep
when the set is too large to hold
in mind and too valuable to skim —
hundreds of pages of manuals,
minutes, records. Below that, a
folder and a text search (chapter
14) answer faster and cannot
hallucinate at all.

## The question needs all of it

Retrieval returns a *few* chunks.
Questions whose answers live in the
whole set — "what do all these
invoices total?", "which themes run
through a year of minutes?", "list
every part number mentioned anywhere"
— are starved by design: the missing
chunks are not noise, they are the
answer. Such questions want the
documents processed whole (a script,
a spreadsheet, or a long-context
model with the set in the prompt,
chapter 14), not sampled by
similarity.

## The answer is not in any document

RAG grounds answers in your set. It
says nothing useful about the wider
world: tomorrow's weather, the
capital of anywhere, why your code
throws an error that no local
document discusses. Worse, asked such
a question, a weakly-grounded system
may force the nearest chunk into an
answer-shaped object. If the
knowledge is the model's own or the
public web's, ask there, and do not
let your documents be ventriloquised.

## The job is writing, not recall

Drafting a letter, brainstorming
names, rewording a paragraph: there
is no fact to retrieve and no
citation that would mean anything.
Grounding machinery adds cost and a
false air of authority to work whose
value is judgement. Use the model
bare, and review like an editor.

## The facts change faster than you rebuild

Chapter 10's rule cuts both ways. A
set that changes hourly — prices,
rosters, live schedules — behind an
index rebuilt weekly is a machine
for producing confident, cited,
out-of-date answers, which are worse
than honest ignorance. Either the
rebuild keeps pace (automatically,
on every change) or RAG is the wrong
shape for that data.

## The documents are the problem

RAG repeats your documents
faithfully. If they are wrong,
outdated, or two drafts arguing with
each other, the system laundered
through citations is still wrong —
with better presentation. Some jobs
that arrive dressed as "we need to
ask our documents questions" are
really "our documents need an
editor". No pipeline fixes that, and
chapter 15 returns to it.
