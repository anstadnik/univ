foo = input('')
bar = input('')
quotes = chr(34) * 3
s = """foo = input('')
bar = input('')
quotes = chr(34) * 3
s = 42
s = s[:57] + quotes + s + quotes + s[59:]
s = s.replace(foo, bar, 1)#[::-1]
print(s, sep = '', end = '')
"""
s = s[:57] + quotes + s + quotes + s[59:]
s = s.replace(foo, bar, 1)#[::-1]
print(s, sep = '', end = '')
