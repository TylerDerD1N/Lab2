# -*- coding: utf-8 -*-
"""
Лабораторная работа № 2. Вариант 12.
Файл: lab2.py

Сравнение сортировки пузырьком (с флагом) и сортировки вставками.

Вариант 12:
    Размеры n: 500, 1000, 2000, 3000, 4000
    Тип данных: R (случайные целые числа)
    Диапазон: [-10000; 10000]
    Повторов k: 5
    Доп. задание: М7 (устойчивость на записях вида (фамилия_клиента, сумма_заказа))
"""

import random
import statistics
import time
import csv
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Параметры варианта 12
# ----------------------------------------------------------------------
SIZES = [500, 1000, 2000, 3000, 4000]
DATA_KIND = "random"
DATA_LO = -10_000
DATA_HI = 10_000
REPEATS = 5


# ----------------------------------------------------------------------
# Генерация данных
# ----------------------------------------------------------------------
def generate_data(n, lo=DATA_LO, hi=DATA_HI, seed=42):
    """Генерация случайных целочисленных массивов (R)."""
    rng = random.Random(seed + n)
    return [rng.randint(lo, hi) for _ in range(n)]


def generate_records(n, seed=42):
    """Генерация записей (фамилия_клиента, сумма_заказа) для М7."""
    rng = random.Random(seed + n)
    names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Попов"]
    # Генерируем записи, специально создавая дубликаты сумм для проверки устойчивости
    records = [(rng.choice(names), rng.randint(1, 100)) for _ in range(n)]
    return records


# ----------------------------------------------------------------------
# Алгоритмы сортировки (с поддержкой key-функции для М7)
# ----------------------------------------------------------------------
def bubble_sort(arr, key=None):
    """Сортировка пузырьком с флагом досрочного выхода."""
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            val1 = a[j] if key is None else key(a[j])
            val2 = a[j + 1] if key is None else key(a[j + 1])
            if val1 > val2:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(arr, key=None):
    """Сортировка вставками."""
    a = arr.copy()
    for i in range(1, len(a)):
        key_item = a[i]
        key_val = key_item if key is None else key(key_item)
        j = i - 1
        while j >= 0:
            curr_val = a[j] if key is None else key(a[j])
            if curr_val > key_val:  # Строгое неравенство обеспечивает устойчивость
                a[j + 1] = a[j]
                j -= 1
            else:
                break
        a[j + 1] = key_item
    return a


# ----------------------------------------------------------------------
# Замер времени
# ----------------------------------------------------------------------
def measure(sort_func, data, repeats=REPEATS, key=None):
    """Возвращает медианное время работы sort_func на данных data, с."""
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        result = sort_func(data, key=key)
        times.append(time.perf_counter() - start)
        assert result == sorted(data, key=key), f"{sort_func.__name__}: ошибка сортировки"
    return statistics.median(times)


# ----------------------------------------------------------------------
# Основной эксперимент
# ----------------------------------------------------------------------
def run_experiment():
    algorithms = {"Bubble": bubble_sort, "Insertion": insertion_sort}
    results = {name: [] for name in algorithms}

    print("=" * 70)
    print("Лабораторная работа № 2. Вариант 12 (файл lab2.py)")
    print(f"Размеры: {SIZES}, тип данных: R, диапазон: [{DATA_LO}; {DATA_HI}]")
    print("=" * 70)
    print(f"{'n':>6} | {'Пузырьком (с)':>16} | {'Вставками (с)':>16} | {'Отношение':>10}")
    print("-" * 60)

    for n in SIZES:
        data = generate_data(n)
        row_times = {}
        for name, func in algorithms.items():
            t = measure(func, data, REPEATS)
            results[name].append(t)
            row_times[name] = t

        ratio = row_times["Bubble"] / row_times["Insertion"] if row_times["Insertion"] > 0 else 0
        print(f"{n:>6} | {row_times['Bubble']:>16.4f} | {row_times['Insertion']:>16.4f} | {ratio:>10.2f}")

    # Сохранение результатов в CSV
    with open("lab2_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "bubble_time", "insertion_time"])
        for i, n in enumerate(SIZES):
            writer.writerow([n, results["Bubble"][i], results["Insertion"][i]])
    print("\nРезультаты сохранены в lab2_results.csv")

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(SIZES, results["Bubble"], marker='o', label='Сортировка пузырьком')
    plt.plot(SIZES, results["Insertion"], marker='s', label='Сортировка вставками')
    plt.xlabel("Размер массива n")
    plt.ylabel("Время, с")
    plt.title("Зависимость времени сортировки от n (Вариант 12, R)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig("lab2_plot.png", dpi=150)
    print("График сохранён в lab2_plot.png")


# ----------------------------------------------------------------------
# Дополнительное задание М7: Устойчивость
# ----------------------------------------------------------------------
def run_m7_stability():
    print("\n" + "=" * 70)
    print("Дополнительное задание М7: Демонстрация устойчивости")
    print("=" * 70)

    # Берем небольшой массив для наглядности
    n = 10
    records = generate_records(n)

    # Ключ сортировки - сумма заказа (второй элемент кортежа)
    key_func = lambda x: x[1]

    print("Исходный массив (Фамилия, Сумма):")
    for r in records:
        print(f"  {r}")

    bubble_res = bubble_sort(records, key=key_func)
    insert_res = insertion_sort(records, key=key_func)

    # Сохранение вывода в файл
    with open("lab2_m7_stability.txt", "w", encoding="utf-8") as f:
        f.write("Исходный массив:\n")
        for r in records:
            f.write(f"  {r}\n")
        f.write("\nРезультат сортировки пузырьком:\n")
        for r in bubble_res:
            f.write(f"  {r}\n")
        f.write("\nРезультат сортировки вставками:\n")
        for r in insert_res:
            f.write(f"  {r}\n")

    print("\nРезультат пузырьком (отсортировано по сумме):")
    for r in bubble_res:
        print(f"  {r}")

    print("\nРезультат вставками (отсортировано по сумме):")
    for r in insert_res:
        print(f"  {r}")

    print("\nВывод М7 сохранён в lab2_m7_stability.txt")

    # Проверка на устойчивость (сравнение с эталонной устойчивой сортировкой)
    # sorted() в Python использует Timsort, который является устойчивым.
    expected = sorted(records, key=key_func)
    assert bubble_res == expected, "Сортировка пузырьком НЕ устойчива!"
    assert insert_res == expected, "Сортировка вставками НЕ устойчива!"
    print("Проверка пройдена: обе сортировки УСТОЙЧИВЫ (порядок клиентов с одинаковой суммой сохранен).")


if __name__ == "__main__":
    run_experiment()
    run_m7_stability()