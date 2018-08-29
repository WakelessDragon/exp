from exp import run

print(run('!(a.b.0.c > 110)', {'a': {'b': [{'c': '12'}]}}))