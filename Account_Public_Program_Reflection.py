#!/usr/bin/env python3
"""Static account-level inventory/reflection over public GitHub program files.

This tool does not execute scanned programs and does not prove consistency.
It classifies source text heuristically and keeps computed/verified/heuristic/
declared claims separate in the output.
"""
from __future__ import annotations
import base64, hashlib, json, os, re, sys, urllib.parse, urllib.request

OWNER = os.getenv("GITHUB_OWNER", "letsgo0226")
TOKEN = os.getenv("GITHUB_TOKEN", "")
INCLUDE_FORKS = os.getenv("INCLUDE_FORKS", "0") == "1"
EXTS = {".py",".sh",".c",".h",".cpp",".cc",".js",".ts",".java",".go",".rs",".rb",".pl",".lua",".hs",".ml"}
HEADERS = {"User-Agent":"account-program-reflection","Accept":"application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

def api(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def pages(url: str):
    out, p = [], 1
    while True:
        sep = "&" if "?" in url else "?"
        xs = api(f"{url}{sep}per_page=100&page={p}")
        out.extend(xs)
        if len(xs) < 100:
            return out
        p += 1

def is_program(path: str) -> bool:
    low = path.lower()
    return any(low.endswith(x) for x in EXTS)

RULES = {
    "godel": r"g[oö]del|gödel|int\.from_bytes|prime.{0,16}(factor|exponent)",
    "zeta_riemann": r"riemann|\bzeta\b|ζ|\beta\s*\(|eta.{0,16}series",
    "turing": r"turing|transition.{0,12}(table|function)|\btape\b|halting|\bdelta\b|δ",
    "omega_limit": r"\bomega\b|ω|colim|direct\s+limit|inverse\s+limit",
    "self_reference": r"sys\.argv\[0\]|__file__|quine|self[-_ ]?refer",
    "network": r"urllib|requests|api\.github|\bcurl\b|\bwget\b",
    "dynamic_exec": r"\bexec\s*\(|\beval\s*\(|subprocess|os\.system",
}

def tags(text: str):
    return sorted(k for k, pat in RULES.items() if re.search(pat, text, re.I | re.S))

def get_blob(repo: str, sha: str) -> str:
    obj = api(f"https://api.github.com/repos/{OWNER}/{repo}/git/blobs/{sha}")
    if obj.get("encoding") != "base64":
        return ""
    raw = base64.b64decode(obj.get("content", ""), validate=False)
    return raw.decode("utf-8", "replace")

def main():
    repos = pages(f"https://api.github.com/users/{urllib.parse.quote(OWNER)}/repos?type=owner&sort=full_name")
    repos = [r for r in repos if not r.get("private") and (INCLUDE_FORKS or not r.get("fork"))]
    repos.sort(key=lambda r: r["name"].lower())
    entries, tree_truncated, read_errors = [], [], []
    for r in repos:
        name, branch = r["name"], r.get("default_branch") or "main"
        try:
            tree = api(f"https://api.github.com/repos/{OWNER}/{urllib.parse.quote(name)}/git/trees/{urllib.parse.quote(branch, safe='')}?recursive=1")
        except Exception as e:
            read_errors.append({"repo":name,"stage":"tree","error":type(e).__name__})
            continue
        if tree.get("truncated"):
            tree_truncated.append(name)
        for x in tree.get("tree", []):
            if x.get("type") != "blob" or not is_program(x.get("path", "")):
                continue
            row = {"repo":name,"path":x["path"],"git_blob_sha":x["sha"],"size":x.get("size",0)}
            try:
                text = get_blob(name, x["sha"])
                row["heuristic_tags"] = tags(text)
                row["content_sha256"] = hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()
            except Exception as e:
                row["heuristic_tags"] = []
                row["read_error"] = type(e).__name__
            entries.append(row)
    entries.sort(key=lambda x:(x["repo"].lower(),x["path"].lower()))
    canonical = json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode()
    g = int.from_bytes(b"\x01" + canonical, "big")
    back = g.to_bytes((g.bit_length()+7)//8, "big")[1:]
    counts = {k:0 for k in RULES}
    for e in entries:
        for t in e.get("heuristic_tags", []):
            counts[t] += 1
    report = {
      "model":"ACCOUNT_PUBLIC_PROGRAM_REFLECTION_V1",
      "owner":OWNER,
      "scope":{"public":True,"include_forks":INCLUDE_FORKS,"execution_of_scanned_code":False},
      "computed":{"repositories":len(repos),"program_files":len(entries),"godel_manifest_bits":g.bit_length(),"tag_counts":counts},
      "verified":{"canonical_manifest_roundtrip":back==canonical},
      "heuristic":{"rules":RULES,"entries":entries},
      "declared":{"omega":"formal colim only","open":True,"final":False},
      "limitations":{"consistency_proved":False,"semantic_equivalence_proved":False,"tree_truncated":tree_truncated,"read_errors":read_errors}
    }
    json.dump(report, sys.stdout, ensure_ascii=False, separators=(",",":"))
    print()

if __name__ == "__main__":
    main()
