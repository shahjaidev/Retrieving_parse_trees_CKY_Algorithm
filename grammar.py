"""
COMS W4705 - Natural Language Processing - Spring 2019
Homework 2 - Parsing with Context Free Grammars 
Yassine Benajiba
"""

import sys
import math
from collections import defaultdict
from math import fsum

class Pcfg(object): 
    """
    Represent a probabilistic context free grammar. 
    """

    def __init__(self, grammar_file): 
        self.rhs_to_rules = defaultdict(list)
        self.lhs_to_rules = defaultdict(list)
        self.startsymbol = None 
        self.read_rules(grammar_file)      
 
    def read_rules(self,grammar_file):
        
        for line in grammar_file: 
            line = line.strip()
            if line and not line.startswith("#"):
                if "->" in line: 
                    rule = self.parse_rule(line.strip())
                    lhs, rhs, prob = rule
                    self.rhs_to_rules[rhs].append(rule)
                    self.lhs_to_rules[lhs].append(rule)
                else: 
                    startsymbol, prob = line.rsplit(";")
                    self.startsymbol = startsymbol.strip()
                    
     
    def parse_rule(self,rule_s):
        lhs, other = rule_s.split("->")
        lhs = lhs.strip()
        rhs_s, prob_s = other.rsplit(";",1) 
        prob = float(prob_s)
        rhs = tuple(rhs_s.strip().split())
        return (lhs, rhs, prob)

    def verify_grammar(self):
        """
        Return True if the grammar is a valid PCFG in CNF.
        Otherwise return False. 
        """

        for key in self.lhs_to_rules.keys():

            rules = self.lhs_to_rules[key]

            for r in rules:
                lhs = r[0]
                rhs = r[1]

                if (len(rhs) != 1 and len(rhs) != 2):
                    return False
                if(len(rhs) == 2):
                    if (rhs[0].isupper() != True or rhs[1].isupper() != True):
                        return  False
                elif(len(rhs) == 1):
                    if (rhs[0].islower() != True):
                        return False

            arr = []
            for r in rules:
                arr.append(r[2])

            if ((round(abs(math.fsum(arr)), 1)) != 1.0):
                return False
            return True


if __name__ == "__main__":
    with open(sys.argv[1],'r') as grammar_file:
        grammar = Pcfg(grammar_file)

    if (grammar.verify_grammar()):
        print("Grammar is in CNF.")  
    else:
        print("Grammar is not in CNF.")  
    
