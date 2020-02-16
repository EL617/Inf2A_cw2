# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    NN = set()
    NNS = set()
    with open("sentences.txt", "r") as f:
        for line in f:
            for word, pos in [part.split('|') for part in line.split(' ')]:
            	if pos == 'NN':
            		NN.add(word)
            	elif pos == 'NNS':
            		NNS.add(word)
    return list(NN.intersection(NNS))

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    rule1 = re.match('^[A-Z]*[a-z]+([^s|x|y|z|a|i|o|u|e]|^(ch)|^(sh))s$',s)
    rule2 = re.match('^[A-Z]*[a-z]+(x|s|z|ch|sh|ss|zz)es$',s)
    rule3 = re.match('^[A-Z]*[a-z]+os$',s)
    rule4 = re.match('^[A-Z]*[a-z]+oes$',s)
    rule5 = re.match('^[A-Z]*[a-z]+ves$',s)
    rule6 = re.match('^[A-Z]*[a-z]+[a|e|i|o|u]ys$',s)
    rule7 = re.match('^[A-Z]*[a-z]+[^a|e|i|o|u]ies$',s)
    rule8 = re.match('^[A-Z]*[a-z]*men$',s)
    rule9 = re.match('^[A-Z]*[a-z]+a$',s)
    rule10 = re.match('^[A-Z]*[a-z]+([^i|o|s|x|z]|^(ch)|^(sh))es$',s)
    rule11 = re.match('^[A-Z]*[a-z]+i$',s)

    if s in unchanging_plurals_list:
    	return s

    elif rule1:
    	if (s[0:-1],'NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-1]
    		return n_stem
    	else:
    		return ''
    		
    elif rule2:
    	if (s[0:-2] + 'is','NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-2] + 'is'
    		return n_stem
    	elif (s[0:-2],'NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-2]
    		return n_stem    	
    	elif (s[0:-1],'NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-1]
    		return n_stem
    	else:
    		return ''	

    elif rule3:
    	if (s[0:-1],'NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-1]
    		return n_stem
    	else:
    		return ''

    elif rule4:
    	if (s[0:-2],'NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-2]
    		return n_stem
    	else:
    		return ''

    elif rule5:
    	if (s[0:-3] + 'f','NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-3] + 'f'
    		return n_stem
    	elif (s[0:-3] + 'fe','NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-3] + 'fe'
    		return n_stem
    	else:
    		return ''

    elif rule6:
    	if (s[0:-1],'NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-1]
    		return n_stem
    	else:
    		return ''

    elif rule7:
    	if (s[0:-3] + 'y','NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-3] + 'y'
    		return n_stem
    	else:
    		return ''

    elif rule8:
    	if (s[0:-2] + 'an','NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-2] + 'an'
    		return n_stem
    	else:
    		return ''

    elif rule9:
    	if (s[0:-1] + 'on','NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-1] + 'on'
    		return n_stem
    	else:
    		return ''

    elif rule10:
    	if (s[0:-1],'NN') in brown_taggedset and (s,'NNS') in brown_taggedset:	
    		n_stem = s[0:-1]
    		return n_stem
    	else:
    		return ''

    elif rule11:
    	if (s[0:-1] + 'us','NN') in brown_taggedset and (s,'NNS') in brown_taggedset:
    		n_stem = s[0:-1] + 'us'
    		return n_stem
    	else:
    		return ''

    else:
    	return ''


def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    tagset = []
    for (word,tag) in function_words_tags:
    	if wd == word:
    		add(tagset, tag)

    prop_lxtags = ['P']
    adj_lxtags = ['A']
    v_lxtags = ['I','T']
    n_lxtags = ['N']

    for tag in prop_lxtags:
    	if wd in lx.getAll(tag):
    		add(tagset, tag)

    for tag in adj_lxtags:
    	if wd in lx.getAll(tag):
    		add(tagset, tag)

    for tag in v_lxtags:
    	if wd in lx.getAll(tag):
    		add(tagset, (tag + 'p'))
    	if verb_stem(wd) in lx.getAll(tag):
    		add(tagset, (tag + 's'))

    for tag in n_lxtags:
    	if wd in lx.getAll(tag):
    		add(tagset, (tag + 's'))
    	if noun_stem(wd) in lx.getAll(tag):
    		add(tagset, (tag + 'p'))

    return list(tagset)


def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]



# End of PART B.