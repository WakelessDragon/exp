from exp.AST import AST
from exp.Operator import get_all_operator
from exp.Tokenizer import Tokenizer


def run(exp, env):
    ao = get_all_operator(env)
    tokens = Tokenizer(ao).tokenizer(exp)
    return AST(ao, tokens).eval(env)


def get_ast(exp, env):
    ao = get_all_operator(env)
    tokens = Tokenizer(ao).tokenizer(exp)
    return AST(ao, tokens)
