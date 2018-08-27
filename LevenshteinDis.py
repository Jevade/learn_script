def check_LD(s,t):
	m = len(s)
	n = len(t)
	if not m:
		return n
	if not n:
		return m
	m += 1
	n += 1
	matrix = [ 0 for i in range(m*n)]
    # init x axis
	for i in range(m):
		matrix[i] = i
    # init y axis
	for i in range(0,m*n,m):
		if i % m == 0:
			matrix[i] = i // m
	for i in range(1,m):
		for j in range(1,n):
			if s[i-1] == t[j-1]:
				cost = 0
			else:
				cost = 1
			matrix[j * m + i] = min(matrix[j * m + i - 1] + 1,matrix[(j - 1) * m + i ] + 1,matrix[(j - 1) * m + i - 1] + cost)
	return matrix[-1]

print(check_LD('12226662','12313'))


def max_subStr(s1,s2):
	if not s1 or not s2:
		return 0 
	m = len(s1) + 1
	n = len(s2) + 1
	matrix = [0 for n in range(m*n)]
	print(matrix)
	for i in range(1,m):
		for j in range(1,n):
			same = 1 if s1[i-1] == s2[j-1] else 0
			matrix[j * m + i] = max(matrix[j * m + i - 1],matrix[(j-1) * m + i],matrix[(j-1) * m + i-1] + same)
			
			for k in range(n):
				print(matrix[k*m:(k+1)*m])
			print(same)
			print('-'*20)
			
	return matrix[-1]


print(max_subStr('123233','12313'))



