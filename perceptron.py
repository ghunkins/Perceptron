# CSC 242 | AI
# PROJECT #4
# OPTION: Linear Classifier (Perceptron)
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
n = 10000                                            # max times to train
logORheavi = False                                  # bool to switch between log and linear
convergence = 20

# PERCEPTRON CLASS
class Perceptron():
    def __init__(self, _lr=0.0, _w=None):    # initialize with learning rate and w
        self.lr = _lr                        # float             
        self.w = _w                          # numpy array
    def train(self, x, y):                   # train on data x, expected outcome Y
        if (len(x) != len(self.w)): return
        yprime = dot(self.w, x)
        if (logORheavi):
            err = y - heaviside(yprime)      # logORheavi = True --> linear
        else:
            err = y - logistic(yprime)       # logORheavi = False --> log
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
            x = []
            for i in range(len(data)-1):                    # handles variable len data
                x.append(data[i])
            x.append(1.0)                                  # for offset (b in y = mx + b)
            X.append(x)                                 
            Y.append(data[len(data)-1])
            #print("X:", x, "Y:", data[len(data)-1])
    except Exception:
        print("Issue with obtaining data from:", filename)
        print("Exiting.")
        sys.exit()
    return X, Y

# Train on a random data point in X, Y
# Returns the num of errors
def trainStochastic(X, Y, sizeOfData):
    randomEx = randint(0, len(X)-1)         # choose random example
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
    if (logORheavi):
        threshold = " | Threshold: Linear"
    else:
        threshold = " | Threshold: Logistic"
    plt.plot(err)
    plt.ylabel("Error")
    plt.xlabel("Training num")
    plt.title("Learning Rate: " + str(myPercep.lr) + threshold)
    plt.show()

def plotPercentageCorrect(p):
    if (logORheavi):
        threshold = " | Threshold: Linear"
    else:
        threshold = " | Threshold: Logistic"
    plt.plot(p)
    plt.ylabel("Percent Correct")
    plt.xlabel("Training num")
    plt.title("Learning Rate: " + str(myPercep.lr) + threshold)
    plt.ylim(0,1)
    plt.show()

def divideData(X, Y, divisions):
    X = array(X)
    Y = array(Y)
    n_train = int((divisions[0]/sum(divisions))*len(X))
    #n_test = len(X) - n_train 
    trainX, trainY, testX, testY = [], [], [], []
    for i in range(len(X)):
        if (i < n_train):
            trainX.append(X[i])
            trainY.append(Y[i])
        else:
            testX.append(X[i])
            testY.append(Y[i])
    return trainX, testX, trainY, testY

def plotWvsRaw(X, Y, w):
    if (len(X[0])-1 != 2):
        print("Dimension: " + str(len(X[0])-1))
        print("Cannot plot raw data that is not 2-D.")
        print("Returning.")
        return
    colors = []
    for y in Y:
        if (y):
            colors.append('red')
        else:
            colors.append('blue')
    #print(Y)
    #print(colors)
    plt.title("Weight Vector Plotted on Color-Classified Data")
    plt.scatter([row[0] for row in X], [row[1] for row in X], color=colors)
    slope, intercept = (w[0]/w[1]), (w[2]/w[1])         # modified from: http://stackoverflow.com/questions/7941226/add-line-based-on-slope-and-intercept-in-matplotlib
    line_vals = [slope * i + intercept for i in [row[0] for row in X]]
    #plt.plot([row[0] for row in X], line_vals)
    plt.show()

def converged(errors):
    if (len(errors) < convergence):
        return False
    for i in range((-convergence+1), 1):
        if (errors[i] != 0):
            return False
    return True

def main():
    learningRates = [0.1, 0.2, 0.5, 1, 2, 5, 10, 100]  # learning rates
    TF = [True, False]
    X, Y = getData("earthquake-clean.data.txt")
    trainX, testX, trainY, testY = divideData(X, Y, (0.8, 0.2)) # 80% train, 20% test
    rawX = X[0:len(X)-2]
    sizeOfData = len(Y)
    for lr in learningRates:             # test Perceptron on all learning rates
        for boolean in TF:
            global logORheavi
            logORheavi = boolean
            myPercep.w = random.rand(3)      # randomly generate a w vector
            myPercep.lr = lr                 # assign the learning rate
            errors = []                      # initalize an array to save the errors in
            percent = []                     # initialize an array to save the percentage correct
            for i in range(n):
                errors.append(trainStochastic(trainX, trainY, sizeOfData))      # add to errors for plotting
                percent.append(testDataSet(testX, testY))                       # add to percent for plotting
                if (converged(errors)):                                         # check for convergence
                    print("CONVERGED.", i, "|", myPercep.w)
                    print("PERCENTAGE CORRECT ON TEST SET:", testDataSet(testX, testY)*100)
                    break
                elif (i == n-1):
                    print("DID NOT CONVERGE.", i, "|", myPercep.w)
                    print("PERCENTAGE CORRECT ON TEST SET:", testDataSet(testX, testY)*100)
                print(i, "|", myPercep.w)
            plotWvsRaw(rawX, Y, myPercep.w)         # plot the data against the w
            plotErrors(errors)
            plotPercentageCorrect(percent)

myPercep = Perceptron()
main()
        
