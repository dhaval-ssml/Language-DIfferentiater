"""
Name: Dhaval Shrishrimal @<drs4554@cs.rit.edu>
File: 'main.py'
Description: This is the main entry program. The user runs this file 
with command line arguments it either creates a decision tree or an 
adaboost forrest and stores it into binary file, or predicts a file
of sentences.
"""

import sys
import pickle
from decision_learning import decision_tree_learning, create_examples, node, check_sentence
from adaboost import ada_boost, check_ada_sentence

def train(filename, output, ltype):
    """
    This function creates an example file and trains it based on the
    ltype and stores it as the output file.
    @param filename: name of file to train from
    @oaram output: the file to be saved
    @param ltype: at or ada?
    """
    # create examples file
    examples = create_examples(filename)
    raw = None
    # if ltype = dt
    if ltype == 'dt':
        raw = decision_tree_learning(examples, [], True, -1, [])
    # if ltype = ada
    elif ltype == 'ada':
        raw = ada_boost(examples, 130)
    # else
    else:
        print('Wrong learning type. Enter dt or ada.') 
        return
    # create and store to outfile
    outfile = open(output,'wb')
    pickle.dump(raw, outfile)
    outfile.close()
    return

def predict(filename, testname):
    """
    This program takes in a algorithm and the test file and
    prints whether each statement is dutch or english
    @param filename: the name of the file containing the algo
    @oaran testname: the file with test sentences
    """
    # open the files
    test = open(testname, 'r')
    infile = open(filename, 'rb')
    # load the data
    data = pickle.load(infile)
    isDt = isinstance(data, node)
    # check for dt
    if isDt:
        for line in test:
            print(check_sentence(line.strip(), data))
    # check for ada
    else:
        for line in test:
            print(check_ada_sentence(line.strip(), data[0], data[1]))
    infile.close()
    test.close()
    return

def main():
    """
    This is the main entry point of the program
    """
    if len(sys.argv) < 2:
        print("Enter predict or train.")
        return
    # if called to train
    if sys.argv[1] == 'train':
        if len(sys.argv) != 5:
            print("Invalid # of arguments")
            return
        else:
            print("Creating data file...")
            algo = train(sys.argv[2], sys.argv[3], sys.argv[4])
            if algo: print("File Saved. Exiting Program...")
    # if called to predict
    elif sys.argv[1] == 'predict':
        if len(sys.argv) != 4:
            print("Invalid # of arguments")
            return
        else:
            predict(sys.argv[2], sys.argv[3])
    else:
        print("Invalid arguments")
        return

# run the program
if __name__ == "__main__":
    main()