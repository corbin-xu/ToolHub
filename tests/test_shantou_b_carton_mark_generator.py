import unittest
from pathlib import Path

from main.label.carton_mark_generator import (
    ShantouBCartonMarkGenerator,
    ShantouBValidationError,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = PROJECT_ROOT / "templates" / "shantou_b_carton_mark.pld"


class ShantouBCartonMarkGeneratorTests(unittest.TestCase):
    def make_generator(self) -> ShantouBCartonMarkGenerator:
        generator = ShantouBCartonMarkGenerator(str(TEMPLATE_PATH))
        self.assertTrue(generator.load_template())
        return generator

    def test_reads_maximum_lengths_from_template(self) -> None:
        generator = self.make_generator()

        pr_placeholder = generator._find_prefixed_numeric_placeholder("PR")
        epl_placeholder = generator._find_prefixed_numeric_placeholder("EPL")

        self.assertIsNotNone(pr_placeholder)
        self.assertIsNotNone(epl_placeholder)
        self.assertEqual(pr_placeholder[2], 20)
        self.assertEqual(epl_placeholder[2], 19)

    def test_shorter_values_replace_remaining_placeholder_with_nulls(self) -> None:
        generator = self.make_generator()
        pr_start, pr_end, _ = generator._find_prefixed_numeric_placeholder("PR")
        epl_start, epl_end, _ = generator._find_prefixed_numeric_placeholder("EPL")

        generator._replace_pr_field("需求单号", "PR1234567", 1)
        generator._replace_epl_field("EPL采购单号", "EPL1234567890", 1)

        self.assertEqual(
            bytes(generator.content[pr_start:pr_end]),
            b"PR1234567".ljust(pr_end - pr_start, b"\x00"),
        )
        self.assertEqual(
            bytes(generator.content[epl_start:epl_end]),
            b"EPL1234567890".ljust(epl_end - epl_start, b"\x00"),
        )

    def test_accepts_values_at_template_maximum_length(self) -> None:
        generator = self.make_generator()

        generator._replace_pr_field("需求单号", "PR12345678901234567890", 1)
        generator._replace_epl_field("EPL采购单号", "EPL1234567890123456789", 1)

    def test_empty_values_clear_the_whole_placeholder_with_nulls(self) -> None:
        generator = self.make_generator()
        pr_start, pr_end, _ = generator._find_prefixed_numeric_placeholder("PR")
        epl_start, epl_end, _ = generator._find_prefixed_numeric_placeholder("EPL")

        generator._replace_pr_field("需求单号", "", 1)
        generator._replace_epl_field("EPL采购单号", "", 1)

        self.assertEqual(
            bytes(generator.content[pr_start:pr_end]),
            b"\x00" * (pr_end - pr_start),
        )
        self.assertEqual(
            bytes(generator.content[epl_start:epl_end]),
            b"\x00" * (epl_end - epl_start),
        )

    def test_rejects_values_over_template_maximum_length(self) -> None:
        generator = self.make_generator()

        with self.assertRaises(ShantouBValidationError):
            generator._replace_pr_field(
                "需求单号", "PR123456789012345678901", 1
            )
        with self.assertRaises(ShantouBValidationError):
            generator._replace_epl_field(
                "EPL采购单号", "EPL12345678901234567890", 1
            )

    def test_rejects_non_numeric_suffix(self) -> None:
        generator = self.make_generator()

        with self.assertRaises(ShantouBValidationError):
            generator._replace_pr_field("需求单号", "PR123ABC", 1)
        with self.assertRaises(ShantouBValidationError):
            generator._replace_epl_field("EPL采购单号", "EPL123ABC", 1)


if __name__ == "__main__":
    unittest.main()
