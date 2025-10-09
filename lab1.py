import math
import matplotlib.pyplot as plt
import numpy as np

""" Целевая функция (вариант 1)
f(x) = (x-3)^2 + 4, x in [0,10] 
"""

def f(x):
    return (x - 3.0)**2 + 4.0


# Аналитическое решение
x_analytic = 3.0
f_analytic = f(x_analytic)
print("АНАЛИТИЧЕСКИ: минимум в x = {:.6f}, f = {:.6f}\n".format(
    x_analytic, f_analytic))


def dichotomy(a, b, eps=1e-5, delta=1e-6):
    left, right = float(a), float(b)
    count = 0  # количество вычислений f
    # пока длина интервала больше eps
    while (right - left) > eps:
        mid = 0.5 * (left + right)
        x1 = mid - delta
        x2 = mid + delta
        f1 = f(x1)
        f2 = f(x2)
        count += 2
        if f1 < f2:
            right = x2
        else:
            left = x1
        # страховка от бесконечного цикла
        if right - left <= 0:
            break
    x_min = 0.5 * (left + right)
    return {"x_min": x_min, "f_min": f(x_min), "count": count,
            "left": left, "right": right, "error": right - left}


def golden_section(a, b, eps=1e-5):
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    resphi = 2.0 - phi
    left, right = float(a), float(b)
 
    x1 = left + resphi * (right - left)
    x2 = right - resphi * (right - left)
    f1 = f(x1)
    f2 = f(x2)
    count = 2
    while (right - left) > eps:
        if f1 < f2:
            # минимум в [left, x2]
            right = x2
            x2 = x1
            f2 = f1
            x1 = left + resphi * (right - left)
            f1 = f(x1)
            count += 1
        else:
            left = x1
            x1 = x2
            f1 = f2
            x2 = right - resphi * (right - left)
            f2 = f(x2)
            count += 1
        if right - left <= 0:
            break
    x_min = 0.5 * (left + right)
    return {"x_min": x_min, "f_min": f(x_min), "count": count,
            "left": left, "right": right, "error": right - left}


def fibonacci_method(a, b, N, eps=1e-5):
    if N < 2:
        raise ValueError("N must be >= 2")

    F = [1, 1]
    for i in range(2, N + 1):
        F.append(F[-1] + F[-2])

    left, right = float(a), float(b)
    r = N

    x1 = left + (F[r-2] / F[r]) * (right - left)
    x2 = left + (F[r-1] / F[r]) * (right - left)
    f1 = f(x1)
    f2 = f(x2)
    count = 2

    while r > 2 and (right - left) > eps:
        if f1 <= f2:
            right = x2
            x2, f2 = x1, f1
            r -= 1
            x1 = left + (F[r-2] / F[r]) * (right - left)
            f1 = f(x1)
            count += 1
        else:
            left = x1
            x1, f1 = x2, f2
            r -= 1
            x2 = left + (F[r-1] / F[r]) * (right - left)
            f2 = f(x2)
            count += 1

    x_min = 0.5 * (left + right)
    return {"x_min": x_min, "f_min": f(x_min),
            "count": count, "left": left, "right": right, "error": right - left}


if __name__ == "__main__":
    a, b = 0.0, 10.0
    eps = 1e-5

    dich = dichotomy(a, b, eps=eps, delta=1e-6)
    gold = golden_section(0, 10, eps=1e-5)
    fib = fibonacci_method(0, 10, N=gold["count"] + 1, eps=1e-5)

    print("МЕТОД ДИХОТОМИИ:")
    print(f"x ≈ {dich['x_min']:.8f}, f(x) ≈ {dich['f_min']:.8f}")
    print(f"Вычислений f(x): {dich['count']}, Интервал: [{dich['left']:.8f}, {dich['right']:.8f}], Погрешность: {dich['error']:.3e}\n")

    print("МЕТОД ЗОЛОТОГО СЕЧЕНИЯ:")
    print(f"x ≈ {gold['x_min']:.8f}, f(x) ≈ {gold['f_min']:.8f}")
    print(f"Вычислений f(x): {gold['count']}, Интервал: [{gold['left']:.8f}, {gold['right']:.8f}], Погрешность: {gold['error']:.3e}\n")

    print("МЕТОД ФИБОНАЧЧИ (с тем же числом измерений, что и у З.С.):")
    print(f"x ≈ {fib['x_min']:.8f}, f(x) ≈ {fib['f_min']:.8f}")
    print(f"Вычислений f(x): {fib['count']}, Интервал: [{fib['left']:.8f}, {fib['right']:.8f}], Погрешность: {fib['error']:.3e}\n")

    X = np.linspace(a, b, 500)
    Y = [f(x) for x in X]
    plt.figure(figsize=(9, 5))
    plt.plot(X, Y, label="f(x) = (x-3)^2 + 4", linewidth=1.2)
    plt.scatter([dich['x_min']], [dich['f_min']], s=60, label="Дихотомия")
    plt.scatter([gold['x_min']], [gold['f_min']],
                s=60, label="Золотое сечение")
    plt.scatter([fib['x_min']], [fib['f_min']], s=60, label="Фибоначчи")
    plt.scatter([x_analytic], [f_analytic], color='red',
                s=80, label="Аналитический минимум (x=3)")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Сравнение методов на f(x)=(x-3)^2+4")
    plt.grid(True)
    plt.legend()
    plt.show()
