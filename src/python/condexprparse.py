# coding=utf-8

from parser.condparse import ConditionParser
from parser.exprparse import ExpressionParser
from evtmanage import EventManager

class ConditionExpressionParser:

    def __init__(self):
        self.result = []
        self.cond_parser = ConditionParser()
        self.expr_parser = ExpressionParser([">=", "<=", ">", "<", "=", "<>"])

        self.cond_parser.add_and_operator(" and ")
        self.cond_parser.add_and_operator("&")
        self.cond_parser.add_or_operator(" or ")
        self.cond_parser.add_or_operator("|")

        self.expr_parser.add_function_token("count")
        self.expr_parser.add_function_token("size")
        self.expr_parser.add_function_token("speed")

        manager = EventManager()
        for k in manager.EVENT_LIST.keys():
            self.expr_parser.add_parameter_token(k)

    def parse(self, condexpr):
        self.result = self.cond_parser.parse_cond(condexpr)
        self.recursive_split(self.result)
        return self.result

    def recursive_split(self, recursive_list):
        if len(recursive_list) == 1:
            while (type(recursive_list[0]) is str) is False:
                recursive_list = recursive_list[0]
            recursive_list[0] = self.expr_parser.parse_expr(recursive_list[0])
        else:
            self.recursive_split(recursive_list[1])
            self.recursive_split(recursive_list[2])
