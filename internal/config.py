import os

class Config:
    def __init__(self):
        """Initialize configuration with default settings."""
        self.botApi = os.getenv("botApi", "")
        self.baseUrl = os.getenv("baseUrl", "https://erp.saitm.ac.in")
        self.authorId = list(map(int, os.getenv("authorId", "8132481394").split()))
        self.emailId = os.getenv("emailId", "codexsaitm@gmail.com")
        self.emailPass = os.getenv("emailPass", "")
        self.smtpServer = os.getenv("smtpServer", "smtp.gmail.com")
        self.smtpPort = int(os.getenv("smtpPort", "587"))