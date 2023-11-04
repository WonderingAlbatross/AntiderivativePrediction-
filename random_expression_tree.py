import random
from functools import cmp_to_key

element = ["+","*","^","-","/","Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf","X","1"]

weight = [10,20,1,10,10,3,5,3,3,3,1,1,1,10,20]
level = {"+": 5, "*": 5, "^": 20, "-": 1, "/": 3, "Sqrt": 15, "Exp": 10, "Log": 10, "Sin": 5, "Cos": 5, "ArcSin": 25, "ArcTan": 25, "Erf": 25}
forbid = {"+":"+","*":"*","-":"-","/":"/","Exp":"Log","Log":"Exp","Sin":"ArcSin"}


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
		elif expression in ("-","/","Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf"):
			self.expression = ""
			while expression in ("-","/","Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf"):
				self.rec_level += level[expression]
				self.expression += "," + expression
				if self.rec_level > max_level:
					expression = "X"
				elif expression in ("Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf") and random.random()>non_x_rate_for_complicated_expressions:
					expression = "X"
				else:
					expression = random.choices(element,weight)[0]
			self.expression = self.simplify_uni(self.expression)
			if not self.expression:
				self.expression = "1"
			else:
				self.next = [expression_tree(lv = self.rec_level,expression = expression)]

	#remove this
	def simplify_uni(self,expression):
		#["+","*","^","-","/","Sqrt","Exp","Log","Sin","Cos","ArcSin","ArcTan","Erf"]
		e = expression[1:].split(",")
		change = True
		while change:
			change = False
			for i in range(len(e)-1):
				if e[i+1]=="-":
					if e[i] in ("/","Sin","ArcSin","ArcSin","Arctan","Erf"):
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
			else:
				#if self.expression == "" and self.next[0].expression == "":
				return k
		else:
			if len(self.next) == 1:
				k = self.next[0].simplify()
				self.expression = self.next[0].expression
				self.next = self.next[0].next
				return k
			elif self.expression == "*":
				for i in range(len(self.next)):
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
										#next: add x/x function here

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

			
def is_sorted(lst):
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))




def express_to_tree(expression):
	return ""

	









exp = expression_tree()
t = 1
while t:
	t = exp.simplify()
	print(exp.tree_to_expression())
