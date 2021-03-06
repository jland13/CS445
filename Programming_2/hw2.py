import numpy as np
import math

MINSTD = 0.0001
NFEATURES = 57


def main():
    """Main entry point for running naive Bayes' model on the UCI Spambase data.

    Calls functions used to create and initialize train and test data, create
     probablistic model from train data, run naive Bayesian model on test data,
      and output/compute confusion matrix, accuracy, precision and accuracy.

    Params:
        None

    Returns:
        None

    Raises:
        None
    """
    print("Welcome to Programming #2")

    # 1. Create training and test set
    print("Creating train and test data sets...")
    infile = 'spambase_data.csv'
    train, test = initData(infile)

    # 2. Create probabilistic model
    print("Creating probabilistic model from training data...")
    p, μ, σ = probmodel(train)

    # 3. Run Bayesian learning model
    print("Running naive Bayesian learning model on test data...\n")
    aclass = nblm(train, p, μ, σ)
    fclass = classify(aclass)

    # Output confusion matrix
    outfile = 'confmat.csv'
    confmat = getconfmat(train[:, NFEATURES], fclass, outfile)

    tn = confmat[0, 0]
    tp = confmat[1, 1]
    fn = confmat[1, 0]
    fp = confmat[0, 1]

    # Compute accuracy
    accuracy = (tp + tn) / (tn + tp + fn + fp)
    print("accuracy = ", accuracy)

    # Compute precision
    precision = tp / (tp + fp)
    print("precision = ", precision)

    # Compute recall
    recall = tp / (tp + fn)
    print("recall = ", recall)

    return 0


def classify(aclass):
    """Classifies test data using argmax(P(x_i | class))

    Uses passed in array of classifications for each training example given the
     probabilities given a class and returns the computed classification using
     the argmax of the two possible classifications (0, 1).

    Params:
       aclass: Two dimensional Numpy array of floats representing the probabil-
        ities given each possible class.

    Returns:
       fclass: One dimensional Numpy array containing the computed classifiica-
        tions using the argmax of the probabilities in the aclass array.

    Raises:
        None
    """
    fclass = np.zeros((aclass.shape[0]))
    for i in range(aclass.shape[0]):
        if aclass[i, 0] > aclass[i, 1]:
            fclass[i] = 0
        else:
            fclass[i] = 1
    return fclass


def example():
    """Main entry point for running naive Bayes' model on the simple example
     from the course slides.

    Calls functions used to create and initialize train and test data, create
     probablistic model from train data, run naive Bayesian model on test data,
      and output/compute confusion matrix, accuracy, precision and accuracy.

    Params:
        None

    Returns:
        None

    Raises:
        None
    """
    extrain = np.array([[3.0, 5.1, 1.0],
                       [4.1, 6.3, 1.0],
                       [7.2, 9.8, 1.0],
                       [2.0, 1.1, -1.0],
                       [4.1, 2.0, -1.0],
                       [8.1, 9.4, -1.0]])

    p = [0.5, 0.5]
    μ = np.zeros((6, 2))
    σ = np.zeros((6, 2))
    μ[0] = np.mean(extrain[3:, :2], axis=0, dtype=np.float64)
    μ[1] = np.mean(extrain[:3, :2], axis=0, dtype=np.float64)
    σ[0] = np.std(extrain[3:, :2], axis=0, dtype=np.float64)
    σ[1] = np.std(extrain[:3, :2], axis=0, dtype=np.float64)

    extest = np.array([5.2, 6.3])
    exclass = np.zeros((2, 2))

    for i in range(extest.size):
        exclass[i, 0] = ndist(extest[i], μ[i, 0], σ[i, 0])
        exclass[i, 1] = ndist(extest[i], μ[i, 1], σ[i, 1])

    posex = p[1] * exclass[0, 0] * exclass[1, 0]
    negex = p[0] * exclass[0, 1] * exclass[1, 1]

    if posex > negex:
        print("Example class = 1")
    else:
        print("Example class = 0")


def getconfmat(labels, ys, fname):
    """Computes, outputs and returns the classification confusion matrix.

    Performs the calculations needed to output a csv format confusion matrix
     containing the values representing the ratio of predicted and output class-
     ifications.


    Arguments:
        labels: An array of integer values containing the labels/target classif-
         ications for each data set.
        ys: An array of integer values containing the predicted classification
         for each data set.
        fname: String used to save the csv file to.

    Returns:
        confmat: An 2x2 NumPy matrix containing the confusion matrix for the
         classifications.

    Raises:
        None
    """

    # Confusion matrix
    confmat = np.zeros((2, 2))
    for i in range(labels.size):
        l = int(labels[i])
        y = int(ys[i])
        confmat[l, y] += 1

    confmatfile = f'''{fname}.csv'''
    np.savetxt(confmatfile, confmat, delimiter=',')

    return confmat


