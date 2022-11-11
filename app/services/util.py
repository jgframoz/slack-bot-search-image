import random
import string


class UtilService:

    @staticmethod
    def create_random_string(len: int):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(len))
