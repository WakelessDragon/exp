from exp import run, get_ast

env = {'a': {'b': [{'c': '2'}]}}
assert run('a.b.0.c == (1+(2*(4/4))-1) & (!(1>2))', env), "assert failure"
assert get_ast('a.b.0.c == a.b.0.c & (!({a|b+c-d&f/f%4} == {a|b+c-d&f/f%5}) & (1==1))', env).eval(env), "assert failure"
assert run('a.b.0.c+5+5-5 == a.b.0.c+5*2/2 & (!(1>2))', env), "assert failure"