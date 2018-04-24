import logging
from programytest.parser.pattern.matching.base import PatternMatcherBaseClass

class PatternMatcherBasicTests(PatternMatcherBaseClass):

    def test_single_word_match(self):
        self.add_pattern_to_graph(pattern="A", topic="X", that="Y", template="1")

        context = self.match_sentence("A", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

    def test_single_word_no_match(self):
        self.add_pattern_to_graph(pattern="A", topic="X", that="Y", template="1")

        context = self.match_sentence("B", topic="X", that="Y")
        self.assertIsNone(context)








