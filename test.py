# -*- coding: utf-8 -*-

with open ('input.txt', 'r', encoding='utf-8') as fio:
    data = fio.readlines()

L=[]
hashed=[]
# hash student id
for line in data:
    row = line.split(' ')
    L.append(row[0])
    hashed.append((int(row[0]) *3011+1009)%1000)        # hash


for i in hashed:
    print(i)

print("===========")
S=set(hashed)
if len(S) == len(hashed):
    print("no duplicate")
else:
    print("has duplicate")
    print(f"S: {len(S)}, L: {len(hashed)}")


