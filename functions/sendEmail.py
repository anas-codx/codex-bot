import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import User
from internal import Config
from internal import logger

async def sendmail(subject: str, body: str, message):
    """Broadcast an email to all students with valid email addresses."""
    # Get all student emails from the database
    emails = await User.filter(student_mail__isnull=False).values_list(
        "student_mail", flat=True
    )
    total_emails = len(emails)
    sent_count = 0
    try:
        logger.info(f"Total emails found: {total_emails}. Starting broadcast...")
        await message.answer(
            text=f"Total emails found: {total_emails}. Starting broadcast...",
            parse_mode="html",
        )
        server = smtplib.SMTP(Config().smtpServer, Config().smtpPort) # config the smtp server for sending emails
        server.starttls()
        server.login(Config().emailId, Config().emailPass)
        for email in emails:
            msg = MIMEMultipart()
            msg["From"] = Config().emailId
            msg["To"] = email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            server.sendmail(Config().emailId, email, msg.as_string())
            sent_count += 1
        server.quit() # after sending all the emails server will quit
        logger.info(f"Email sent successfully!\n\nTotal emails: {total_emails}\nSuccessfully sent: {sent_count}")
        await message.answer(
            text=f"Email sent successfully!\n\nTotal emails: {total_emails}\nSuccessfully sent: {sent_count}",
            parse_mode="html",
        )
    except Exception as e:
        logger.error(e)