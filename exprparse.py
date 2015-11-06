#-*- coding: utf-8 -*-

class ConditionParser:
    """
    <BPF Program과 아무 관련이 없는 클래스>
    raw한 expr 인자를 그대로 받아서 context flow graph와 각 boolean expr에
    해당하는 expr을 반환해준다. 이 클래스를 통해 반환받은 expr들을 올바른 bpf 프로그램이
    작동하도록 파싱하기 위해선 ExpressionParser 클래스를 활용할 것.
    """

    def __init__(self,
                 expression):
        self.expr = expression

    def parse_expr(self):
        print(self.expr)

class ExpressionParser:
    """
    'count(task.create) > 100' 와 같은 expr 자체를 BPF Program을 구동하기 위해
    파싱해주는 클래스이다.
    """

    def __init__(self,
                 expression,
                 functions,
                 parameters,
                 operators):
        self.expr = expression
        self.token = {}
        self.ops = operators

        """
        인자로 받은 토큰들을 분류한다.
        함수 타입이면 1, 파라미터 타입이면 2, 상수 타입이면 4로 분류
        """
        for new_token in functions:
            self.token[new_token] = 1
        for new_token in parameters:
            self.token[new_token] = 2

    def parse_expr(self):

        side_expr = self.splitExpression()
        result = [side_expr[0]]

        for side_expr_idx in range(1, 3):
            side_expr[side_expr_idx] = side_expr[side_expr_idx].lstrip()
            side_expr[side_expr_idx] = side_expr[side_expr_idx].rstrip()
            call_stack = []
            first_idx = 0
            last_idx = 0
            expected_token_type = 5 # 첫 토큰은 함수나 상수만 가능

            while True:
                #print result
                #print call_stack
                if last_idx != len(side_expr[side_expr_idx]) and expected_token_type == 0:
                    print "Unexpected token"
                    exit()
                elif last_idx == len(side_expr[side_expr_idx]) and expected_token_type != 0:
                    pass
                elif last_idx == len(side_expr[side_expr_idx]) and expected_token_type == 0:
                    result.append(call_stack)
                    break
                elif first_idx == last_idx or (side_expr[side_expr_idx][last_idx] != " " and side_expr[side_expr_idx][last_idx] != '(' and side_expr[side_expr_idx][last_idx] != ')'):
                    last_idx += 1
                    continue

                current_token = side_expr[side_expr_idx][first_idx:last_idx]

                try:
                    token_type = self.token[current_token]
                except:
                    try:
                        if int(current_token):
                            token_type = 4
                    except:
                        if first_idx == last_idx:
                            print "Token expected; Expression ends unexpectedly"
                        else:
                            print "Unexpected token \'" + current_token + "\'"
                        exit()

                if (expected_token_type & token_type) == 0:
                    print "Unexpected token type \'" + current_token +"\'"
                    exit()

                if token_type == 1:
                    # 토큰이 함수일 경우
                    brace_cnt = 1
                    while brace_cnt != 0:
                        if last_idx == len(side_expr[side_expr_idx]):
                            print "Token expected; Expression ends unexpectedly"
                            exit()

                        if side_expr[side_expr_idx][last_idx] != " " and side_expr[side_expr_idx][last_idx] != "(":
                            print "Expected \'(\'"
                            exit()

                        if side_expr[side_expr_idx][last_idx] == "(":
                            brace_cnt -= 1

                        last_idx += 1

                    call_stack.insert(0, current_token)
                    side_expr[side_expr_idx] = side_expr[side_expr_idx].replace(side_expr[side_expr_idx][last_idx:], side_expr[side_expr_idx][last_idx:].lstrip())
                    first_idx = last_idx
                    expected_token_type = 7 # 함수 뒤에는 모든 토큰 타입이 전부 올 수 있다
                else:
                    # 토큰이 파라미터나 상수일 경우
                    brace_cnt = len(call_stack)
                    while brace_cnt != 0:
                        if last_idx == len(side_expr[side_expr_idx]):
                            print "Token expected; Expression ends unexpectedly"
                            exit()

                        if side_expr[side_expr_idx][last_idx] != " " and side_expr[side_expr_idx][last_idx] != ")":
                            print "Expected \')\'"
                            exit()

                        if side_expr[side_expr_idx][last_idx] == ")":
                            brace_cnt -= 1

                        last_idx += 1

                    call_stack.insert(0, current_token)
                    side_expr[side_expr_idx] = side_expr[side_expr_idx].replace(side_expr[side_expr_idx][last_idx:], side_expr[side_expr_idx][last_idx:].lstrip())
                    first_idx = last_idx
                    expected_token_type = 0 # 파라미터나 상수는 콜스택의 top에 있어야만 한다

        return result

    def splitExpression(self):
        op_idx = -1
        result = []
        for ops_idx in range(0, len(self.ops)):
            op_idx = self.expr.find(self.ops[ops_idx])
            if op_idx != -1:
                result.append(self.ops[ops_idx])
                break

        if op_idx == -1:
            print "No operator in this expression \"" + self.expr + "\""
            exit()

        return result + [self.expr[0:op_idx], self.expr[op_idx + len(result[0]):]]
