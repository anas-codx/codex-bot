import requests
from aiogram import html
from bs4 import BeautifulSoup
from internal import logger, Config
from models import User
from functions import dashboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Define headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

loginBtn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Login', callback_data='btn_login')
        ]
    ]
)

async def login(username: str, password: str, message):
    """
    Handle user login by authenticating against the website,
    fetching student profile details, and storing them in the database.
    """
    user_id = message.from_user.id
    logger.info(f"User - {user_id} Started Login...")
    session = requests.Session()
    try:
        # Get login page and CSRF token
        response = session.get(f"{Config().baseUrl}/account/login", headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        tokeninput = soup.find("input", {"name": "__RequestVerificationToken"})
        token = tokeninput["value"] if tokeninput else None
        if not token:
            await message.answer(
                text=f"The bot encountered an error while processing your request.\nPlease try again!\nIf the issue persists even after retrying, you may report it by using the /start command and selecting {html.bold('Report Issue')} from the menu.",
                reply_markup=loginBtn,
                parse_mode="html",
            )
            logger.error("Could not find CSRF token. Check the form or page structure.")
            return None
        payload = {
            "email": username,
            "password": password,
            "__RequestVerificationToken": token,
            "ReturnUrl": "", # can be None
        }
        # Submit login form
        loginresponse = session.post(f"{Config().baseUrl}/account/login", data=payload, headers=headers)
        loginresponse.raise_for_status()
        # Check login success
        if "logout" in loginresponse.text.lower() or "dashboard" in loginresponse.text.lower():
            pfresponse = session.get(f"{Config().baseUrl}/StudentProfile/StudentProfileUpdateRequest", headers=headers)
            pfresponse.raise_for_status()
            soup = BeautifulSoup(pfresponse.text, "html.parser")
            details = {}
            for div in soup.select(".student-content, .Parent-content"):
                spans = div.find_all("span")
                if len(spans) >= 2:
                    key = spans[0].get_text(strip=True).replace(" :", "")
                    value = spans[1].get_text(strip=True)
                    details[key] = value
                    # Save user to database
            await User.create(
                telegram_id=user_id,
                student_name=details.get('Student Name', 'N/A'),
                roll_number=details.get('Enrollemnt No', 'N/A'),
                branch = details.get('Program Name', 'N/A'),
                session = details.get("Session Name", "N/A"),
                student_mail = details.get('EmailID', 'N/A'),
            )
            logger.info(f"User - {user_id} Logged in successfully.")
            await dashboard(user_id, message)
        else:
            await message.answer(
                text=f"Login failed. Please verify your {html.bold('Username')} and {html.bold('Password')} and try again.",
                reply_markup=loginBtn,
                parse_mode="html",
            )
            logger.error(f"Login failed. Invalid credentials or token issue for user - User ID: {user_id}")
            return None
    except requests.RequestException as e:
        await message.answer(
            text=f"The bot encountered an error while processing your request.\nPlease try again!\nIf the issue persists even after retrying, you may report it by using the /start command and selecting {html.bold('Report Issue')} from the menu.",
            reply_markup=loginBtn,
            parse_mode="html",
            )
        logger.error(f"Network error encountered: {e}")
        return None