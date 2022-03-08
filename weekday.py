import datetime
week = '9'
d1 = "2022-W" + str(int(week) - 1)
d2 = "2022-W" + week
r1 = datetime.datetime.strptime(d1 + '-6', "%Y-W%W-%w")
r1 = str(r1).split(' ')[0]
r2 = datetime.datetime.strptime(d2 + '-5', "%Y-W%W-%w")
r2 = str(r2).split(' ')[0]
print(r1)
print(r2)