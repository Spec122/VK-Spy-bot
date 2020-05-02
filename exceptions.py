class NoCredentials(Exception):
    def __str__(self):
        return "No data for login"
