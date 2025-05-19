#!/usr/bin/env python3

"""
gaze.py
====================
Dump stargazer profile details to CSV.

Example
-------
$ .venv/bin/python stargazers_to_csv.py instantdb instant stargazers.csv --token $GITHUB_TOKEN

Columns
-------
first,last,full,location,followers,link
"""

import argparse
import csv
import os
import re
import sys
from typing import Tuple, Optional, Dict, List

import requests

API_ROOT = "https://api.github.com"
PER_PAGE = 100  # GitHub maximum


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export GitHub stargazers to CSV.")
    p.add_argument("owner", help="Repo owner/org (e.g. instantdb)")
    p.add_argument("repo", help="Repo name (e.g. instant)")
    p.add_argument("outfile", help="CSV output path")
    p.add_argument(
        "--token",
        help="GitHub personal-access token (or set GITHUB_TOKEN env var)",
        default=os.getenv("GITHUB_TOKEN"),
    )
    return p.parse_args()


def gh_request(url: str, token: Optional[str]) -> requests.Response:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return r


def split_name(full: Optional[str]) -> Tuple[str, str]:
    if not full:
        return "", ""
    parts = re.split(r"\s+", full.strip(), maxsplit=1)
    return (parts[0], parts[1] if len(parts) > 1 else "")


def get_stargazer_logins(owner: str, repo: str, token: Optional[str]) -> List[str]:
    url = f"{API_ROOT}/repos/{owner}/{repo}/stargazers?per_page={PER_PAGE}"
    logins: List[str] = []
    while url:
        print(f"Fetching logins at {url}")
        resp = gh_request(url, token)
        logins += [u["login"] for u in resp.json()]
        url = resp.links.get("next", {}).get("url")
    return logins


def get_user_data(login: str, token: Optional[str]) -> Dict:
    url = f"{API_ROOT}/users/{login}"
    print(f"Fetching from {url}")
    resp = gh_request(url, token)
    data = resp.json()
    first, last = split_name(data.get("name"))
    return {
        "first": first,
        "last": last,
        "full": data.get("name") or "",
        "location": data.get("location") or "",
        "followers": data.get("followers") or 0,
        "link": data.get("blog") or data.get("html_url") or "",
        "email": data.get("email") or "",
    }


def main() -> None:
    args = parse_args()
    if not args.token:
        sys.exit("❌  Provide a GitHub token via --token or GITHUB_TOKEN env var.")

    logins = get_stargazer_logins(args.owner, args.repo, args.token)
    print(f"✨ Found {len(logins)} stargazers – fetching profiles…")

    sample = logins[:2000]
    with open(args.outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "first", "last", "full", "location", "followers", "link", "email"
        ])
        writer.writeheader()
        for login in sample:
            row = get_user_data(login, args.token)
            writer.writerow(row)

    print(f"✅  Done! CSV saved to {args.outfile}")


if __name__ == "__main__":
    main()

