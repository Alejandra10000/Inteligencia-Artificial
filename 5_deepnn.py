# -*- coding: utf-8 -*-
"""5_deepNN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n_kyzFQM-nncuS4oydj3oi_u5mKAN7U1
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numba import jit

# Leer imágenes de números escritos a mano
data = pd.read_csv('train.csv')
data = np.array(data)
m, n = data.shape
print("Número de imágenes =", m)
print("Número de píxeles =", n)
np.random.shuffle(data)

# Separar imágenes en dev (prueba) y train (entrenamiento)
data_dev = data[0:1000].T
Y_dev = data_dev[0]
X_dev = data_dev[1:n]
X_dev = X_dev / 255.

data_train = data[1000:m].T
Y_train = data_train[0]
X_train = data_train[1:n]
X_train = X_train / 255.
_, m_train = X_train.shape

# Inicialización de parámetros
@jit(nopython=True)
def init_params():
    W = []
    b = []
    m = np.array([784, 10, 10])
    n = np.array([10, 10, 10])
    capas = len(m)
    for i in range(capas):
        W.append(np.random.rand(n[i], m[i]) - 0.5)
        b.append(np.random.rand(n[i], 1) - 0.5)
    return W, b

# Función ReLU
def ReLU(Z):
    return np.maximum(Z, 0)

# Función softmax
def softmax(Z):
    A = np.exp(Z) / sum(np.exp(Z))
    return A

# Evaluar la red (forward propagation)
def forward_prop(W, b, X):
    A = []
    Z = []
    A.append(X)
    for i in range(len(W)):
        Z.append(W[i].dot(A[-1]) + b[i])
        if i < len(W) - 1:
            A.append(ReLU(Z[-1]))
        else:
            A.append(softmax(Z[-1]))
    return Z, A

# Derivada de la ReLU
def ReLU_deriv(Z):
    return Z > 0

# Codificación de la clasificación
def one_hot(Y):
    one_hot_Y = np.zeros((Y.size, Y.max() + 1))
    one_hot_Y[np.arange(Y.size), Y] = 1
    return one_hot_Y.T

# Cálculo numérico del gradiente
def backward_prop(Z, A, W, X, Y):
    dW = []
    db = []
    m = X.shape[1]
    n = len(W) - 1
    one_hot_Y = one_hot(Y)
    dZ = A[n] - one_hot_Y
    dW.append(1 / m * dZ.dot(A[n-1].T))
    db.append(1 / m * np.sum(dZ, axis=1, keepdims=True))
    for i in range(n - 1, 0, -1):
        dZ = W[i + 1].T.dot(dZ) * ReLU_deriv(Z[i])
        dW.append(1 / m * dZ.dot(A[i-1].T))
        db.append(1 / m * np.sum(dZ, axis=1, keepdims=True))
    dZ = W[1].T.dot(dZ) * ReLU_deriv(Z[0])
    dW.append(1 / m * dZ.dot(X.T))
    db.append(1 / m * np.sum(dZ, axis=1, keepdims=True))
    dW.reverse()
    db.reverse()
    return dW, db

# Mejorar parámetros
def update_params(W, b, dW, db, alpha):
    for i in range(len(W)):
        W[i] = W[i] - alpha * dW[i]
        b[i] = b[i] - alpha * db[i]
    return W, b

# Predicciones
@jit(nopython=True)
def get_predictions(A2):
    return np.argmax(A2, axis=0)

# Precisión
@jit(nopython=True)
def get_accuracy(predictions, Y):
    return np.sum(predictions == Y) / Y.size

# Descenso de gradiente
def gradient_descent(X, Y, alpha, iterations):
    W, b = init_params()
    for i in range(iterations):
        Z, A = forward_prop(W, b, X)
        dW, db = backward_prop(Z, A, W, X, Y)
        W, b = update_params(W, b, dW, db, alpha)
        if i % 10 == 0:
            print("Iteración:", i)
            predictions = get_predictions(A[-1])
            print(get_accuracy(predictions, Y))
    return W, b

# Entrenar la red
W, b = gradient_descent(X_train, Y_train, 0.10, 1000)

# Hacer predicciones
def make_predictions(X, W, b):
    _, A = forward_prop(W, b, X)
    predictions = get_predictions(A[-1])
    return predictions

# Evaluar predicciones
def test_prediction(index, W, b):
    current_image = X_train[:, index, None]
    prediction = make_predictions(X_train[:, index, None], W, b)
    label = Y_train[index]
    print("Prediction:", prediction)
    print("Label:", label)
    current_image = current_image.reshape((28, 28)) * 255
    plt.gray()
    plt.imshow(current_image, interpolation='nearest')
    plt.show()

for i in range(20):
    test_prediction(i, W, b)