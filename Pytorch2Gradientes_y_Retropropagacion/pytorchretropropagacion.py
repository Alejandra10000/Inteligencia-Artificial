# -*- coding: utf-8 -*-
"""Pytorchretropropagacion.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13W4qMbpN8Br4bkWDH2OxQFC7w9VF8MDl
"""

import torch

x = torch.tensor(1.0)
y = torch.tensor(2.0)

# Tensor a optimizar -> requires_grad=True
w = torch.tensor(1.0, requires_grad=True)

# Evaluación cálculo de costo
y_predicted = w * x
loss = (y_predicted - y) ** 2
print(loss)

# Retropropagación para calcular gradiente
loss.backward()
print(w.grad)

# Nuevos coeficientes, repetir evaluación y retropropagación
with torch.no_grad():
    w -= 0.01 * w.grad
    w.grad.zero_()

# Repetir los pasos anteriores según sea necesario