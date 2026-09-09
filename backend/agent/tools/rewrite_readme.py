from __future__ import annotations
from typing import Any


def rewrite_readme(repo: dict[str, Any], copy: dict[str, Any]) -> str:
    return f"""# {copy['title']}\n\n{copy['value_prop']}.\n\n## Why it exists\n\n{copy['body']}\n\n## Install\n\n```bash\n{copy['install_command']}\n```\n\n## Why star this repo\n\n{copy['why_star']}\n\n## Project shape\n\n- {repo.get('manifest_name') or 'README.md'}\n- {len(repo.get('files', []))} top-level files detected\n- Primary language: {repo.get('language') or 'not specified'}\n"""
