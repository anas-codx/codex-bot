from aiogram import types, html, Router
from aiogram.filters import Command
from internal import logger
from models import User
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.functions.dashBoard import dashboard

router = Router()

# Inline keyboard
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Terms and Conditions',
                                 url="https://telegra.ph/Terms-and-Conditions-01-02-6")
        ],
        [
            InlineKeyboardButton(text='Login', callback_data="btn_login")
        ],
        [
            InlineKeyboardButton(text='Website', url="https://saitm.ac.in"),
            InlineKeyboardButton(text='Report Issue', url="https://t.me/CodeXSaitm")
        ],
        [
            InlineKeyboardButton(text='Help', callback_data="btn_help")
        ]
    ]
)

@router.message(Command("start"))
async def start_handler(message: types.Message):
    """Handles the /start command when a user initiates the bot"""
    user_id = message.from_user.id
    logger.info(f"User - {user_id} Started the Bot.")
    student = await User.filter(telegram_id=user_id).exists()
    if student:
        await dashboard(user_id, message)
        return
    else:
        text = (
            f"Hey, {message.from_user.first_name}!\n\n"
            f"Welcome to the Official {html.bold('St. Andrews College')} CodeX Club Management Bot.\n\n"
            "Your smart digital companion designed to streamline CodeX Club activities and enhance your learning experience. Stay updated with announcements, events, workshops, and resources, while managing club participation seamlessly, all from one unified platform.\n\n"
            "Remain informed, stay connected, and grow your technical skills through an organized and secure club ecosystem.\n\n"
            f"Click the {html.bold('Help button')} below to explore available commands and features."
        )
        await message.answer(
            text=text,
            reply_markup=keyboard,
            parse_mode="html",
            disable_web_page_preview=True,
        )