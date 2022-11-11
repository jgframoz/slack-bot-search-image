class LogService:
    @staticmethod
    def log(message):
        """
        Just a tempporary fix, ECS ignores prints without flush
        """
        print(message, flush=True)