import csv
import json
import tempfile
import unittest
from pathlib import Path

from xquik_to_social_media_posts import convert, load_rows, normalize_row


class XquikConverterTest(unittest.TestCase):
    def test_loads_nested_api_response(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "tweets.json"
            source.write_text(
                json.dumps({"data": {"tweets": [{"id": "42", "text": "Hello"}]}}),
                encoding="utf-8",
            )

            self.assertEqual(load_rows(source), [{"id": "42", "text": "Hello"}])

    def test_loads_only_object_rows_from_jsonl(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "tweets.jsonl"
            source.write_text(
                '{"id": "1", "text": "First"}\n'
                '{"data": {"tweets": [{"id": "2", "text": "Second"}]}}\n'
                "42\n\n",
                encoding="utf-8",
            )

            self.assertEqual(
                load_rows(source),
                [{"id": "1", "text": "First"}, {"id": "2", "text": "Second"}],
            )

    def test_normalizes_nested_author_and_metrics(self):
        row = normalize_row(
            {
                "id": "7",
                "text": "Useful update",
                "like_count": "12",
                "retweet_count": "3",
                "author": {"username": "@analyst", "followers_count": "900"},
            },
            "X",
        )

        self.assertEqual(
            row,
            {
                "post_id": "7",
                "platform": "X",
                "username": "analyst",
                "post_text": "Useful update",
                "post_time": "",
                "likes": "12",
                "shares": "3",
                "followers": "900",
            },
        )

    def test_preserves_explicit_zero_metrics(self):
        row = normalize_row(
            {
                "id": "8",
                "text": "Zero is a real metric",
                "likes": 0,
                "like_count": 12,
                "shares": 0,
                "retweet_count": 3,
                "followers": 0,
                "author": {"followers_count": 900},
            },
            "X",
        )

        self.assertEqual(row["likes"], "0")
        self.assertEqual(row["shares"], "0")
        self.assertEqual(row["followers"], "0")

    def test_convert_skips_rows_without_text(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "tweets.json"
            output = Path(directory) / "converted.csv"
            source.write_text(
                json.dumps([{"id": "1", "text": "Included"}, {"id": "2"}]),
                encoding="utf-8",
            )

            self.assertEqual(convert(source, output, "X"), (1, 1))
            with output.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["post_text"], "Included")

    def test_converts_canonical_xquik_csv_headers(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "tweets.csv"
            output = Path(directory) / "converted.csv"
            source.write_text(
                "Tweet ID,Username,Tweet Text,Tweet Created At,Likes,Reposts,Followers\n"
                '42,analyst,"Useful, verified update",2026-07-19T12:00:00Z,0,3,900\n',
                encoding="utf-8",
            )

            self.assertEqual(convert(source, output, "X"), (1, 0))
            with output.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(
                rows,
                [
                    {
                        "post_id": "42",
                        "platform": "X",
                        "username": "analyst",
                        "post_text": "Useful, verified update",
                        "post_time": "2026-07-19T12:00:00Z",
                        "likes": "0",
                        "shares": "3",
                        "followers": "900",
                    }
                ],
            )


if __name__ == "__main__":
    unittest.main()
