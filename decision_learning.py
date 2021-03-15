"""
Name: Dhaval Shrishrimal @<drs4554@cs.rit.edu>
File: 'decision_learning.py'
Description: This files has all the functions to create the decision
tree and then decide based on that whether the langauge is dutch or english.
"""

from math import log2, pow, inf
from random import randint

# this is the list of all attributes
atList = ['th', ' ee', 'het', ' de ', 'ij', 'sch', 'van', 'aa', 'als', 'oo']

class node:
    """
    This class represents a node on the decision tree with the
    left and right examples, att index and value if the node is a 
    leaf node.
    """
    def __init__(self, left, right, att, value):
        self.att = att
        self.left = left
        self.right = right
        self.value = value

def check_attributes(sentence):
    """
    Checkes the attributes of the sentence and return a list
    of 10 numbers 1 if the att exists, 0 if it does not.
    """
    atVal = [0] * 10
    attNum = 0
    for att in atList:
        if att in sentence:
            atVal[attNum] = 1
        attNum += 1
    atVal[0] = 1 - atVal[0]
    return atVal

def create_examples(filename):
    """
    This function takes a filename and creates an example file out of
    it.
    """
    examples_raw = open(filename, 'r')
    examples = list()
    for line in examples_raw:
        att_line = check_attributes(line.strip()[2:])
        examples.append((line[0:2], att_line))
    return examples

def check_all(examples):
    """
    This checks if all the examples are in the same language.
    """
    first = ''
    for ex in examples:
        if first == '':
            first = ex[0]
        if ex[0] != first:
            return False
    return True

def calc_entropy(lang):
    """
    Calculates the entropy of the left or right
    parts of a node by checking the correct and incorrect numbers.
    """
    # if lang is empty
    if len(lang) == 0:
        return 0
    count_en = 0
    count_nl = 0
    # for example in lang
    for ex in lang:
        if ex[0] == 'en':
            count_en += 1
        else:
            count_nl += 1
    # to avoid divide by zero error
    if count_en == 0:
        english = 0
        dutch = (count_nl / len(lang)) * log2(count_nl / len(lang))
    elif count_nl == 0:
        dutch = 0
        english = (count_en / len(lang)) * log2(count_en / len(lang))
    # if none of the counts are zero
    else:
        english = (count_en / len(lang)) * log2(count_en / len(lang))
        dutch = (count_nl / len(lang)) * log2(count_nl / len(lang))
    return english + dutch

def info_gain(examples, atIdx, p_ent):
    """
    This function calculates the infromation gain of a new attribute,
    it has examples, the attribute's inex, entropy of the parent node.
    """
    dutch = list()
    english = list()
    # divide into arma
    for ex in examples:
        if ex[1][atIdx] == 1:
            dutch.append(ex)
        else:
            english.append(ex)
    # calc entropy for both
    nl_ent = calc_entropy(dutch)
    en_ent = calc_entropy(english)
    # add them weighted
    final = (len(dutch) / len(examples)) * nl_ent + \
        (len(english) / len(examples)) * en_ent
    return p_ent - final

def get_most_imp(examples, p_ent, atDone):
    """
    This loops over the attributes that are not used yet,
    and then calculates the most important attribute for the
    next round.
    """
    maxGain = -inf
    maxIdx = -1
    # find the max gain
    for idx in range(len(atList)):
        if not atList[idx] in atDone:
            gain = info_gain(examples, idx, p_ent)
            if gain > maxGain:
                maxGain = gain
                maxIdx = idx
    return maxIdx

def findPV(examples):
    """
    This function finds the pluarity value of the given list of examples.
    """
    total = 0
    for ex in examples:
        if ex[0] == 'en':
            total += 1
        else:
            total -= 1
    if total == 0:
        total += pow(-1, randint(0,1))
    if total > 0:
        return 'en'
    else:
        return 'nl'

def decision_tree_learning(examples, parent_examples, first, atPrev, atDone):
    """
    Creates a decsision tree from scratch in a recurssive way.
    needs a list of examples, a list of parent examples, first if this is the first call
    atPrev which is previous attribute. and a list of all the attribute that are done.
    """
    # if len of examples is zero
    if len(examples) == 0:
        return node(None, None, -1, findPV(parent_examples))
    # if all examples are the same type
    elif check_all(examples):
        return node(None, None, -1, examples[0][0])
    # if all examples are used
    elif len(atList) == len(atDone):
        return node(None, None, -1, findPV(examples))
    else:
        # is this the first call?
        if first:
            p_ent = 0
        else:
            p_ent = abs(info_gain(parent_examples, atPrev, 0))
        # find the at index of the next important index
        atIdx = get_most_imp(examples, p_ent, atDone)
        atDone.append(atList[atIdx])
        left = list()
        right = list()
        # split the examples
        for ex in examples:
            if ex[1][atIdx] == 1:
                left.append(ex)
            else:
                right.append(ex)
        # the recurssive calls
        left_tree = decision_tree_learning(left, examples, False, atIdx, atDone)
        right_tree = decision_tree_learning(right, examples, False, atIdx, atDone)
        head = node(left_tree, right_tree, atIdx, None)
        return head

def check_sentence(sentence, tree):
    """
    This function checks the sentence for whether it is dutch or
    english by passing it through the decision tree
    """
    node = tree
    atTemp = check_attributes(sentence)
    while node.value == None:
        if atTemp[node.att] == 1:
            node = node.left
        else:
            node = node.right
    return (node.value)