from exprparse import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--expr", type=str)
args = parser.parse_args()

cond = ConditionParser()
cond.add_andOperator("and")
cond.add_andOperator("&")
cond.add_orOperator("or")
cond.add_orOperator("|")
result = cond.parse_cond(args.expr)

print result

real = ExpressionParser(operators=["<=", ">=", "=", ">", "<", "<>"])
real.add_functionToken("count")
real.add_functionToken("size")
real.add_parameterToken("task.switch")
real.add_parameterToken("memory.alloc")
result = real.parse_expr(args.expr)

print result