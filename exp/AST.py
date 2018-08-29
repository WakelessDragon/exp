from exp.Operator import UnaryOperator, BinaryOperator, get_all_operator


class AST:

    def __init__(self, all_operator, tokens, depth=1):
        self.all_operator = all_operator
        self.depth = depth
        self.tks = tokens
        if tokens[-1] == ')':
            left_bracket_idx = self.__find_matched_left(tokens, len(tokens)-1, '(')
            assert left_bracket_idx is not None, 'un binate bracket'
            tokens_before_bracket = tokens[:left_bracket_idx]
            oik_before_bracket = self.__op_idx_tk(tokens_before_bracket)
            if oik_before_bracket is not None:
                self.is_basal = False
                self.operator = oik_before_bracket[0]
                if oik_before_bracket[1] != 0:
                    self.left = AST(all_operator, tokens_before_bracket[0:oik_before_bracket[1]], depth+1)
                self.right = AST(all_operator, tokens[left_bracket_idx:], depth+1)
            else:
                tokens_in_bracket = tokens[1:-1]
                self.__init__(all_operator, tokens_in_bracket, depth)
        else:
            oik = self.__op_idx_tk(tokens)
            if oik is not None:
                self.is_basal = False
                self.operator = oik[0]
                if oik[1] != 0:
                    self.left = AST(all_operator, tokens[0: oik[1]], depth+1)
                self.right = AST(all_operator, tokens[oik[1]+1:], depth+1)
            else:
                self.is_basal = True
                self.operator = None
                self.left = None
                self.right = None

    def __find_matched_left(self, tokens, right_idx, left_char):
        rb_stk = []
        for idx in reversed(range(right_idx+1)):
            tk = tokens[idx]
            if idx == right_idx or tk == rb_stk[-1]:
                rb_stk.append(tk)
            else:
                if tk == left_char:
                    rb_stk.pop()
                    if len(rb_stk) == 0:
                        return idx

    def __op_idx_tk(self, tokens):
        for i in reversed(range(len(tokens))):
            tk = tokens[i]
            for op in self.all_operator:
                if op.mark == tk:
                    return op, i

    def eval(self, env):
        if self.is_basal:
            key = self.tks[0]
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
        pad = ''.ljust(self.depth*4)
        return 'tks: %s, \n%soperator: %s, \n%sleft: %s, \n%sright: %s' \
               % (self.tks, pad, self.operator, pad, self.left, pad, self.right)