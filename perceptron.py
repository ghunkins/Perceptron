# CSC 242 | AI
# PROJECT #4
# PROGRAMMERS:  Gregory Hunkins and Matthew Dombroski

# IMPORTS
from numpy import dot, array, random, split
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
        self.lr = _lr                        # float             
        self.w = _w                          # numpy array
    def train(self, x, y):                   # train on data x, expected outcome Y
        if (len(x) != len(self.w)): return
        yprime = dot(self.w, x)
        err = y - heaviside(yprime)
        self.w += self.lr * err * x
        return err
    def test(self, x, y):                 # return 0 if no error, return 1 if error
        yprime = dot(self.w, x)
        return y - heaviside(yprime)

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

def plotPercentageCorrect(p):
    plt.plot(p)
    plt.ylabel("Percent Correct")
    plt.xlabel("Training num")
    plt.title("Learning Rate: " + str(myPercep.lr))
    plt.ylim(0,1)
    plt.show()

def divideData(X, Y, divisions):
    X = array(X)
    Y = array(Y)
    n_train, n_dev = (divisions[0]/sum(divisions))*len(X), (divisions[1]/sum(divisions))*len(X)
    n_test = len(X) - n_train - n_dev
    trainX, devX, testX = split(X, [n_train, n_dev, n_test])
    trainY, devY, testY = split(Y, [n_train, n_dev, n_test])
    return trainX, devX, testX, trainY, devY, testY

def plotWvsRaw(X, Y, w):
    x_true, y_true, x_false, y_false = [], [], [], []
    for i, y in enumerate(Y):
        if (y):
            x_true.append[]
        else:




def main():
    learningRates = [0.1, 0.2, 0.5, 1, 2, 5, 10, 100]  # learning rates
    X, Y = getData("earthquake-clean.data.txt")
    trainX, devX, testX, trainY, devY, testY = divideData(X, Y, (0.6, 0.2, 0.2)) # 60% train, 20% dev, 20% testterm
    rawX = X[0:len(X)-2]
    sizeOfData = len(Y)
    for lr in learningRates:             # test Perceptron on all learning rates
        myPercep.w = random.rand(3)      # randomly generate a w vector
        myPercep.lr = lr                 # assign the learning rate
        errors = []                      # initalize an array to save the errors in
        percent = []                     # initialize an array to save the percentage correct
        for i in range(n):
            errors.append(trainStochastic(X, Y, sizeOfData))
            percent.append(testDataSet(X, Y))
            print(i, "|", myPercep.w)
        plotErrors(errors)
        plotPercentageCorrect(percent)

myPercep = Perceptron()
main()
        
