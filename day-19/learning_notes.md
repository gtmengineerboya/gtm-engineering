# Day 19 learning notes

AI research should not turn a guess into a fact. The output schema separates
copied observed facts from labeled hypotheses, records which fields support
each hypothesis, and includes confidence and limitations.

The validator checks that every observed fact matches a supplied input field.
It does not claim to prove arbitrary natural-language hypotheses. When Ollama
is unavailable or returns invalid JSON, the fallback contains only known
source fields and an explicit reason. The local model is optional; no external
enrichment service is called.
