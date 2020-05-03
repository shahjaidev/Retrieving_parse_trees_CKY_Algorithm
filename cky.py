"""
Homework - Parsing with Context Free Grammars
Jaidev Shah, js5161
"""
import math
import sys
from collections import defaultdict
import itertools
from grammar import Pcfg

### Use the following two functions to check the format of your data structures in part 3 ###
def check_table_format(table):
	"""
	Return true if the backpointer table object is formatted correctly.
	Otherwise return False and print an error.
	"""
	if not isinstance(table, dict):
		sys.stderr.write("Backpointer table is not a dict.\n")
		return False
	for split in table:
		if not isinstance(split, tuple) and len(split) ==2 and \
		  isinstance(split[0], int)  and isinstance(split[1], int):
			sys.stderr.write("Keys of the backpointer table must be tuples (i,j) representing spans.\n")
			return False
		if not isinstance(table[split], dict):
			sys.stderr.write("Value of backpointer table (for each span) is not a dict.\n")
			return False
		for nt in table[split]:
			if not isinstance(nt, str):
				sys.stderr.write("Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
				return False
			bps = table[split][nt]
			if isinstance(bps, str): # Leaf nodes may be strings
				continue
			if not isinstance(bps, tuple):
				sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Incorrect type: {}\n".format(bps))
				return False
			if len(bps) != 2 and len(bps) != 1:
				sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Found more than two backpointers: {}\n".format(bps))
				return False
			for bp in bps:
				if not isinstance(bp, tuple) or len(bp)!=3:
					sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has length != 3.\n".format(bp))
					return False
				if not (isinstance(bp[0], int) and isinstance(bp[1], int) and isinstance(bp[2], str)):
					print(bp)
					sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has incorrect type.\n".format(bp))
					return False
	return True

def check_probs_format(table):
	"""
	Return true if the probability table object is formatted correctly.
	Otherwise return False and print an error.
	"""
	if not isinstance(table, dict):
		sys.stderr.write("Probability table is not a dict.\n")
		return False
	for split in table:
		if not isinstance(split, tuple) and len(split) ==2 and isinstance(split[0], int) and isinstance(split[1], int):
			sys.stderr.write("Keys of the probability must be tuples (i,j) representing spans.\n")
			return False
		if not isinstance(table[split], dict):
			sys.stderr.write("Value of probability table (for each span) is not a dict.\n")
			return False
		for nt in table[split]:
			if not isinstance(nt, str):
				sys.stderr.write("Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
				return False
			prob = table[split][nt]
			if not isinstance(prob, float):
				sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a float.{}\n".format(prob))
				return False
			if prob > 0:
				sys.stderr.write("Log probability may not be > 0.  {}\n".format(prob))
				return False
	return True



class CkyParser(object):
	"""
	A CKY parser.
	"""

	def __init__(self, grammar):
		"""
		Initialize a new parser instance from a grammar.
		"""
		self.grammar = grammar

	def is_in_language(self,tokens):


		totaltokens = len(tokens)
		

		parse_dict = {}

		for i in range(totaltokens + 1):


			for j in range(totaltokens + 1):


				parse_dict[(i, j)] = []

		

		for k in range(totaltokens):


			my_tuple = (tokens[k], )

			rules = self.grammar.rhs_to_rules[my_tuple]
			

			for r in rules:
				parse_dict[(k, k + 1)].append(r[0]) #going through the diagonal

		for i in range(2, totaltokens + 1):
			

			for j in range(totaltokens + 1 - i):
				end = j + i
				for p in range(j + 1, end):
					

					b = parse_dict[(j, p)]
					c = parse_dict[(p, end)]
					

					for val_1 in b:
						for val_2 in c:
							check_t = (val_1, val_2)
							rhs_possibilities = self.grammar.rhs_to_rules[check_t]
							

							for r in rhs_possibilities:
								parse_dict[(j, end)].append(r[0])

		final_symbols = []
		

		for s in parse_dict[(0, totaltokens)]:
			if (s == self.grammar.startsymbol):
				final_symbols.append(s)

		if (final_symbols): #if table[0][num_tokens] has a start symbol, meaning the sentence was successfully parsed
			return True
		else:
			return False

	def parse_with_backpointers(self, tokens):
		"""
		Parse the input tokens and return a parse table and a probability table.
		"""
		n = len(tokens)
		

		parse_table = {}
		

		log_probs = {}

		for i in range(n + 1):
			for j in range(n + 1):
				parse_table[(i, j)] = {}
				log_probs[(i, j)] = {}

		for i in range(n):
			modified_tuple = (tokens[i], )

			rhs_result = self.grammar.rhs_to_rules[modified_tuple]
			for rule in rhs_result:
				lhs = rule[0]
				parse_table[(i, i + 1)][lhs] = tuple([(i, i + 1, lhs)])
				log_probs[i, i + 1][lhs] = math.log2(rule[2])	

			# for lhs in self.grammar.lhs_to_rules.keys():
			# 	#rules = {}
			# 	if (modified_tuple in self.grammar.lhs_to_rules[lhs]):
			# 		terminal = self.grammar.rhs_to_rules[modified_tuple]
			# 		parse_table[(i, i + 1)][lhs] = tuple([(i, i + 1, terminal[0])])
			# 		log_probs[i, i + 1][lhs] = math.log2(terminal[2])	
					
					#rules[lhs] = self.grammar.rhs_to_rules[modified_tuple]

		#print(parse_table)
			#if (lhs in rules.keys()):		
				
					

			# rhs_result = self.grammar.rhs_to_rules[modified_tuple]
			# max_prob = 0
			# for rule in rhs_result:
			# 	if (rule[2] > max_prob):
			# 		max_rule = rule


		for length in range(2, n + 1):
			
			for i in range(n + 1 - length):
				j = i + length
				
				best_split = {}
				for k in range(i + 1, j):
					b = parse_table[(i, k)]
					c = parse_table[(k, j)]
					#print(c.keys())
					b_nts = []
					c_nts = []

					for a in b.keys():
						b_nts.append(a)
					for d in c.keys():
						c_nts.append(d)

					#print(b_nts)
					#print(c_nts)

					possible_rhs_tuples = []
					
					for x in b_nts:
						for y in c_nts:
							possible_rhs_tuples.append((x, y))

					#print(possible_rhs_tuples)
					
					
					
					for rhs_tuple_to_check in possible_rhs_tuples:
						if rhs_tuple_to_check in self.grammar.rhs_to_rules.keys():
							rules = self.grammar.rhs_to_rules[rhs_tuple_to_check]
							max_prob = 0.0
							for r in rules:
								#print(r[2])
								if (r[2] > max_prob):	
									max_prob = r[2]
									best_split[r[0]] = (k, r)
				#print(best_split)
				for lhs_nt in best_split.keys():
					
					split_point = best_split[lhs_nt][0]
					rhs1_nt = str((best_split[lhs_nt][1][1][0]))
					rhs2_nt = str(best_split[lhs_nt][1][1][1])

					parse_table[(i, j)][lhs_nt] = tuple([(i, split_point, rhs1_nt), (split_point, j, rhs2_nt)]) #assigning backpointers
					log_probs[(i, j)][lhs_nt] = math.log2(best_split[lhs_nt][1][2])

			# 	limit = j + i
				# for lhs in self.grammar.lhs_to_rules.keys():
				# 	max_prob = 0.0
				# 	best_split = {}
				# 	for k in range(j + 1, limit):
				# 		#if (parse_table[(j, k)]):
				# 		if (parse_table[(j, k)]):
				# 			b = str([key for key in parse_table[(j, k)]][0])
				# 			#print(b)
				# 		else:
				# 			continue
				# 		#b = str(parse_table[(j, k)].keys()
				# 		#c = str(parse_table[(k, limit)].keys())
				# 		if (parse_table[(k, limit)]):
				# 			c = str([key for key in parse_table[(k, limit)]][0])
				# 			#print(c)
				# 		else:
				# 			continue
				# 		#for symbol1 in b:
				# 		#	for symbol2 in c:
				# 		tuple_to_check = (b, c)

				# 		rules = self.grammar.lhs_to_rules[lhs]
				# 		if (tuple_to_check in rules):
				# 			for r in rules:
				# 				if (r[2] > max_prob):
				# 					max_prob = r[2]
				# 					best_split[lhs] = (k, r)

				# 	if (lhs in best_split.keys()):
				# 		entry2 = int(best_split[0])
				# 		rhs1 = str(best_split[1][1][0])
				# 		rhs2 = str(best_split[1][1][1])

				# 		parse_table[(j, limit)][lhs] = tuple([(j, entry2, rhs1), (entry2, limit, rhs2)])
				# 		log_probs[(j, limit)][lhs] = math.log2(best_split[1][2])

						# #print(tuple_to_check)
						# rhs_result = self.grammar.rhs_to_rules[tuple_to_check]
						# if (rhs_result[2] > max_prob):
						# 	best_split = (i, j, rhs_result[2])
				


				# for rule in rhs_result:
				# 	if (rule[2] > max_prob):
				# 		max_rule = rule
					
		table = parse_table
		probs = log_probs
		return table, probs


def get_tree(chart, i,j,nt):
	"""
	Return the parse-tree rooted in non-terminal nt and covering span i,j.
	"""

	if isinstance(chart[(i, j)][nt][0], str):
		return(nt, chart[(i, j)][nt][0])
	

	else:
		# This means we have not reached a terminal and our nt has children-> left child and right child. We can recursively call get_tree 
			l_child = chart[(i, j)][nt][1]
			r_child = chart[(i, j)][nt][2]
			l_nt= l_child[0]
			l_i=l_child[1]
			l_j= l_child[2]
			r_nt=r_child[0]
			r_i=r_child[1]
			r_j=r_child[2]
			return(nt, get_tree(chart, l_i, l_j, l_nt), get_tree(chart, r_i, r_j, r_nt))
	

if __name__ == "__main__":

	with open('atis3.pcfg','r') as grammar_file:
		grammar = Pcfg(grammar_file)
		parser = CkyParser(grammar)
		toks =['flights', 'from','miami', 'to', 'cleveland','.']
		#toks =['miami', 'flights','cleveland', 'from', 'to','.']
		#parser.is_in_language(toks)
		print(parser.is_in_language(toks))
		table,probs = parser.parse_with_backpointers(toks)
		print(table)
		print(probs)
		#assert check_table_format(chart)
		#assert check_probs_format(probs)
		#get_tree(table, 0, len(toks), grammar.startsymbol)
