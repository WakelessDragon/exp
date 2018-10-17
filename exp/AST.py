from typing import Union

from exp.Operator import UnaryOperator, BinaryOperator, get_all_operator


class AST:

    def __init__(self, all_operator, tokens, depth=1):
        self.left = None
        self.right = None
        self.all_operator = all_operator
        self.depth = depth
        self.tks = tokens
        if tokens[-1] == ')' or tokens[-1] == '}':
            right_pair = tokens[-1]
            if right_pair == ')':
                left_pair = '('
            elif right_pair == '}':
                left_pair = '{'
            else:
                raise ValueError('invalid token ' + right_pair)
            left_bracket_idx = self.__find_matched_left(tokens, len(tokens) - 1, left_pair)
            assert left_bracket_idx is not None, 'un pair bracket' + right_pair
            tokens_before_bracket = tokens[:left_bracket_idx]
            oik_before_bracket = self.__op_idx_tk(tokens_before_bracket)
            if oik_before_bracket is not None:
                self.is_basal = False
                self.operator = oik_before_bracket[0]
                if oik_before_bracket[1] != 0:
                    self.left = AST(all_operator, tokens_before_bracket[0:oik_before_bracket[1]], depth + 1)
                self.right = AST(all_operator, tokens[left_bracket_idx:], depth + 1)
            else:
                tokens_in_bracket = tokens[1:-1]
                if right_pair == ')':
                    self.__init__(all_operator, tokens_in_bracket, depth)
                elif right_pair == '}':
                    self.tks = tokens_in_bracket
                    self.is_basal = True
                    self.operator = None
                    self.left = None
                    self.right = None
        else:
            oik = self.__op_idx_tk(tokens)
            if oik is not None:
                self.is_basal = False
                self.operator = oik[0]
                if oik[1] != 0:
                    self.left = AST(all_operator, tokens[0: oik[1]], depth + 1)
                self.right = AST(all_operator, tokens[oik[1] + 1:], depth + 1)
            else:
                self.is_basal = True
                self.operator = None
                self.left = None
                self.right = None

    def __find_matched_left(self, tokens, right_idx, left_char):
        rb_stk = []
        for idx in reversed(range(right_idx + 1)):
            tk = tokens[idx]
            if idx == right_idx or tk == rb_stk[-1]:
                rb_stk.append(tk)
            else:
                if tk == left_char:
                    rb_stk.pop()
                    if len(rb_stk) == 0:
                        return idx

    def __op_idx_tk(self, tokens):
        rst = None
        skip_to = len(tokens)
        for i in reversed(range(len(tokens))):
            if i > skip_to:
                continue
            tk = tokens[i]
            if tk == ')':
                left_bracket_idx = self.__find_matched_left(tokens, i, '(')
                assert left_bracket_idx is not None, 'un pair bracket )'
                skip_to = left_bracket_idx - 1
            elif tk == '}':
                left_bracket_idx = self.__find_matched_left(tokens, i, '{')
                assert left_bracket_idx is not None, 'un pair bracket }'
                skip_to = left_bracket_idx - 1
            for op in self.all_operator:  # type: Union[BinaryOperator, UnaryOperator]
                if op.mark == tk:
                    if rst is None:
                        rst = (op, i)
                    elif op.priority > rst[0].priority:
                        rst = (op, i)
                    break
        return rst

    def eval(self, env):
        if self.is_basal:
            key = ''.join(self.tks)
            return env.get(key, key)
        else:
            if isinstance(self.operator, UnaryOperator):
                right_eval = self.right.eval(env)
                return self.operator.apply(right_eval)
            elif isinstance(self.operator, BinaryOperator):
                left_eval = self.left.eval(env)
                right_eval = self.right.eval(env)
                return self.operator.apply(left_eval, right_eval)

    def __str__(self):
        pad = ''.ljust(self.depth * 4)
        return 'tks: %s, \n%soperator: %s, \n%sleft: %s, \n%sright: %s' \
               % (self.tks, pad, self.operator, pad, self.left, pad, self.right)
