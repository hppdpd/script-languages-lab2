import hashlib

class PasswordHasher:
    """Відповідає за кодування символів та порівняння хешів."""
    def __init__(self, hash_name: str, target_hash: str):
        self.hash_name = hash_name
        self.target_hash = target_hash.strip().lower()

    def check(self, candidate: str) -> bool:
        """Повертає True, якщо хеш кандидата співпадає з цільовим."""
        candidate_hash = hashlib.new(self.hash_name, candidate.encode('utf-8')).hexdigest()
        return candidate_hash == self.target_hash