class ApiCheckError(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code

class UnsupportedCountryError(ApiCheckError):
    def __init__(self, message: str, country: str):
        super().__init__(message, 400)
        self.country = country

class AuthenticationError(ApiCheckError):
    def __init__(self):
        super().__init__("Invalid API key", 401)

class RateLimitError(ApiCheckError):
    def __init__(self, retry_after: int | None = None):
        super().__init__("Rate limit exceeded", 429)
        self.retry_after = retry_after
