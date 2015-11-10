# coding=utf-8


class ConditionParser:
    """
    <BPF Program과 아무 관련이 없는 클래스>
    raw한 expr 인자를 그대로 받아서 context flow graph와 각 boolean expr에
    해당하는 expr을 반환해준다. 이 클래스를 통해 반환받은 expr들을 올바른 bpf 프로그램이
    작동하도록 파싱하기 위해선 ExpressionParser 클래스를 활용할 것.
    예시 input:
    "a & (c | d) & e"
    예시 output:
    [1, [1, ['a '], [2, ['c '], ['d']]], 'e ']

    예시 input2:
    "a & b & c | d & e | f | g"
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

    def add_and_operator(self, token):
        self.ops[token] = 1

    def add_or_operator(self, token):
        self.ops[token] = 2

    def parse_cond(self, condition):
        result = []
        expr_idx = 0
        last_op = -1
        while True:
            condition = condition[expr_idx:].lstrip()
            if condition[0] == '(':
                par_cnt = 0
                while True:
                    expr_idx += 1
                    if par_cnt == len(condition):  # 괄호 짝이 맞지 않고 문장이 끝남
                        print "Broken condition expression"
                        exit()

                    if condition[expr_idx] == '(':
                        par_cnt += 1
                    elif condition[expr_idx] == ')':
                        if par_cnt == 0:
                            min_list = self.find_operator(condition[expr_idx:])

                            if condition[expr_idx + 1: expr_idx + min_list[0]].lstrip() != "":
                                print "Broken condition expression"
                                exit()

                            if min_list[0] == -1:  # 해당 문장 뒤에 연산자가 없음
                                result.append(self.parse_cond(condition[1: expr_idx]))
                                return result

                            if last_op == -1:
                                if min_list[1] == 2:
                                    result = [2, self.parse_cond(condition[1: expr_idx]),
                                              self.parse_cond(condition[expr_idx + min_list[0] + min_list[2]:])]
                                    return result
                                else:
                                    last_op = 1
                                    result = [1, self.parse_cond(condition[1: expr_idx])]
                            else:
                                if min_list[1] == 2:
                                    result.append(self.parse_cond(condition[1: expr_idx]))
                                    result = [2, result,
                                              self.parse_cond(condition[expr_idx + min_list[0] + min_list[2]:])]
                                    return result
                                else:
                                    result.append(self.parse_cond(condition[1: expr_idx]))
                                    result = [1, result]

                            expr_idx = expr_idx + min_list[0] + min_list[2]
                            break

                        else:
                            par_cnt -= 1

            else:
                min_list = self.find_operator(condition)

                if min_list[0] == -1:  # 해당 문장 뒤에 연산자가 없음
                    result.append([condition])
                    return result

                if last_op == -1:
                    if min_list[1] == 2:
                        result = [2, [condition[:min_list[0]]], self.parse_cond(condition[min_list[0] + min_list[2]:])]
                        return result
                    else:
                        last_op = 1
                        result = [1, [condition[:min_list[0]]]]
                else:
                    if min_list[1] == 2:
                        result.append([condition[:min_list[0]]])
                        result = [2, result, self.parse_cond(condition[min_list[0] + min_list[2]:])]
                        return result
                    else:
                        result.append([condition[:min_list[0]]])
                        result = [1, result]

                expr_idx = min_list[0] + min_list[2]

    def find_operator(self, expression):
        """
        :param expression: 연산자가 출현하는 최초의 위치를 찾는다
        :return: [연산자가 출현하는 최초의 위치, 연산자의 타입, 연산자 문자열 자체]
        """

        min_idx = -1
        min_op_type = ""
        min_op_str_len = -1
        for k, v in self.ops.items():
            op_idx = expression.find(k)
            if op_idx != -1 and (min_idx > op_idx or min_idx == -1):
                min_idx = op_idx
                min_op_type = v
                min_op_str_len = len(k)

        return [min_idx, min_op_type, min_op_str_len]
