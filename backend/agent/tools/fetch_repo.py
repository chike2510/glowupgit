from __future__ import annotations
import os
import re
from typing import Any
import httpx


def _parse_repo(url: str) -> tuple[str, str]:
    match = re.match(r"https?://github\.com/([^/]+)/([^/#]+)", url.strip().rstrip("/"))
    if not match:
        raise ValueError("Enter a public GitHub repository URL.")
    return match.group(1), match.group(2).removesuffix(".git")


def fetch_repo(url: str) -> dict[str, Any]:
    owner, repo = _parse_repo(url)
    headers = {"Accept": "application/vnd.github+json"}
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    base = f"https://api.github.com/repos/{owner}/{repo}"
    with httpx.Client(timeout=15, headers=headers) as client:
        meta = client.get(base)
        if meta.status_code == 404:
            raise ValueError("That repository was not found or is not public.")
        meta.raise_for_status()
        info = meta.json()
        readme = client.get(f"{base}/readme", headers={**headers, "Accept": "application/vnd.github.raw+json"})
        readme_text = readme.text if readme.status_code == 200 else ""
        tree = client.get(f"{base}/contents")
        tree.raise_for_status()
        files = [item.get("name", "") for item in tree.json() if item.get("name")]
        manifest_name = next((name for name in ("package.json", "pyproject.toml", "Cargo.toml", "go.mod") if name in files), None)
        manifest = ""
        if manifest_name:
            manifest_response = client.get(f"{base}/contents/{manifest_name}", headers={**headers, "Accept": "application/vnd.github.raw+json"})
            manifest = manifest_response.text if manifest_response.status_code == 200 else ""
    return {"owner": owner, "repo": repo, "url": url, "description": info.get("description") or "", "stars": info.get("stargazers_count", 0), "language": info.get("language") or "", "readme": readme_text[:12000], "manifest_name": manifest_name, "manifest": manifest[:8000], "files": files[:30]}
