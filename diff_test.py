import diff
import unittest


class NoneAcceptanceTestCase(unittest.TestCase):

    def test_none_diff(self):
        bool_diff = diff.BooleanDiffer(None, False)
        self.assertEqual('<None>', bool_diff.output)

    def test_none_same(self):
        bool_diff = diff.BooleanDiffer(None, None)
        self.assertEqual('None', bool_diff.output)


class BooleanAcceptanceTestCase(unittest.TestCase):

    def test_bool_diff(self):
        bool_diff = diff.BooleanDiffer(True, False)
        self.assertEqual('<True>', bool_diff.output)

    def test_bool_same(self):
        bool_diff = diff.BooleanDiffer(False, False)
        self.assertEqual('False', bool_diff.output)


class IntegerDifferAcceptanceTestCase(unittest.TestCase):

    def test_integer_diff(self):
        integer_diff = diff.IntegerDiffer(1234567890, 1234557890)
        self.assertEqual('12345<6>7890', integer_diff.output)

    def test_integer_diff_beginning(self):
        integer_diff = diff.IntegerDiffer(1234567890, 1234567890)
        self.assertEqual('1234567890', integer_diff.output)

    def test_integer_diff_len(self):
        integer_diff = diff.IntegerDiffer(1234567890, 123456)
        self.assertEqual('123456<7890>', integer_diff.output)

        integer_diff = diff.IntegerDiffer(123456, 1234567890)
        self.assertEqual('123456<>', integer_diff.output)


class FloatDifferAcceptanceTestCase(unittest.TestCase):

    def test_float_diff(self):
        float_diff = diff.FloatDiffer(3.14529, 3.24529)
        self.assertEqual('3.<1>4529', float_diff.output)


class LongDifferAcceptanceTestCase(unittest.TestCase):

    def test_long_diff(self):
        long_diff = diff.LongDiffer(1234567890L, 12345L)
        self.assertEqual('12345<67890>L', long_diff.output)


class StringAcceptanceTestCase(unittest.TestCase):

    def assert_diff_strings_are(self, a, b, expected_a_diff_string, expected_b_diff_string):
        string_differ = diff.StringDiffer(a, b)
        a_diff_string, b_diff_string = string_differ.diff_strings
        self.assertEqual(a_diff_string, expected_a_diff_string)
        self.assertEqual(b_diff_string, expected_b_diff_string)

    def test_string_diff(self):
        self.assert_diff_strings_are(
            'this is the old string', 'this is the new string',
            'this is the <old> string', 'this is the <new> string'
        )

    def test_string_diff_beginning(self):
        self.assert_diff_strings_are(
            'this is the old string', 'kess is the old string',
            '<thi>s is the old string', '<kes>s is the old string'
        )

    def test_string_diff_end(self):
        self.assert_diff_strings_are(
            'this is the old string', 'this is the old strina',
            'this is the old strin<g>', 'this is the old strin<a>'
        )

    def test_string_same(self):
        self.assert_diff_strings_are(
            'this is the old string', 'this is the old string',
            'this is the old string', 'this is the old string'
        )

    def test_potential_duplicated_matching(self):
        self.assert_diff_strings_are(
            'matchematcher', 'matcher',
            '<matche>matcher', '<>matcher'
        )
        self.assert_diff_strings_are(
            'karsbarscars', 'iarsoarspars',
            '<k>ars<b>ars<c>ars', '<i>ars<o>ars<p>ars'
        )
        self.assert_diff_strings_are(
            'marscarsbars', 'carsbarsmars',
            '<mars>carsbars<>', '<>carsbars<mars>'
        )

    def test_always_takes_longer_match(self):
        # difflib will always prefer the longest available matches
        # not necessarily those that produce the smallest diffs.
        self.assert_diff_strings_are(
            'marscarsbars', 'marsbarscars',
            'm<>arscars<bars>', 'm<arsb>arscars<>'
        )

    def test_string_diff_len(self):
        self.assert_diff_strings_are(
            'this is the old string', 'this is the old',
            'this is the old< string>', 'this is the old<>'
        )
        self.assert_diff_strings_are(
            'this is the old string', 'this is the old strings',
            'this is the old string<>', 'this is the old string<s>'
        )

    def test_string_newline(self):
        self.assert_diff_strings_are(
            'this is \nthe old string', 'this is the old string',
            'this is <\n>the old string', 'this is <>the old string'
        )

    def test_string_multiple_diff(self):
        self.assert_diff_strings_are(
            'this is the old string', 'this old the is string',
            'this <is> the <old> string', 'this <old> the <is> string'
        )

    def test_string_long_diff(self):
        self.assert_diff_strings_are(
            'this is the old string', 'this is abcd-fg old string',
            'this is <the> old string', 'this is <abcd-fg> old string'
        )
        self.assert_diff_strings_are(
            'this is the old string', 'this is abcdefg old string',
            'this is <th>e<> old string', 'this is <abcd>e<fg> old string'
        )

    def test_string_empty(self):
        self.assert_diff_strings_are(
            'this is the old string', '',
            '<this is the old string>', '<>'
        )

    def test_string_contains_highlight_markers(self):
        self.assert_diff_strings_are(
            'this is >< old string', 'this is the old string',
            'this is <><> old string', 'this is <the> old string'
        )


if __name__ == '__main__':
    unittest.main()
