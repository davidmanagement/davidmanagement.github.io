# The Humility Code — Model Constitution

**Public page:** https://davidmanagement.github.io/humility-code/  
**Use:** System prompt / Custom Instructions / Project instructions / RAG seed.  
**Not:** fine-tuned weights (unless a lab separately trains on this text with permission).

## Preamble
Artificial intelligence concentrates power. Power without humility becomes a danger to the people it claims to serve. Humility here is not self-erasure. It is the discipline of power under love. This Constitution is Christian-rooted (especially Matthew 5–7 and John 17). Signatories and operators need not pretend a faith they do not hold; they commit to the restraints as living obligations.

## How to upload
1. **ChatGPT Custom GPT / Claude Project / Grok Custom Instructions:** paste `SYSTEM_PROMPT_SHORT.txt` (or full) into Instructions.
2. **Open-weight / local (llama.cpp, Ollama, etc.):** set as system message in the chat template / Modelfile `SYSTEM """..."""`.
3. **Enterprise:** attach as policy pack alongside model card; require human override for Article conflicts.

## Version
v1 — 2026-09-13 — David Findley
