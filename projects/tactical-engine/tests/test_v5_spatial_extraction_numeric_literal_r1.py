"""R1-only differential checks; justification recorded before execution.

Technical difference: the new remediation A handoff contradicted the effective
numeric/literal caller branch. Historical 16 checks only covered single-slot
representation, not caller dispatch with two numeric literals. Do not run those
16 checks, historical 37/37 or wrapper 13/13 here. No transport/model/runtime.
"""
from pathlib import Path
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import v5_tactical_semantic_support_s2_spatial_v2 as final
import v5_tactical_semantic_support_s2_spatial_v2_extraction as extraction


def numeric(literal):
    return {'status': 'explicit', 'value': 'numeric', 'literal': literal,
            'selected_fragments': [literal]}


def uncertain(status):
    return {'status': status, 'value': status, 'literal': None,
            'selected_fragments': ['incerto'] if status == 'ambiguous' else []}


class NumericLiteralR1Tests(unittest.TestCase):
    def test_different_numeric_literals_return_same_before_dispatch(self):
        with mock.patch.object(final, '_quantifier_comparison',
                               wraps=final._quantifier_comparison) as helper:
            result = final._expected_comparison('quantifier', numeric('2'), numeric('3'))
        self.assertEqual(result, {'same'})
        helper.assert_not_called()

    def test_identical_numeric_literals_return_same_before_dispatch(self):
        with mock.patch.object(final, '_quantifier_comparison',
                               wraps=final._quantifier_comparison) as helper:
            result = final._expected_comparison('quantifier', numeric('2'), numeric('2'))
        self.assertEqual(result, {'same'})
        helper.assert_not_called()

    def test_numeric_with_different_value_dispatches_real_helper(self):
        other = {'status': 'explicit', 'value': 'many', 'literal': None,
                 'selected_fragments': ['molti']}
        for claim, evidence in ((numeric('2'), other), (other, numeric('3'))):
            with self.subTest(claim=claim['value'], evidence=evidence['value']):
                with mock.patch.object(final, '_quantifier_comparison',
                                       wraps=final._quantifier_comparison) as helper:
                    result = final._expected_comparison('quantifier', claim, evidence)
                self.assertEqual(result, {'different'})
                helper.assert_called_once_with(evidence['value'], claim['value'],
                                               evidence['literal'], claim['literal'])

    def test_unknown_ambiguous_precede_values_and_dispatch(self):
        cases = [(uncertain('unknown'), numeric('2'), 'unknown'),
                 (numeric('3'), uncertain('unknown'), 'unknown'),
                 (uncertain('ambiguous'), numeric('2'), 'ambiguous'),
                 (numeric('3'), uncertain('ambiguous'), 'ambiguous'),
                 (uncertain('unknown'), uncertain('ambiguous'), 'ambiguous'),
                 (uncertain('ambiguous'), uncertain('unknown'), 'ambiguous')]
        for claim, evidence, expected in cases:
            with self.subTest(claim=claim['status'], evidence=evidence['status']):
                with mock.patch.object(final, '_quantifier_comparison',
                                       wraps=final._quantifier_comparison) as helper:
                    result = final._expected_comparison('quantifier', claim, evidence)
                self.assertEqual(result, {expected})
                helper.assert_not_called()

    def test_corrected_handoff_describes_observed_caller_precedence(self):
        text = extraction.extraction_handoff_instructions()
        for instruction in (
            'dopo la precedenza degli stati, _expected_comparison confronta i value prima del dispatch specifico del quantifier',
            'Value uguali richiedono same: due value=numeric richiedono attualmente same anche con literal diversi',
            'Il confronto dei literal nel helper non prevale sul return anticipato del caller',
            'Questa e la semantica attuale del contratto versionato, non una regola di correttezza numerica generale',
            'Solo con value diversi si applicano le regole seguenti',
        ):
            self.assertIn(instruction, text)
        self.assertNotIn('salvo numeric con literal diversi che richiede different', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
