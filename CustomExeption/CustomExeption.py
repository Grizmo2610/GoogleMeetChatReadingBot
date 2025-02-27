class LimitReach(Exception):
    def __init__(self, message="Limit message approach!"):
        super().__init__(message)