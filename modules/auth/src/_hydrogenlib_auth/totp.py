class TOTP:
    def __init__(self, key, digits=6, period=30):
        self.key = key
        self.digits = digits
        self.period = period