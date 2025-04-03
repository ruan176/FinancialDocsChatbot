NOTE: See [prototypeSummary.md](prototypeSummary.md) for further detail on prototype.

# Initial Process Flow

The methods are purposely decoupled to enable testing and assessment of each section of the prototype. Once each section is performing as required they could be refined, refactored and run via a `main.py` file.

Running the five files in the order highlighted below, provides an end2end overview of the prototype.

## 1. extract_and_generate_content_data.py
Takes `train.json` and strips out the content used as context to answer user questions. File also generates the section summaries and section embeddings.

## 2. extract_qa_pairs.py
Takes `train.json` and creates a file of indexed question and answer pairs, used to assess prototype performance.

## 3. dedupe_content.py
Deduplicates any repeated content. (Note: This should be done in step 1 ideally, but the requirement was only identified in later testing. The `dedupe_content.py` file
has a note summarising a more effecient implementation solution).

---
### At this point the preprocessing is complete and now the prototype can be defined and assessed.
---

## 4. section_test.py
Takes a user question (in its current development form it takes random questions from the `extract_qa_pairs.py` output file) as an input and seeks to identify the most relevant content section to help answer the question.

## 5. response_test.py
Given a content section from the previous step and a user question input it aims to calculate and provide a response to the user.

# Assumptions
- The question and answers provided in `train.json` provide no additional context, and are purely considered as examples of questions that would be asked.
- The example questions are assumed to be representative questions, and it is currently out of scope to ask for specific sections or pages (e.g. Summarise section 12 of the document). This is possible but would require further development, likely using metadata to capture this detail.

