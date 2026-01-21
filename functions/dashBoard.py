from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import User
from aiogram import html
from internal import logger

# Create an inline keyboard for the dashboard based on bot features
btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Resources', callback_data='btn_resources'),
                InlineKeyboardButton(text='Jobs', callback_data='btn_jobs'),
            ],
            [
                InlineKeyboardButton(text='Project Idea', callback_data='btn_project_idea'),
                InlineKeyboardButton(text='Start-Ups', callback_data='btn_startup'),
            ],
            [
                InlineKeyboardButton(text='Weekly Tests', callback_data='btn_weekly_tests'),
            ],
            [
                InlineKeyboardButton(text='Help', callback_data='btn_help'),
            ],
            [
                InlineKeyboardButton(text='Logout', callback_data='btn_logout'),
            ]
        ]
    )

async def dashboard(user_id, message):
    """
    Fetch and display the user's dashboard.
    Retrieves user details from the database and sends
    a formatted dashboard message with action buttons.
    """
    # Fetch user data based on Telegram user ID
    try:
        logger.info("Fetching user information from the database...")
        student = await User.get_or_none(telegram_id=user_id)
        student_name = student.student_name
        roll_number = student.roll_number
        branch = student.branch
        session = student.session
        created_at = student.created_at
        # Prepare the dashboard message with formatted text
        logger.info("Information fetched successfully. Sending it to the user.")
        text = (
            f"Hey, {student_name}\n\n"
            "Welcome to your dashboard!\n\n"
            f"{html.bold('Profile:')}\n"
            f"Roll Number: {roll_number}\n"
            f"Branch: {branch}\n"
            f"Session: {session}\n"
            f"Profile Created On: {created_at}\n\n"
            "Manage your activities and stay connected with the club effortlessly."
        )
        # Send the dashboard message with inline keyboard buttons
        await message.answer(
            text=text,
            reply_markup=btn,
            parse_mode="html",
            disable_web_page_preview=True,
        )
    except Exception as e:
        logger.error(e)