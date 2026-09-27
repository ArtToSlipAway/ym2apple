import unittest
from demo import Track, plan


class DemoTests(unittest.TestCase):
    def setUp(self):
        self.source = Track("s", "Example", "Imaginary Band", 180000)
        self.target = Track("a", "Example", "Imaginary Band", 181000)

    def test_duplicate_sources_produce_one_target(self):
        result = plan([self.source, self.source], [self.target])
        self.assertEqual(result["add_ids"], ["a"])

    def test_existing_target_is_not_added(self):
        self.assertEqual(plan([self.source], [self.target], ["a"])["add_ids"], [])

    def test_distinct_close_candidates_require_review(self):
        other = Track("b", "Example", "Imaginary Band", 180500)
        self.assertEqual(plan([self.source], [self.target, other])["ambiguous"], ["s"])

    def test_wrong_artist_or_duration_is_rejected(self):
        for target in [Track("b", "Example", "Other Band", 180000),
                       Track("b", "Example", "Imaginary Band", 190000),
                       Track("b", "Example", "Imaginary Band", 0)]:
            self.assertEqual(plan([self.source], [target])["unresolved"], ["s"])


if __name__ == "__main__":
    unittest.main()
