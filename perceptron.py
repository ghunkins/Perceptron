# CSC 242 | AI
# PROJECT #4

# IMPORTS
from numpy import dot, array, random
from random import randint
import matplotlib.pyplot as plt
import sys
from math import exp
# THRESHOLD FUNCTIONS
heaviside = lambda z: 0 if z < 0 else 1     # step function
logistic = lambda z: 1/(1+exp(-z))          # logistic function
# GLOBAL VARIABLES TO CHANGE FOR VARYING PERCEPTRON FUNCTION
learningRates = [0.1, 0.2, 0.5, 1, 2, 5, 10, 100]   # learning rates
n = 1000                                             # max times to train

# PERCEPTRON CLASS
class Perceptron():
    def __init__(self, _lr=0.0, _w=None):    # initialize with learning rate and w
        self.lr = _lr               # float             
        self.w = _w                 # numpy array
    def train(self, x, Y):                # train on data x, expected outcome Y
        if (len(x) != len(self.w)): return
        yprime = dot(self.w, x)
        err = Y - heaviside(yprime)
        self.w += self.lr * err * x
        return err
    def test(self, x, Y):                 # return 0 if no error, return 1 if error
        yprime = dot(self.w, x)
        return Y - heaviside(yprime)

# Parses data from comma-seperated text files
# Ex: earthquake-clean.data.txt
def getData(filename):
    try:
        f = open(filename)
        X, Y = [], []
        for line in f:
            data = ([float(s) for s in line.split(',')])    # split on the comma
            X.append([data[0], data[1], 1.0])
            Y.append(data[2])
    except Exception:
        print("Issue with obtaining data from:", filename)
        print("Exiting.")
        sys.exit()
    return X, Y

def testDev(_w):              # test the Dev set, returns num wrong
    devF.seek(0)             # reset the pointer to the beginning of the text file
    errors = 0
    w = _w
    for i, dev_inst in enumerate(devF):
        Y, x = parse(dev_inst)
        if (len(x) != len(myPercep.w)): continue 
        yprime = dot(w, x)
        err = Y - heaviside(yprime)
        errors += abs(err)
    #print("Errors on Dev set: ", errors)
    return errors

# Train on a random data point in X, Y
# Returns the num of errors
def trainStochastic(X, Y, sizeOfData):
    randomEx = randint(0, sizeOfData-1)         # choose random example
    return myPercep.train(array(X[randomEx]), Y[randomEx])    # train on it
    
def testTest(_w):             # test the Test set, returns num wrong
    errors = 0
    w = _w
    for test_inst in testF.readlines():
        x, Y = parse()
        yprime = dot(w, x)
        err = Y - heaviside(yprime)
        errors += err
    print("Errors on Test set: ", errors)
    return errors

def testDataSet(X, Y):
    errors = 0
    for i in range(len(Y)):
        if (myPercep.test(array(X[i]), Y[i]) != 0.0):
            errors += 1
            #print(((len(Y) - errors) / len(Y)) )
    return ((len(Y) - errors) / len(Y))     # returns percentage correct

def plotErrors(err):
    plt.plot(err)
    plt.ylabel("Error")
    plt.xlabel("Training num")
    plt.title("Learning Rate: " + str(myPercep.lr))
    plt.show()
    print("change")

def plotPercentageCorrect(p):
    plt.plot(p)
    plt.ylabel("Percent Correct")
    plt.xlabel("Training num")
    plt.title("Learning Rate: " + str(myPercep.lr))
    plt.ylim(0,1)
    plt.show()


def main():
    learningRates = [0.1, 0.2, 0.5, 1, 2, 5, 10, 100]  # learning rates
    X, Y = getData("earthquake-clean.data.txt")
    sizeOfData = len(Y)
    for lr in learningRates:        # test Perceptron on all learning rates
        myPercep.w = random.rand(3)
        # myPercep.w = array([0. for i in range(n)])
        myPercep.lr = lr
        errors = []
        percent = []
        for i in range(n):
            errors.append(trainStochastic(X, Y, sizeOfData))
            percent.append(testDataSet(X, Y))
            print(i, "|", myPercep.w)
        plotErrors(errors)
        plotPercentageCorrect(percent)

myPercep = Perceptron()
main()
        
