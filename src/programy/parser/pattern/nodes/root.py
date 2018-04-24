"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.parser.exceptions import ParserException

from programy.parser.pattern.matcher import Match
from programy.parser.pattern.nodes.base import PatternNode


class PatternRootNode(PatternNode):

    def __init__(self):
        PatternNode.__init__(self)

    def is_root(self):
        return True

    def can_add(self, new_node: PatternNode):
        if new_node.is_root():
            raise ParserException("Cannot add root node to existing root node")
        if new_node.is_topic():
            raise ParserException("Cannot add topic node to root node")
        if new_node.is_that():
            raise ParserException("Cannot add that node to root node")
        if new_node.is_template():
            raise ParserException("Cannot add template node to root node")

    def equivalent(self, other: PatternNode)->bool:
        if other.is_root():
            return True
        return False

    def to_string(self, verbose: bool = True)->str:
        if verbose is True:
            return "ROOT [%s]" % self._child_count(verbose)
        return "ROOT "

    def match(self, client_context, context, words):
        return self.consume(client_context, context, words, 0, Match.WORD, 0)
