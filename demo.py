"""Offline matching demonstration using fictional tracks only."""
import argparse
import json
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    id: str
    title: str
    artist: str
    duration_ms: int


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def plan(source, catalog, existing=()):
    known = set(existing)
    result = {"dry_run": True, "add_ids": [], "ambiguous": [], "unresolved": []}
    for track in source:
        hits = {candidate.id for candidate in catalog
                if normalize(track.title) == normalize(candidate.title)
                and normalize(track.artist) == normalize(candidate.artist)
                and track.duration_ms > 0 and candidate.duration_ms > 0
                and abs(track.duration_ms - candidate.duration_ms) <= 2000}
        if len(hits) != 1:
            result["ambiguous" if hits else "unresolved"].append(track.id)
            continue
        target = next(iter(hits))
        if target not in known:
            result["add_ids"].append(target)
            known.add(target)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", required=True)
    parser.parse_args()
    source = [Track("s1", "Example One", "Imaginary Band", 180000),
              Track("s2", "Example One", "Imaginary Band", 180000),
              Track("s3", "Example Two", "Imaginary Band", 200000),
              Track("s4", "Example Three", "Imaginary Band", 210000)]
    catalog = [Track("a1", "Example One", "Imaginary Band", 180100),
               Track("a2", "Example Two", "Imaginary Band", 200000),
               Track("a3", "Example Two", "Imaginary Band", 200500)]
    print(json.dumps(plan(source, catalog), indent=2))


if __name__ == "__main__":
    main()
