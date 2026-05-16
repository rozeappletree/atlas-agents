"""
adaptive_chunker.py — Header-aware chunking vs. naive character splitting.

The problem: character-count chunking splits documents at arbitrary byte
offsets. A 1000-character chunk might end mid-sentence, mid-code-block,
or mid-table — destroying the context that makes a chunk answerable.

This script splits the same document both ways and prints both outputs
side by side so you can see exactly where character chunking breaks down.

    python adaptive_chunker.py

No API keys required — this is pure text processing.

Requires: pip install langchain-text-splitters
"""

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

SAMPLE_DOC = """
# MCP Server Design

The Model Context Protocol defines how tools expose themselves to agents.
A well-designed MCP server is stateless, idempotent, and scoped.

## Authentication

Every MCP server must validate the caller before executing any tool.
Use bearer tokens passed in the Authorization header. Never accept
unauthenticated requests, even on internal networks.

### Token Validation

Tokens are JWTs signed with your server's private key. Validate the
signature, the `exp` claim, and the `aud` claim on every request.
Do not cache validation results across requests.

## Error Handling

Errors must be structured. Return a JSON object with `error.code`
and `error.message`. Never return raw exception tracebacks to callers —
they leak implementation details and confuse agents.

### Retryable vs. Terminal Errors

Use HTTP 429 for rate limits (retryable). Use HTTP 400 for invalid
tool arguments (terminal — retrying won't help). Use HTTP 500 only
for unexpected server faults. Agents use these codes to decide whether
to retry or escalate.

## Tool Scoping

Each tool should do exactly one thing. A tool named `search_and_summarize`
is two tools badly merged. Split it: agents can then choose which step
to skip, and you can version each independently.
""".strip()


def character_chunks(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )
    return splitter.split_text(text)


def header_chunks(text: str) -> list[dict]:
    """Split by markdown headers; each chunk carries its header path as metadata."""
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ],
        strip_headers=False,
    )
    return splitter.split_text(text)


def main():
    char_results = character_chunks(SAMPLE_DOC)
    header_results = header_chunks(SAMPLE_DOC)

    print("=" * 72)
    print(f"CHARACTER CHUNKING  ({len(char_results)} chunks, size=300, overlap=50)")
    print("=" * 72)
    for i, chunk in enumerate(char_results, 1):
        print(f"\n── Chunk {i} ──")
        print(chunk)

    print("\n\n")
    print("=" * 72)
    print(f"HEADER-AWARE CHUNKING  ({len(header_results)} chunks)")
    print("=" * 72)
    for i, doc in enumerate(header_results, 1):
        path = " > ".join(doc.metadata.values()) if doc.metadata else "(root)"
        print(f"\n── Chunk {i}  [{path}] ──")
        print(doc.page_content)

    print("\n\nKey observation:")
    print("  Character chunks cut mid-paragraph — 'Do not cache validation' becomes")
    print("  stranded without its header context ('Authentication > Token Validation').")
    print("  Header chunks keep each section intact and carry metadata an agent can use")
    print("  to decide whether the chunk is even relevant before reading it.")


if __name__ == "__main__":
    main()
