import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.resetlearn import TemplateResetLearnNode
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient

class TemplateGraphResetLearnTests(TemplateGraphTestClient):

     def test_learnf_type1(self):
        template = ET.fromstring("""
			<template>
				<resetlearn />
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateResetLearnNode)
        self.assertEqual(0, len(ast.children[0].children))

     def test_learnf_type2(self):
        template = ET.fromstring("""
			<template>
				<resetlearn></resetlearn>
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateResetLearnNode)
        self.assertEqual(0, len(ast.children[0].children))

     def test_request_with_children(self):
        template = ET.fromstring("""
			<template>
				<resetlearn>Error</resetlearn>
			</template>
			""")
        with self.assertRaises(ParserException):
            ast = self._graph.parse_template_expression(template)
