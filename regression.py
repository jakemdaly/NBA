# Module for performing regression on data
import numpy
import matplotlib.pyplot as plt
from statistics import mean

def regression(dataframe_XY, alpha, num_iter, plot=False):

    # Extract X and Y variables from the dataframe
    X = dataframe_XY.iloc[:, 2:]
    X = X.values
    X = numpy.matrix(X)
    y = dataframe_XY.iloc[:, 1]
    y = y.values
    y = numpy.matrix(y)
    y = y.transpose()
    # Get how many training examples there are
    m = len(y)

    # Normalize the features
    [X_norm, mu, sigma] = featureNormalize(X)

    # Add Column of ones to X
    X = numpy.hstack((numpy.ones([m,1]), X_norm))

    # Initialize a theta matrix
    theta = numpy.zeros([numpy.shape(X)[1], 1])
    theta = numpy.matrix(theta)

    # Run gradient descent function
    [theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iter)

    # Plot the convergence
    if plot:
        plt.ylabel('Model error')
        plt.xlabel('No. iterations of gradient descent')
        plt.title("Iterative weights/bias optimization ('Year1' data)")
        plt.plot(J_history, 'go')
        plt.show()
    theta = numpy.transpose(theta)[0]

    projections = [numpy.sum(numpy.multiply(theta,x)) for x in X]

    return [numpy.asarray(theta), X, projections, mu, sigma]

def featureNormalize(X):
    X_norm = X;
    mu = numpy.zeros([1, numpy.shape(X)[1]])
    sigma = numpy.zeros([1, numpy.shape(X)[1]])

    for i in range(0, (numpy.shape(X)[1])):
        mu[0,i] = numpy.mean(X[:,i])
        sigma[0,i] = numpy.std(X[:,i])
        X_norm[:,i] = (X[:,i]-mu[0,i])/sigma[0,i]

    return [X_norm, mu, sigma]

def computeCostMulti(X, y, theta):
    m = len(y)

    J = 0

    for i in range(0,m):
        theta_insert = numpy.squeeze(numpy.asarray(numpy.transpose(theta)))
        X_insert = numpy.squeeze(numpy.asarray(X[i,:]))
        J = J + 1/(2*m)*numpy.square(numpy.dot(theta_insert, X_insert)-y[i])

    return J

def gradientDescentMulti(X, y, theta, alpha, num_iter):
    m = len(y)
    J_history = numpy.zeros([num_iter, 1])
    J_history = numpy.matrix(J_history)
    theta_temp = theta

    for iter in range(0,num_iter):

        for ind in range(0,m):

            theta_insert = numpy.squeeze(numpy.asarray(numpy.transpose(theta)))
            X_insert = numpy.squeeze(numpy.asarray(X[ind,:]))
            theta_temp = theta_temp-alpha*(1/m)*(numpy.dot(theta_insert, X_insert)-y[ind]).item(0)*numpy.transpose(X[ind,:])

        theta = theta_temp
        J_history[iter] = computeCostMulti(X, y, theta)

    return [theta, J_history]

def theta_test(theta_vec, training_ex):

    y_predicted = sum(a*b for a,b in zip(theta_vec, training_ex))
    return y_predicted
    # print("Predicted: {}, Actual {}".format(y_predicted, training_ex[0]))

def unnormalize_theta(theta_vec, associated_data_block):
    #associated data block is entire block of training sets across all features

    num_features = len(associated_data_block[0])
    averages_by_feature = []

    for feat in range(0,num_features):
        data_for_feature = [da[feat] for da in associated_data_block[:]]
        averages_by_feature.append(mean(data_for_feature))

    unNorm_theta = [a*b for a,b in zip(theta_vec, [1] + averages_by_feature)]

    return unNorm_theta

