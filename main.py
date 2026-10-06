import os
import time
import config
from solver import BruteForceSolver

def main():
    # 1. Визначення кількості ядер процесора
    n_cpu = os.cpu_count() or 1
    print(f"Кількість процесорних ядер ПК (n_cpu): {n_cpu}")

    solver = BruteForceSolver(
        charset=config.CHARSET,
        length=config.PASSWORD_LENGTH,
        hash_name=config.HASH_NAME,
        target_hash=config.TARGET_HASH
    )

    # 2b. Мультипроцесорний підбір
    print(f"\n[Запуск] Мультипроцесорний підбір ({n_cpu} процесів)...")
    start = time.perf_counter()
    multi_res = solver.solve_multi(n_processes=n_cpu)
    multi_time = time.perf_counter() - start

    print(f"Час мультипроцесорного виконання: {multi_time:.2f} сек. ({multi_time/60:.2f} хв.)")
    print(f"Знайдений пароль: {multi_res}")

    # 2a. Однопроцесорний підбір (за потреби викладач може попросити зауважити різницю)
    # Зверніть увагу: однопроцесорний запуск на 9.5 млрд комбінацій може тривати 2-3 години,
    # тому спочатку перевірте мультипроцесорний запуск!

if __name__ == "__main__":
    main()