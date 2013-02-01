from difflib import SequenceMatcher


class Base(object):

    def __init__(self, a, b, color=False):
        self.a, self.b = a, b

    @property
    def output(self):
        raise NotImplementedError()


class NoneDiffer(Base):

    @property
    def output(self):
        if self.b is None:
            return str(None)
        return '<' + str(None) + '>'


class BooleanDiffer(Base):

    @property
    def output(self):
        if self.a is self.b:
            return str(self.a)
        return '<' + str(self.a) + '>'


class IntegerDiffer(Base):

    @property
    def output(self):
        return StringDiffer(str(self.a), str(self.b)).output


class FloatDiffer(IntegerDiffer):
    pass


class LongDiffer(Base):
    pass


class ComplexDiffer(Base):
    pass


class StringDiffer(Base):

    highlight_start = '<'
    highlight_end = '>'

    def __init__(self, a, b):
        super(StringDiffer, self).__init__(a, b)
        self.matches = sorted(
            SequenceMatcher(
                a=self.a,
                b=self.b
            ).get_matching_blocks(),
            key=lambda m: m.a
        )
        self.matches = filter(lambda x: x.size > 0, self.matches)

    @property
    def output(self):
        return ''.join(self.get_diff_string_lists()[0])

    def get_diff_strings(self):
        return map(''.join, get_diff_string_lists())

    def get_diff_string_lists(self):
        a_diff_strings = []
        b_diff_strings = []
        a_last_end = 0
        b_last_end = 0
        for match in self.matches:
            a_diff_strings.append(self.a[a_last_end:match.a])
            a_last_end = match.a + match.size
            a_diff_strings.append(self.a[match.a:a_last_end])

            b_diff_strings.append(self.b[b_last_end:match.b])
            b_last_end = match.b + match.size
            b_diff_strings.append(self.b[match.b:b_last_end])

        try:
            first_match = self.matches[0]
        except IndexError:
            starts_with_match = False
            ends_with_match = False
        else:
            starts_with_match = first_match.a == 0 and first_match.b == 0
            last_match = self.matches[-1]
            ends_with_match = a_last_end == len(self.a) and b_last_end == len(self.b)

        if not ends_with_match:
            a_diff_strings.append(self.a[a_last_end:])
            b_diff_strings.append(self.b[b_last_end:])

        for index in range(0, len(a_diff_strings), 2):
            a_diff_strings[index] = self._highlight(a_diff_strings[index])
            b_diff_strings[index] = self._highlight(b_diff_strings[index])

        if starts_with_match:
            a_diff_strings = a_diff_strings[1:]
            b_diff_strings = b_diff_strings[1:]

        return a_diff_strings, b_diff_strings

    @classmethod
    def _highlight(self, string):
        return ''.join(
            [
                self.highlight_start,
                string,
                self.highlight_end
            ]
        )


class UnicodeDiffer(Base):
    pass


class TupleDiffer(Base):
    pass


class ListDiffer(Base):
    pass


class SetDiffer(Base):
    pass


class DictDiffer(Base):
    pass


class FunctionDiffer(Base):
    pass


class LambdaDiffer(Base):

    # XXX: This does not belong here. Just keeping it for refrence.
    # def isalambda(l):
    #   return isinstance(l, type(lambda: None)) and l.__name__ == '<lambda>'

    pass
