import os

class Config:
    def __init__(self):
        """Initialize configuration with default settings."""
        self.botApi = os.getenv("botApi", "8271648321:AAEHNsxUCmiD4q6vpGZwsLPnZ1Hy3rnKOPE") # botApi: get this from #BotFather on telegram
        self.baseUrl = os.getenv("baseUrl", "https://erp.saitm.ac.in") # base url of college erp site (you can visit https://erp.saitm.ac.in)
        self.authorId = list(map(int, os.getenv("authorId", "8132481394 5679740685").split())) # telegram user_id of all the admins of the bot
        self.emailId = os.getenv("emailId", "codexsaitm@gmail.com") # official notify mail of saitm codex club
        self.emailPass = os.getenv("emailPass", "wdme lvzb zrta puar") # emails pass for sending emails to students using smtp server
        self.smtpServer = os.getenv("smtpServer", "smtp.gmail.com") # smtp server (helps in sending emails to students)
        self.smtpPort = int(os.getenv("smtpPort", "587")) # smtp server port to send request to the server
        self.loggerId = int(os.getenv("loggerId", "-1003607718085")) # you telegram logger group id