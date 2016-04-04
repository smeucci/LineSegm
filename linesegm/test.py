dic = {'a': 1, 'b': 3, '[1, 2]': -1}

best = min(dic, key=dic.get)
print best
best = best.replace('[', '').replace(']', '')
print best
x, y = best.split(',')
best = [int(x), int(y)]
print best
print dic[str(best)]
print float('-inf') > 0
