"""
Name: Dhaval Shrishrimal @<drs4554@cs.rit.edu>
File: 'adaboost.py'
Description: This file creates the forest for adaboost
and has the functions to check sentences based on the forest.
"""

from math import log2

# the list of attributes
atList = ['th', ' ee', 'het', ' de ', 'ij', 'sch', 'van', 'aa', 'als', 'oo']

class hypo:
    """
    This class represents a hypothesis or a stump.
    @left: the list of left examples
    @right: the list of right examples
    @attIdx: the index of the attribute used  
    """
    def __init__(self, left, right, attIdx):
        self.left = left
        self.right = right
        self.attIdx = attIdx

def form_hypo(examples, attIdx):
    """
    this forms the hypothesis from the example and the
    attIdx for the head.
    """
    left = list()
    right = list()
    for ex in examples:
        if ex[1][attIdx] == 0:
            left.append(ex)
        else:
            right.append(ex)
    return hypo(left, right, attIdx)

def find_next(examples, weights):
    """
    Given examples and weights, the program loops over
    the atList, and figures out the attributes with the lowest
    total error.
    """
    total_incorrect = [0] * len(atList)
    # for each attribute
    for attIdx in range(len(atList)):
        # loop over examples
        for idx in range(len(examples)):
            ex = examples[idx]
            # check for incorrect examples
            if ex[1][attIdx] == 1 and attIdx != 0 and ex[0] == 'en':
                total_incorrect[attIdx] += weights[idx]
            elif ex[1][attIdx] == 1 and attIdx == 0 and ex[0] == 'nl':
                total_incorrect[attIdx] += weights[idx]
            elif ex[1][attIdx] == 0 and attIdx != 0 and ex[0] == 'nl':
                total_incorrect[attIdx] += weights[idx]
            elif ex[1][attIdx] == 0 and attIdx == 0 and ex[0] == 'en':
                total_incorrect[attIdx] += weights[idx]
    return total_incorrect.index(min(total_incorrect))

def ada_boost(examples, k):
    """
    This function creates the adaboost stumps stores them in an array
    and then returns it with the weight of each stump
    """
    # inititalize the hypothesis list and hypothesis weight
    hypo_list = [None] * k
    hypo_weights = [0] * k
    weights = [1/len(examples)] * len(examples)
    # for 1..k
    for i in range(k):
        # get the first stump head
        attIdx = find_next(examples, weights)
        # create a hypothesis
        hypo_list[i] = form_hypo(examples, attIdx)
        total_error = 0
        # find the total error
        for idx in range(len(examples)):
            ex = examples[idx]
            if ex[1][attIdx] == 1 and attIdx != 0 and ex[0] == 'en':
                total_error += weights[idx]
            elif ex[1][attIdx] == 1 and attIdx == 0 and ex[0] == 'nl':
                total_error += weights[idx]
            elif ex[1][attIdx] == 0 and attIdx != 0 and ex[0] == 'nl':
                total_error += weights[idx]
            elif ex[1][attIdx] == 0 and attIdx == 0 and ex[0] == 'en':
                total_error += weights[idx]
        # fix the total_error so that log2 does not give out an errro
        if total_error == 0:
            total_error = 0.00001
        elif total_error == 1:
            total_error = 0.99999
        # fix the weights for the next round
        for idx in range(len(examples)):
            ex = examples[idx]
            if ex[1][attIdx] == 1 and attIdx != 0 and ex[0] == 'nl':
                weights[idx] = weights[idx] * (total_error / (1 - total_error))
            elif ex[1][attIdx] == 1 and attIdx == 0 and ex[0] == 'en':
                weights[idx] = weights[idx] * (total_error / (1 - total_error))
            elif ex[1][attIdx] == 0 and attIdx != 0 and ex[0] == 'en':
                weights[idx] = weights[idx] * (total_error / (1 - total_error))
            elif ex[1][attIdx] == 0 and attIdx == 0 and ex[0] == 'nl':
                weights[idx] = weights[idx] * (total_error / (1 - total_error))
        total = 0
        # store the hypothesis weights
        hypo_weights[i] = log2((1 - total_error) / total_error)
    return (hypo_list, hypo_weights)

def check_ada_sentence(sentence, hypo_list, hypo_weights):
    """
    This function takes in a sentence and checks whether the sentence
    is dutch or english using the adaboost tree forest.
    """
    english = 0
    dutch = 0
    # for each hypo
    for hypo in hypo_list:
        # if hypo in sentence
        if atList[hypo.attIdx] in sentence:
            if hypo.attIdx == 0:
                english += hypo_weights[hypo.attIdx]
            else:
                dutch += hypo_weights[hypo.attIdx]
        # if hypo not in sentence
        else:
            if hypo.attIdx == 0:
                dutch += hypo_weights[hypo.attIdx]
            else:
                english += hypo_weights[hypo.attIdx]
    # return dutch or english
    if english > dutch:
        return 'en'
    else:
        return 'nl'