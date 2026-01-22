from aiogram import types, Router, F, html
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import  User

Button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Start-Ups", callback_data="help_start_ups"),
            InlineKeyboardButton(text="Resources", callback_data="help_resources"),
            InlineKeyboardButton(text="Jobs", callback_data="help_jobs"),
        ],
        [
            InlineKeyboardButton(text="Project Ideas", callback_data="help_project_ideas"),
            InlineKeyboardButton(text="Weekly Tests", callback_data="help_weekly_tests"),
        ],
        [
            InlineKeyboardButton(text="Report Issues", url="https://t.me/CodeXSaitm"),
        ]
    ]
)

bbutton = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Back", callback_data="btn_back"),
        ]
    ]
)

router = Router()

@router.callback_query(F.data == "btn_help")
async def handle_btn_help(callback: types.CallbackQuery):
    """
    this handler handle the help button callback
    """
    user_id = callback.from_user.id
    student = await User.filter(telegram_id=user_id).exists()
    if student:
        text = (
            f"Heya! {callback.from_user.first_name}\n\n"
            "This bot is designed to assist members and coordinators with streamlined club operations and quick access to essential commands.\n\n"
            "Please use the buttons below to view detailed help for a specific command or feature."
            "Each option will guide you with clear and concise instructions.\n\n"
            "If you require further assistance, feel free to reach out to the CodeX Club team."
        )
        await callback.message.answer(
            text=text,
            reply_markup=Button,
            parse_mode="html",
        )
        await callback.answer()
        return
    else:
        await callback.answer(
            text=f"You are required to log in before attempting to use this command. Do not proceed without proper authentication.",
            show_alert=True
        )

@router.callback_query(F.data == "btn_back")
async def handle_btn_back(callback: types.CallbackQuery):
    """
    if user click on back button
    this handler handle the back button callback
    """
    user_id = callback.from_user.id
    student = await User.filter(telegram_id=user_id).exists()
    if student:
        text = (
            f"Heya! {callback.from_user.first_name}\n\n"
            "This bot is designed to assist members and coordinators with streamlined club operations and quick access to essential commands.\n\n"
            "Please use the buttons below to view detailed help for a specific command or feature."
            "Each option will guide you with clear and concise instructions.\n\n"
            "If you require further assistance, feel free to reach out to the CodeX Club team."
        )
        await callback.message.edit_text(
            text=text,
            reply_markup=Button,
            parse_mode="html",
        )
        await callback.answer()
        return
    else:
        await callback.answer(
            text=f"You are required to log in before attempting to use this command. Do not proceed without proper authentication.",
            show_alert=True
        )

@router.callback_query(F.data == "help_project_ideas")
async def handle_btn_help_project(callback: types.CallbackQuery):
    """
    this handler handle the project idea help button callback
    """
    user_id = callback.from_user.id
    student = await User.filter(telegram_id=user_id).exists()
    if student:
        text = (
            f"{html.bold('Project Ideas')}\n\n"
            f"{html.bold('New Project Idea')}\n"
            "Submit your own project idea step by step.\n"
            "The bot will ask for all required details and publish your idea so others with the same interest can collaborate with you.\n\n"
            f"{html.bold('Get Project Ideas')}\n"
            "Find projects based on your interests.\n"
            "Enter keywords (e.g., Python, Web, AI) and the bot will show relevant projects.\n"
            "You can contact the project owner and work together to make it happen.\n"
        )
        await callback.message.edit_text(
            text=text,
            reply_markup=bbutton,
            parse_mode="html",
        )
        await callback.answer()
        return
    else:
        await callback.answer(
            text=f"You are required to log in before attempting to use this command. Do not proceed without proper authentication.",
            show_alert=True
        )