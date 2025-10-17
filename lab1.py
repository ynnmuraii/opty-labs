import math

def f(x):
    return (x - 3.0)**2 + 4.0

x_analytic = 3.0
f_analytic = f(x_analytic)
print("АНАЛИТИЧЕСКИ: минимум в x = {:.6f}, f = {:.6f}\n".format(
    x_analytic, f_analytic))


def dichotomy(a, b, delta=1e-5, eps=1e-6):
    left, right = float(a), float(b)
    count = 0  
    while (right - left) > delta:
        x1 = 0.5 * (left + right - eps)
        x2 = 0.5 * (left + right + eps)
        f1 = f(x1)
        f2 = f(x2)
        count += 2
        if f1 < f2:
            right = x2
        else:
            left = x1
        if right - left <= 0:
            break
    x_min = 0.5 * (left + right)
    return {"x_min": x_min, "f_min": f(x_min), "count": count,
            "left": left, "right": right, "error": right - left}


def golden_section(a, b, delta=1e-5):
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    resphi = 2.0 - phi
    left, right = float(a), float(b)
 
    x1 = left + resphi * (right - left)
    x2 = right - resphi * (right - left)
    f1 = f(x1)
    f2 = f(x2)
    count = 2
    while (right - left) > delta:
        if f1 < f2:
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
    x_min = 0.5 * (left + right)
    return {"x_min": x_min, "f_min": f(x_min), "count": count,
            "left": left, "right": right, "error": right - left}


def fibonacci_method(a, b, N):
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

    for i in range(1, r-2):
        if f1 <= f2:
            right = x2
            x2, f2 = x1, f1
            x1 = left + (F[r-i-2] / F[r-i]) * (right - left)
            f1 = f(x1)
        else:
            left = x1
            x1, f1 = x2, f2
            x2 = left + (F[r-i-1] / F[r-i]) * (right - left)
            f2 = f(x2)
        count+=1
    if f1 > f2:
        left = x1
        x1 = x2
        x2 = left + (right - left)/2
        f1 = f2
        f2 = f(x2)
    else:
        right = x2
        x2 = x1
        x1 = left + (right - left)/2
        f2 = f1
        f1 = f(x1)
    if f1 <= f2:
        right = x2
    else:
        left = x1
    count += 1


    x_min = 0.5 * (left + right)
    return {
        "x_min": x_min,
        "f_min": f(x_min),
        "count": count,
        "left": left,
        "right": right,
        "error": right - left
    }

if __name__ == "__main__":
    a, b = 0.0, 10.0
    delta = 1e-5

    dich = dichotomy(a, b, delta=delta, eps=1e-6)
    gold = golden_section(0, 10, delta)
    fib = fibonacci_method(0, 10, N=gold["count"])

    print("МЕТОД ДИХОТОМИИ:")
    print(f"x ≈ {dich['x_min']:.8f}, f(x) ≈ {dich['f_min']:.8f}")
    print(
        f"Вычислений f(x): {dich['count']}, Интервал: [{dich['left']:.8f}, {dich['right']:.8f}], Погрешность: {dich['error']:.3e}\n")

    print("МЕТОД ЗОЛОТОГО СЕЧЕНИЯ:")
    print(f"x ≈ {gold['x_min']:.8f}, f(x) ≈ {gold['f_min']:.8f}")
    print(
        f"Вычислений f(x): {gold['count']}, Интервал: [{gold['left']:.8f}, {gold['right']:.8f}], Погрешность: {gold['error']:.3e}\n")

    print("МЕТОД ФИБОНАЧЧИ (с тем же числом измерений, что и у З.С.):")
    print(f"x ≈ {fib['x_min']:.8f}, f(x) ≈ {fib['f_min']:.8f}")
    print(
        f"Вычислений f(x): {fib['count']}, Интервал: [{fib['left']:.8f}, {fib['right']:.8f}], Погрешность: {fib['error']:.3e}\n")
    
