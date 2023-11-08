import random
from functools import cmp_to_key

element = ["+","*","^","-","/","Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf","X","1"]

weight = [10,20,1,10,10,3,5,3,3,3,1,1,1,10,20]
level = {"+": 5, "*": 5, "^": 20, "-": 1, "/": 3, "Sqrt": 15, "Exp": 10, "Log": 10, "Sin": 5, "Cos": 5, "ArcSin": 25, "ArcTan": 25, "Erf": 25}
forbid = {"+":"+","*":"*","-":"-","/":"/","Exp":"Log","Log":"Exp","Sin":"ArcSin"}
inverse = {"-":"-","/":"/","Exp":"Log","Log":"Exp","Sin":"ArcSin"}

new_term_rate_for_abelian_operators = 1-1/2
non_const_exp_rate = 0.2
non_x_rate_for_complicated_expressions = 0.9
max_level = 10




class expression_tree:
	def __init__(self,lv = 0, expression = "",forbid = []):
		self.rec_level = lv
		self.weight = 0
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

	def __str__(self):
		return str(self.tree_to_expression())

#always simplify before sorting!
	def __eq__(self, other):
		if self.expression != other.expression:
			return False
		else:	
			if len(self.next) != len(other.next):
				return False
			else:
				for i in range(len(self.next)):
					if self.next[i] > other.next[i]:
						return False
					elif self.next[i] < other.next[i]:
						return False
				return True

	def __gt__(self, other):
		if self.expression != other.expression:
			return self.expression > other.expression
		else:	
			if len(self.next) != len(other.next):
				return len(self.next) > len(other.next)
			else:
				for i in range(len(self.next)):
					if self.next[i] < other.next[i]:
						return False
					elif self.next[i] > other.next[i]:
						return True
				return False


	def __lt__(self, other):
		if self.expression != other.expression:
			return self.expression < other.expression
		else:	
			if len(self.next) != len(other.next):
				return len(self.next) < len(other.next)
			else:
				for i in range(len(self.next)):
					if self.next[i] > other.next[i]:
						return False
					elif self.next[i] < other.next[i]:
						return True
				return False

	def __ge__(self, other):
		return not (self < other)

	def __le__(self, other):	
		return not (self > other)

	def __ne__(self, other):
		return not (self == other)

	def generate_next(self,expression):
		if expression in ("+","*"):
			self.next = [expression_tree(lv = level[expression]+self.rec_level,forbid = [expression])]
			self.next.append(expression_tree(lv = level[expression]+self.rec_level,forbid = [expression]))
			while(random.random()<new_term_rate_for_abelian_operators):
				self.next.append(expression_tree(lv = level[expression]+self.rec_level,forbid = [expression]))
		elif expression == "^":
			if random.random()>non_const_exp_rate:
				self.next = [expression_tree(lv = level[expression]+self.rec_level),expression_tree(lv = self.rec_level,expression = "K")]
			else:
				self.next = [expression_tree(lv = level[expression]+self.rec_level),expression_tree(lv = level[expression]+self.rec_level)]
		#rewrite this using forbid
		elif expression in ("-","/"):
			self.next = [expression_tree(lv = level[expression]+self.rec_level,forbid = [expression])]
		elif expression in ("Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf"):
			if random.random()>non_x_rate_for_complicated_expressions:
				self.expression = "X"
			else:
				self.next = [expression_tree(lv = level[expression]+self.rec_level,forbid = [expression])]




	def simplify(self):
		k = 0
		if self.expression in ("X","1","K"):
			return 0
		elif self.expression == "^":
			k = self.next[0].simplify() + self.next[1].simplify()
			if self.next[0].expression == "1" or self.next[1].expression== "1":
				self.expression = "1"
				self.next = []
				return 1
			else:
				return k
		elif self.expression not in ("+","*"):
			k = self.next[0].simplify()
			if self.next[0].expression == "1":
				self.expression = "1"
				self.next = []
				return 1
			elif self.expression in inverse and inverse[self.expression] == self.next[0].expression:
				self.expression = self.next[0].next[0].expression
				self.next = self.next[0].next[0].next
				return 1
			elif self.expression == "/" and self.next[0].expression == "Exp":
				self.expression, self.next[0].expression = "Exp", "-"
				return 1
			elif self.expression == "Log" and self.next[0].expression == "/":
				self.expression, self.next[0].expression = "-", "Log"
				return 1
			elif self.expression in ("/","Sin","ArcSin","ArcTan","Erf") and self.next[0].expression == "-":
				self.expression, self.next[0].expression = self.next[0].expression, self.expression
				return 1
			elif self.expression == "Cos" and self.next[0].expression == "-":
				self.next[0] = self.next[0].next[0]
				return 1
			elif self.expression == "-" and self.next[0].expression == "+":
				pass
			return k

		else:
			if len(self.next) == 1:
				k = self.next[0].simplify()
				self.expression = self.next[0].expression
				self.next = self.next[0].next
				return k
			elif self.expression == "*":
				for i in range(len(self.next)):
					if self.next[i].expression == "-":
						self.next.pop(i)
						temp = expression_tree(expression = "1")
						temp.expression = "*"
						temp.next = self.next
						self.next = [temp]
						return 1
					k += self.next[i].simplify()
					if self.next[i].expression == "1":
						self.next.pop(i)
						return 1
					if self.next[i].expression == "*":
						temp = self.next.pop(i)
						self.next += temp.next
						return 1
					if self.next[i].expression == "/":
						for j in range(len(self.next)):
							if self.next[i].next[0] == self.next[j]:
								self.next.pop(max(i,j))
								self.next.pop(min(i,j))
								return 1

				if is_sorted(self.next):
					return k
				else:
					self.next.sort()
					return 1
			elif self.expression == "+":
				for i in range(len(self.next)):
					k += self.next[i].simplify()
					if self.next[i].expression == "+":
						temp = self.next.pop(i)
						self.next += temp.next
						return 1
				if not is_sorted(self.next):
					self.next.sort()
					k += 1
				for i in range(len(self.next)-1):
					if self.next[i] == self.next[i+1]:
						self.next.pop(i)
						return 1
				return k

	

	def tree_to_expression(self):
		expression = [self.expression]
		for term in self.next:
			next_expression = term.tree_to_expression()
			expression.append(next_expression)
		return expression 

	def recalculate_level(self,value = 0):
		self.rec_level = value + level[self.element]
		for expression in self.next:
			expression.recalculate_level(self.rec_level)
		return self.rec_level

	def max_level(self):
		lv_m = self.rec_level
		for expression in self.next:
			lv_m = max(lv_m,expression.max_level())
		return lv_m

	def recalculate_weight(self):
		self.weight = level[self.element]
		for expression in self.next:
			self.weight += expression.recalculate_weight()
		return self.weight

	def tree_to_wolfram(self):
		if self.expression in ("X","1","K"):
			temp = self.expression
		elif self.expression == "-":
			temp = self.expression +"("+ self.next[0].tree_to_wolfram() + ")"
		elif self.expression == "/":
			temp = "1" + self.expression +"("+ self.next[0].tree_to_wolfram() + ")"			
		elif self.expression == "*":
			temp = self.expression.join([next_expression.tree_to_wolfram() for next_expression in self.next])	
		elif self.expression == "+":
			temp = "(" + self.expression.join([next_expression.tree_to_wolfram() for next_expression in self.next]) + ")"
		elif self.expression == "^":
			temp = "("+ self.next[0].tree_to_wolfram() + ")"+ self.expression +"("+ self.next[1].tree_to_wolfram() + ")"
		else:
			temp = self.next[0].tree_to_wolfram()
			if temp[0] == "(":
				temp = temp[1:-1]
			temp = self.expression +"["+ temp+ "]"	

		temp.replace("*1/","/")
		temp.replace("(1)","1")
		temp.replace("(K)","K")
		temp.replace("(X)","X")
		# bracket need optimization
		return temp


			
def is_sorted(lst):
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))




def express_to_tree(expression):
	return ""

	









exp = expression_tree()
t = 1
while t:
	t = exp.simplify()
	print(exp.tree_to_expression())
	print(exp.tree_to_wolfram())
