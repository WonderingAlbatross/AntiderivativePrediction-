import random
binary = ["+","-","*","/","^"]
binary_weight = [20,10,20,15,3]
total_binary_weight = sum(binary_weight) 
unary = ["x","1","K","Sqrt[","Exp[","Log[","Sin[","Cos[","Tan[","Erf["]
unary_weight = [40,30,20,10,5,5,5,5,2,1]
total_unary_weight =  sum(unary_weight)
binary_rate = 0.3
new_const_rate = 0.3
max_const_num = 0

const_token = 0
def create(level):
	global const_token 
	if not level:
		return "1"
	else:
		if random.random()<binary_rate:
			k = total_binary_weight * random.random()
			i = 0
			k -= binary_weight[i]
			while(k>=0):	
				i += 1
				k -= binary_weight[i]
			s = binary[i]
			e1 = create(level-1)
			e2 = create(level-1)
			if e1 == "1" and e2 == "1":
				return "1"
			elif e1 == "1" and s == "*":
				return e2
			elif e2 == "1" and s in ("*","/"):
				return e1
			ans = "(" + e1 + ")" + s + "(" + e2 + ")"
			if ans in ("((x)+(x))","((x)-(x))","((x)/(x))"):
				return "1"

			return "(" + e1 + ")" + s + "(" + e2 + ")"


		else:
			k = total_unary_weight * random.random()
			i = 0
			k -= unary_weight[i]
			while(k>=0):	
				i += 1
				k -= unary_weight[i]
			s = unary[i]
			if i >= 3:
				if level == 1:
					return s + 	"x]"
				else: 
					e = create(level-1)
					if e != "1":
						return s + 	e + "]"
					else:
						return "1"
			elif i == 2:
				if not max_const_num:
					return "1"
				if not const_token:
					const_token = 1
					return "K0"
				elif const_token<max_const_num-1 and random.random()<new_const_rate:
					const_token += 1
				return "K"+str(const_token)
			else: 
				return s


print(create(6))