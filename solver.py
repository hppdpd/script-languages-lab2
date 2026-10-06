import itertools
import multiprocessing as mp
from hasher import PasswordHasher

def _worker_task(prefixes, charset, length, hash_name, target_hash, stop_event, result_queue):
    """Функція-воркер для окремого процесу."""
    hasher = PasswordHasher(hash_name, target_hash)
    for prefix in prefixes:
        for suffix in itertools.product(charset, repeat=length - 1):
            if stop_event.is_set():
                return
            candidate = prefix + "".join(suffix)
            if hasher.check(candidate):
                result_queue.put(candidate)
                stop_event.set()  # Сигнал іншим процесам про зупинку
                return

class BruteForceSolver:
    """Реалізує однопроцесорний та мультипроцесорний підбір пароля."""
    def __init__(self, charset: str, length: int, hash_name: str, target_hash: str):
        self.charset = charset
        self.length = length
        self.hash_name = hash_name
        self.target_hash = target_hash

    def solve_single(self) -> str | None:
        """Однопроцесорний підбір."""
        hasher = PasswordHasher(self.hash_name, self.target_hash)
        for candidate_tuple in itertools.product(self.charset, repeat=self.length):
            candidate = "".join(candidate_tuple)
            if hasher.check(candidate):
                return candidate
        return None

    def solve_multi(self, n_processes: int) -> str | None:
        """Мультипроцесорний підбір з негайною зупинкою після знаходження."""
        stop_event = mp.Event()
        result_queue = mp.Queue()

        # Розподіляємо стартові символи між процесами
        prefixes = list(self.charset)
        chunk_size = max(1, len(prefixes) // n_processes)
        chunks = [prefixes[i:i + chunk_size] for i in range(0, len(prefixes), chunk_size)]

        processes = []
        for chunk in chunks:
            p = mp.Process(
                target=_worker_task,
                args=(chunk, self.charset, self.length, self.hash_name, self.target_hash, stop_event, result_queue)
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        if not result_queue.empty():
            return result_queue.get()
        return None