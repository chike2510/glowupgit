# Architecture

```mermaid
flowchart LR
  A[GitHub URL input] --> B[POST /api/glowup]
  B --> C[fetch_repo]
  C --> D[README + manifest + file tree]
  D --> E[generate_copy]
  E --> F[rewrite_readme]
  E --> G[Landing page payload]
  F --> H[README payload]
  G --> I[Frontend preview]
  H --> I
```

The API layer owns orchestration and validation. The agent package owns the three product capabilities, so each can be tested independently or swapped for a Strands/Bedrock implementation without changing the UI contract. The frontend remains a thin client: it submits one URL, renders explicit progress, then renders the output payload.