def initData(infile):
    """Initializes the train and test data.

    Uses the passed in filename to open and split up and return the UCI Spambase
     data files into a train and test set.

    Params:
        infile: A string representing the filename of the UCI Spambase data.

    Return:
        test: A NumPy array containing float values representing the examples
         and features of the test data set.
        train: A NumPy array containing float values representing the examples
         and features of the train data set.

    Raises:
        None
    """
    data = np.loadtxt(infile, delimiter=',')
    spam = data[:1813]
    nspam = data[1813:]
    train = spam[:int(spam.shape[0] / 2) + 1, :]
    train = np.append(train, nspam[:int(nspam.shape[0] / 2), :], axis=0)
    test = spam[int(spam.shape[0] / 2) + 1:, :]
    test = np.append(test, nspam[int(nspam.shape[0] / 2):, :], axis=0)

    return train, test


def nblm(test, p, μ, σ):
    """Runs Naive Bayes Learning Algorithm on the test data.

    Uses p, μ and σ to perform the Naive Bayesian Learning algorithm on the test
     data to calculate the probability of each feature given each class.

    Params:
        test: A NumPy array containing float values representing the examples
         and features of the train data set.
        p: Tuple of floats representing the probabilities of each class.
        μ: A NumPy matrix of floats representing the mean for each feature given
         each class.
        σ: A NumPy matrix of floats  representing the standard deviation for
         each features given each class.

    Returns:
        aclass: Two dimensional Numpy array of floats representing the probabil-
         ities given each possible class.

    Raises:
        None
    """
    tclass = np.zeros((test.shape[0], NFEATURES, 2))
    aclass = np.ones((test.shape[0], 2))
    aclass[:, 0] *= math.log2(p[0])
    aclass[:, 1] *= math.log2(p[1])

    for j in range(test.shape[0]):
        for i in range(NFEATURES):
            tclass[j, i, 0] = ndist(test[j, i], μ[i, 0], σ[i, 0])
            tclass[j, i, 1] = ndist(test[j, i], μ[i, 1], σ[i, 1])
            aclass[j, 0] += math.log2(tclass[j, i, 0])
            aclass[j, 1] += math.log2(tclass[j, i, 1])

    return aclass


def ndist(x, μ, σ):
    """Computes the probability using the Gaussian distribution.

    Uses x, μ and σ to compute the probability using the Gaussian naive Bayesian
     algorithm.

    Params:
        x: A float representing the current feature of the current example used
         to calculate the probability.
        μ: A NumPy matrix of floats representing the mean for each feature given
         each class.
        σ: A NumPy matrix of floats  representing the standard deviation for
         each features given each class.

    Returns:
        n: Float representing the result of the Gaussian distribution function,
         or 0.00000001 if n is less than.
    Raises:
        None
    """
    n = (1 / (math.sqrt(2 * math.pi) * σ)) * (math.exp(-1 * pow(x - μ, 2) /
                                                       (2 * pow(σ, 2))))

    if n == 0:
        return 0.0000001
    else:
        return n


def probmodel(train):
    """Creates a probabilistic model for the train data.

    Builds and returns a probabilistic model using the passed in train data

    Params:
        train: A NumPy array containing float values representing the examples
         and features of the train data set.

    Return:
        p: Tuple of floats representing the probabilities of each class.
        μ: A NumPy matrix of floats representing the mean for each feature given
         each class.
        σ: A NumPy matrix of floats  representing the standar deviation for each
         features given each class.

    Raises:
        None
    """
    p = [0, 0]

    class1 = np.sum(train[:, NFEATURES], axis=0, dtype=np.float64)
    p[0] = (train.shape[0] - class1) / train.shape[0]
    p[1] = class1 / train.shape[0]

    μ = np.zeros((NFEATURES, 2))
    σ = np.zeros((NFEATURES, 2))

    μ[:, 0] = np.mean(train[907:, :NFEATURES], axis=0, dtype=np.float64)
    μ[:, 1] = np.mean(train[:907, :NFEATURES], axis=0, dtype=np.float64)
    σ[:, 0] = np.std(train[907:, :NFEATURES], axis=0, dtype=np.float64)
    σ[:, 1] = np.std(train[:907, :NFEATURES], axis=0, dtype=np.float64)

    σ[:, 0] = np.where(σ[:NFEATURES, 0] == 0, MINSTD, σ[:, 0])
    σ[:, 1] = np.where(σ[:NFEATURES, 1] == 0, MINSTD, σ[:, 1])

    return p, μ, σ


if __name__ == '__main__':
    main()
#    example()