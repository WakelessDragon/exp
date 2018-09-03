from exp import run, get_ast

env = {'a': {'b': [{'c': '2'}]}}
print(run('a.b.0.c == (1+(2*(4/4))-1) & (!(1>2))', env))
print(get_ast('a.b.0.c == ({a|b+c-d&f/f%4} & (1==1))', env).eval(env))