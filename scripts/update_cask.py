#!/usr/bin/env python3
"""Point Casks/conn.rb at the newest published Conn release. Standard library only.

Conn's releases are marked as previews, which GitHub's "latest release" skips, so this takes the
newest published, non-draft release. The checksum comes from that release's own SHA256SUMS.

  update_cask.py            rewrite the cask if a newer release exists
  CONN_REPO=owner/name      the application's repository, if it has moved
"""
import json, os, pathlib, re, sys, urllib.request

REPO = os.environ.get("CONN_REPO", "eggplantiny/conn")
CASK = pathlib.Path(__file__).resolve().parent.parent / "Casks" / "conn.rb"

def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "conn-homebrew-tap", "Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url: request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response: return response.read()

def main() -> int:
    releases = json.loads(get(f"https://api.github.com/repos/{REPO}/releases?per_page=20"))
    release = next((r for r in releases if not r["draft"] and re.fullmatch(r"v\d+\.\d+\.\d+", r["tag_name"])), None)
    if release is None: print("no published release found", file=sys.stderr); return 1
    version = release["tag_name"][1:]
    asset = f"conn-v{version}-aarch64-apple-darwin-desktop.dmg"
    sums = get(f"https://github.com/{REPO}/releases/download/v{version}/SHA256SUMS").decode()
    digest = next((line.split()[0] for line in sums.splitlines() if line.endswith(f" {asset}")), None)
    if not digest or not re.fullmatch(r"[0-9a-f]{64}", digest): print(f"{asset} is not listed in SHA256SUMS", file=sys.stderr); return 1
    text = CASK.read_text()
    updated = re.sub(r'(?m)^  version "[^"]+"$', f'  version "{version}"', text, count=1)
    updated = re.sub(r'(?m)^  sha256 "[0-9a-f]{64}"$', f'  sha256 "{digest}"', updated, count=1)
    if updated == text: print(f"cask already at {version}"); return 0
    CASK.write_text(updated); print(f"cask updated to {version}"); return 0

if __name__ == "__main__": raise SystemExit(main())
