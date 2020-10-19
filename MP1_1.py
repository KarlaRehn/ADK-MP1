k = 0

def NumberOfOnes(v, i, j):
	global k
	if j == i and v[i] == 1:
		k += 1
		return 

	if IsZero(v, i, j):
		return

	else:
		indx = int((j+1-i)/2)
		u = v[:indx]
		w = v[indx:]
		NumberOfOnes(u, 0, len(u)-1)
		NumberOfOnes(w, 0, len(w)-1)


def IsZero(v, i, j):
	if 1 in v[i:j+1]:
		return False
	else:
		return True

v = [0,0,0,0,0,0,1,0,0,0,0]
NumberOfOnes(v, 0, len(v))

print(k)
