from exprparse import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--expr", type=str)
args = parser.parse_args()

real = ExpressionParser(expression=args.expr,
                        functions=["count", "size", "speed"],
                        parameters=["task.switch"],
                        operators=["<=", ">=", "=", ">", "<", "<>"])
real.parse_expr()