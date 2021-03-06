import numpy as np
from sympy import diff, Symbol, Matrix

# матрицы коэффициентов
def gen_biases(n=3):
    A = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    b = np.array([1, 0, 1]).reshape((1, 3))
    return A, b


# возвращает значение функции в точке
def func_eval(x, A, b):
    x = x.reshape((1, n))
    return (x @ A @ x.T + b @ x.T)[0, 0]


# получает градиент в виде формулы
def get_gradient(A, b, n=3):
    x = Matrix([Symbol('x[' + str(i) + ']') for i in range(n)])
    f = x.T * A * x + b * x
    return [diff(f, x[i])[0, 0] for i in range(n)]


# подставляет численные координаты вектора вместо переменных вида 'x[i]'
# в формулу градиента и возвращает строку вида 2*1+2*2+3*1
def replacer(x, s):
    for i in range(len(x)):
        s = s.replace('x[' + str(i) + ']', str(x[i]))
    return s


# считает значение градиента в точке
def eval_gradient(x_0, A, b, n=3):
    gradient = get_gradient(A, b)
    return np.array([eval(replacer(x_0, str(gradient[i]))) for i in range(n)])


# зеркальный спуск
def gradientDescent(x_0, lamda, A, b, eps=1e-30, maxStep=1000):
    points = []
    points.append(x_0)
    x = np.copy(x_0)
    step = 0
    while (step == 0 or (abs(func_eval(points[-1], A, b) - func_eval(points[-2], A, b)) >= eps) and step <= maxStep):
        step += 1
        g = eval_gradient(x, A, b)
        y = x * np.exp(-lamda * g)
        x = y / np.linalg.norm((y), ord=1)
        points.append(x)
    return x, np.asarray(points)


n = 3
x_0 = np.array([0.5, 0.5, 0.5], dtype=np.float64)
A, b = gen_biases()
min_pmt, points = gradientDescent(x_0, lamda=5 , A=A, b=b)


# ответ и шаги спуска
print(min_pmt)
print(points)