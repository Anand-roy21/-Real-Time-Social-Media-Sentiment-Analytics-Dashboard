"""Convert Xquik tweet exports into the Power BI source CSV shape."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

FIELDNAMES = [
    "post_id",
    "platform",
    "username",
    "post_text",
    "post_time",
    "likes",
    "shares",
    "followers",
]


def as_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def as_int(value: object) -> int:
    try:
        return max(0, int(float(as_text(value) or "0")))
    except (OverflowError, ValueError):
        return 0


def first_text(row: dict[str, Any], names: tuple[str, ...]) -> str:
    for name in names:
        value = as_text(row.get(name))
        if value:
            return value
    return ""


def first_value(row: dict[str, Any], names: tuple[str, ...]) -> object:
    for name in names:
        value = row.get(name)
        if as_text(value):
            return value
    return None


def nested_author(row: dict[str, Any]) -> dict[str, Any]:
    author = row.get("author") or row.get("user")
    return author if isinstance(author, dict) else {}


def extract_rows(data: object) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        for key in ("tweets", "data", "results", "items"):
            if key in data:
                rows = extract_rows(data[key])
                if rows:
                    return rows
        return [data]
    return []


def load_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return list(csv.DictReader(handle))
    if suffix in {".jsonl", ".ndjson"}:
        rows: list[dict[str, Any]] = []
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    value = json.loads(line)
                    rows.extend(extract_rows(value))
        return rows

    return extract_rows(json.loads(path.read_text(encoding="utf-8")))


def normalize_row(row: dict[str, Any], platform: str) -> dict[str, str] | None:
    author = nested_author(row)
    text = first_text(
        row,
        ("post_text", "Tweet Text", "tweetText", "text", "full_text", "content", "body"),
    )
    if not text:
        return None

    username = (
        first_text(
            row,
            ("username", "Username", "xUsername", "screen_name", "handle", "author_username"),
        )
        or first_text(author, ("username", "screen_name", "handle", "name"))
        or "xquik_user"
    )
    post_id = first_text(
        row,
        ("post_id", "Tweet ID", "tweetId", "id", "id_str", "tweet_id", "Tweet URL", "tweetUrl", "url"),
    )
    created_at = first_text(
        row,
        ("post_time", "Tweet Created At", "tweetCreatedAt", "created_at", "createdAt", "timestamp", "date"),
    )
    likes = as_int(first_value(row, ("likes", "Likes", "likeCount", "like_count", "favorite_count")))
    shares = as_int(
        first_value(row, ("shares", "Reposts", "repostCount", "retweet_count", "retweets"))
    )
    followers_value = first_value(
        row,
        ("followers", "Followers", "xFollowersCount", "followers_count"),
    )
    if followers_value is None:
        followers_value = first_value(author, ("followers", "followers_count"))
    followers = as_int(followers_value)

    return {
        "post_id": post_id,
        "platform": platform,
        "username": username.lstrip("@"),
        "post_text": text,
        "post_time": created_at,
        "likes": str(likes),
        "shares": str(shares),
        "followers": str(followers),
    }


def convert(input_path: Path, output_path: Path, platform: str) -> tuple[int, int]:
    rows = load_rows(input_path)
    converted = [row for row in (normalize_row(row, platform) for row in rows) if row]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(converted)
    return len(converted), len(rows) - len(converted)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a Xquik CSV, JSON, JSONL, or NDJSON tweet export into social_media_posts_20000.csv columns."
    )
    parser.add_argument("input", type=Path, help="Path to the Xquik tweet export")
    parser.add_argument("output", type=Path, help="Destination CSV path for Power BI or MySQL import")
    parser.add_argument("--platform", default="X", help="Platform value to write for converted rows")
    args = parser.parse_args()

    converted, skipped = convert(args.input, args.output, args.platform)
    print(f"Converted {converted} rows to {args.output}. Skipped {skipped} rows without text.")


if __name__ == "__main__":
    main()
