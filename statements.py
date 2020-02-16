# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__ (self):
        self.lx = []
    def add(self,stem,cat):
        if cat in "PANIT":
            add(self.lx,(stem,cat))
    
    def getAll(self,cat):
        result = []
        for i in self.lx:
            if cat in i:
                add(result,i[0])
        return result

class FactBase:
    """stores unary and binary relational facts"""
    def __init__ (self):
        self.unary = []
        self.binary = []
    def addUnary(self,pred,e1):
        add(self.unary,(pred,e1))
    def queryUnary(self,pred,e1):
        for i in self.unary:
            if (pred,e1) in self.unary:
                return True
            else:
                return False
    def addBinary(self,pred,e1,e2):
        add(self.binary,(pred,e1,e2))
    def queryBinary(self,pred,e1,e2):
        for i in self.binary:
            if(pred,e1,e2) in self.binary:
                return True
            else:
                return False

import re
from nltk.corpus import brown 

brown_taggedset = set(brown.tagged_words())

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    case1 = re.match('^[A-Z]*[a-z]+([^s|x|y|z|a|e|i|o|u]|^(ch)|^(sh))s$',s)
    case2 = re.match('^[A-Z]*[a-z]+[a|e|i|o|u]ys$',s)
    case3 = re.match('^[A-Z]*[a-z]+[^a|e|i|o|u]ies$',s)
    case4 = re.match('^[^a|e|i|o|u]ies$',s)
    case5 = re.match('^[A-Z]*[a-z]+(o|x|ch|sh|ss|zz)es$',s)
    case6 = re.match('^[A-Z]*[a-z]+(([^s]se)|([^z]ze))s$',s)
    case7 = re.match('^has$',s)
    case8 = re.match('^[A-Z]*[a-z]+([^i|o|s|x|z]|^(ch)|^(sh))es$',s)

    v_stem = ''

    if case1:
        v_stem = s[0:-1]

    elif case2:
        v_stem = s[0:-1]

    elif case3:
        v_stem = s[0:-3] + 'y'

    elif case4:
        v_stem = s[0:-1]

    elif case5:
        v_stem = s[0:-2]

    elif case6:
        v_stem = s[0:-1]

    elif case7:
		return 'have'

    elif case8:
        v_stem = s[0:-1]

    if (s, 'VBZ') not in brown_taggedset and (v_stem, 'VB') not in brown_taggedset:
		return ''

    return v_stem


def add_proper_name (w,lx):	
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.

