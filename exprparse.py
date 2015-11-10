#-*- coding: utf-8 -*-

class ConditionParser:
    """
    <BPF Program과 아무 관련이 없는 클래스>
    raw한 expr 인자를 그대로 받아서 context flow graph와 각 boolean expr에
    해당하는 expr을 반환해준다. 이 클래스를 통해 반환받은 expr들을 올바른 bpf 프로그램이
    작동하도록 파싱하기 위해선 ExpressionParser 클래스를 활용할 것.
    예시 input:
    "count(task.switch) > 100 and (size(memory.alloc) > 20 or count(memory.alloc) < 50) and size(task.switch) < 30"
    예시 output:
    [1, [1, "count(task.switch) > 100", [2, "size(memory.alloc) > 20", "count(memory.alloc) < 50"], "size(task.switch) < 30"]

    예시 input2:
    a & b & c | d & e | f | g
    예시 output2:
    [2, [1, [1, ['a '], ['b ']], ['c ']], [2, [1, ['d '], ['e ']], [2, ['f '], ['g']]]]
    """

    def __init__(self):
        self.expr = ""
        self.ops = {}

        """
        인자로 받은 연산자들을 분류한다.
        AND 타입이면 1, OR 타입이면 2
        """
    def add_andOperator(self, token):
        self.ops[token] = 1

    def add_orOperator(self, token):
        self.ops[token] = 2

    def parse_cond(self, condition):
        result = []
        expr_idx = 0
        last_op = -1
        while True:
            condition = condition[expr_idx:].lstrip()
            if (condition[0] == '('):
                print 1
            else:
                min = -1
                min_op_type = ""
                min_op_str = ""
                for k, v in self.ops.items():
                    op_idx = condition.find(k)
                    if op_idx != -1 and (min > op_idx or min == -1):
                        min = op_idx
                        min_op_type = v
                        min_op_str = k

                if min == -1: # 해당 문장 뒤에 연산자가 없음
                    result.append(condition)
                    return result

                if last_op == -1:
                    if min_op_type == 2:
                        result = [2, [condition[:min]], self.parse_cond(condition[min + len(min_op_str):])]
                        return result
                    else:
                        last_op = 1
                        result = [1, [condition[:min]]]
                else:
                    if min_op_type == 2:
                        result.append([condition[:min]])
                        result = [2, result, self.parse_cond(condition[min + len(min_op_str):])]
                        return result
                    else:
                        result.append([condition[:min]])
                        result = [1, result]

                expr_idx = min + len(min_op_str)




class ExpressionParser:
    """
    'count(task.create) > 100' 와 같은 expr 자체를 BPF Program을 구동하기 위해
    파싱해주는 클래스이다.
    """

    def __init__(self,
                 operators):
        self.token = {}
        self.ops = operators

        """
        인자로 받은 토큰들을 분류한다.
        함수 타입이면 1, 파라미터 타입이면 2, 상수 타입이면 4로 분류
        """
    def add_functionToken(self, token):
        self.token[token] = 1

    def add_parameterToken(self, token):
        self.token[token] = 2

    def parse_expr(self, expression):
        side_expr = self.splitExpression(expression)
        result = [side_expr[0]]

        for side_expr_idx in range(1, 3):
            side_expr[side_expr_idx] = side_expr[side_expr_idx].lstrip().rstrip()
            call_stack = []
            first_idx = 0
            last_idx = 0
            expected_token_type = 5 # 첫 토큰은 함수나 상수만 가능

            while True:
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

    def splitExpression(self, expression):
        op_idx = -1
        result = []
        for ops_idx in range(0, len(self.ops)):
            op_idx = expression.find(self.ops[ops_idx])
            if op_idx != -1:
                result.append(self.ops[ops_idx])
                break

        if op_idx == -1:
            print "No operator in this expression \"" + expression + "\""
            exit()

        return result + [expression[0:op_idx], expression[op_idx + len(result[0]):]]