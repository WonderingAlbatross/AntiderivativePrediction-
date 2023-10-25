import random
element = ["+","*","^","-","/","Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf","X","1"]

weight = [10,20,1,10,10,3,5,3,3,3,1,1,1,10,20]
level = {"+": 1, "*": 2, "^": 20, "-": 1, "/": 3, "Sqrt": 15, "Exp": 10, "Log": 10, "Sin": 5, "Cos": 5, "ArcSin": 25, "ArcTan": 25, "Erf": 25}
inverse = {"-":"-","/":"/","Exp":"Log","Log":"Exp","Sin":"ArcSin"}


new_term_rate_for_abelian_operators = 1-1/2
non_const_exp_rate = 0.2
non_x_rate_for_complicated_expressions = 0.3
max_level = 30




class expression_tree:
	def __init__(self,lv = 0, expression = ""):
		self.level = lv
		self.next = []
		if expression:
			self.expression = expression
		else:
			if lv > max_level:
				self.expression = random.choices(element[-2:],weight[-2:])[0]
			else:
				self.expression = random.choices(element,weight)[0]

				self.generate_next(self.expression)

	def generate_next(self,expression):
		if expression in ("+","*"):
			self.next = [expression_tree(lv = level[expression]+self.level),expression_tree(lv = level[expression]+self.level)]
			while(random.random()<new_term_rate_for_abelian_operators):
				self.next.append(expression_tree(level[expression]+self.level))
		if expression == "^":
			if random.random()>non_const_exp_rate:
				self.next = [expression_tree(lv = level[expression]+self.level),expression_tree(expression = "K")]
			else:
				self.next = [expression_tree(lv = level[expression]+self.level),expression_tree(lv = level[expression]+self.level)]
		if expression in ("-","/"):
			self.next = [expression_tree(lv = level[expression]+self.level)]
		if expression in ("Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf"):
			if random.random()>non_x_rate_for_complicated_expressions:
				self.next = [expression_tree(expression = "X")]
			else:
				self.next = [expression_tree(lv = level[expression]+self.level)]			





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