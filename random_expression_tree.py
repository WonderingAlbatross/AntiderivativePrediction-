import random
element = ["+","*","^","-","/","Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf","X","1"]

weight = [10,20,1,10,10,3,5,3,3,3,1,1,1,10,20]
level = {"+": 5, "*": 5, "^": 20, "-": 1, "/": 3, "Sqrt": 15, "Exp": 10, "Log": 10, "Sin": 5, "Cos": 5, "ArcSin": 25, "ArcTan": 25, "Erf": 25}
inverse = {"-":"-","/":"/","Exp":"Log","Log":"Exp","Sin":"ArcSin"}


new_term_rate_for_abelian_operators = 1-1/2
non_const_exp_rate = 0.2
non_x_rate_for_complicated_expressions = 0.9
max_level = 50




class expression_tree:
	def __init__(self,lv = 0, expression = "",forbid = []):
		self.level = lv
		self.next = []
		self.expression = ""
		if expression:
			self.expression = expression
		else:
			while not self.expression or self.expression in forbid:
				if lv > max_level:
					self.expression = random.choices(element[-2:],weight[-2:])[0]
				else:
					self.expression = random.choices(element,weight)[0]
		self.generate_next(self.expression)

	def generate_next(self,expression):
		if expression in ("+","*"):
			self.next = [expression_tree(lv = level[expression]+self.level,forbid = [expression])]
			self.next.append(expression_tree(lv = level[expression]+self.level,forbid = [expression]))
			while(random.random()<new_term_rate_for_abelian_operators):
				self.next.append(expression_tree(lv = level[expression]+self.level,forbid = [expression]))
		elif expression == "^":
			if random.random()>non_const_exp_rate:
				self.next = [expression_tree(lv = level[expression]+self.level),expression_tree(lv = self.level,expression = "K")]
			else:
				self.next = [expression_tree(lv = level[expression]+self.level),expression_tree(lv = level[expression]+self.level)]
		elif expression in ("-","/","Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf"):
			self.expression = ""
			while expression in ("-","/","Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf"):
				self.level += level[expression]
				self.expression += "," + expression
				if self.level > max_level:
					expression = "X"
				elif expression in ("Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf") and random.random()>non_x_rate_for_complicated_expressions:
					expression = "X"
				else:
					expression = random.choices(element,weight)[0]
			self.expression = self.simplify(self.expression)
			self.next = [expression_tree(lv = self.level,expression = expression)]
	def simplify(self,expression):
		#["+","*","^","-","/","Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf"]
		e = expression[1:].split(",")
		change = True
		while change:
			change = False
			for i in range(len(e)-1):
				if e[i+1]=="-":
					if e[i] in ("Sin","ArcSin","ArcSin","Arctan","Erf"):
						e[i] , e[i+1] = e[i+1] , e[i]
						change = True
						break
					if e[i] == "Cos":
						e.pop(i+1)
						change = True
						break
				if (e[i],e[i+1]) in (("-","-"),("/","/"),("Sin","ArcSin"),("ArcSin","Sin"),("Exp","Log"),("Log","Exp")):
					e.pop(i)
					e.pop(i)
					change = True
					break
				if (e[i],e[i+1]) == ("/","Exp"):
					e[i],e[i+1] = "Exp" , "-"
					change = True
					break
				if (e[i],e[i+1]) == ("Log","/"):
					e[i],e[i+1] = "-" , "Log"
					change = True
					break	

		return ",".join(e)
		





def express_to_tree(expression):
	return ""

def simplify_expression(expression):
	if len(expression)==1:
		return expression
	if expression[0] in inverse and inverse[expression[0]] == expression[1][0]:
		return expression[1][1]



def express_compare(expression_tree_1,expression_tree_2):
	return 0

def tree_to_expression(expression_tree):
	expression = [expression_tree.expression]
	E_1 = False
	A_1  = True
	for term in expression_tree.next:
		next_expression = tree_to_expression(term)
		if next_expression[0] != "1":
			A_1 = False
			expression.append(next_expression)
		else:
			if not E_1:
				E_1 = True
				expression.append(next_expression)
	if A_1 and expression[0] != "X":
		return ["1"]

	return expression 


print(tree_to_expression(expression_tree()))
