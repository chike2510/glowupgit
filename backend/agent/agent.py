"""Agent boundary. generate_copy() runs a Strands agent against Bedrock by default;
it only drops to a deterministic fallback if the call fails or the agent is explicitly
disabled (GLOWUPGIT_DISABLE_AGENT=1), so local dev works without AWS credentials."""
from .tools.fetch_repo import fetch_repo
from .tools.generate_copy import generate_copy
from .tools.rewrite_readme import rewrite_readme


def run_glowup(url: str) -> dict:
    repo = fetch_repo(url)
    copy = generate_copy(repo)
    readme = rewrite_readme(repo, copy)
    return {"repo": repo, "copy": copy, "readme": readme}
