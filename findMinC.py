import re
a="adefegfksdfkessefea"
ac=[chr(i) for i in range(int('0x21', 16), int('0x7f', 16))]


c=min([(re.search(c, a).span()[0], c) for c in ac if a.count(c)==1])[1]
#c=[(re.search(str(aci),a).span()[0],aci) for aci in ac]
print(c)
def fit(i):
	if i==0:
		return 1
	elif i==1:
		return 2
	elif i==2:
		return 4
	else:
		return fit(i-1)+fit(i-2)+fit(i-3)
print(fit(10))
a=input("shuri:")
index=1
while a!="q":
	index=index+1
	if index>10:
		break
	a=input("shuri:")
	print(a)
print(a)
