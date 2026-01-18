from aiogram import Router, types, F, html
from models import User
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from internal import Config

router = Router()

helpButton = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Resources", callback_data="help_resources"),
            InlineKeyboardButton(text="Jobs", callback_data="help_jobs"),
            InlineKeyboardButton(text="Start-Ups", callback_data="help_start_ups"),
        ],
        [
            InlineKeyboardButton(text="Project Idea", callback_data="help_project_idea"),
            InlineKeyboardButton(text="Weekly Tests", callback_data="help_weekly_tests"),
            InlineKeyboardButton(text="Admins", callback_data="help_admins"),
        ],
        [
            InlineKeyboardButton(text="Report Issues", url="https://t.me/CodeXSaitm"),
        ]
    ]
)

backButton = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Back", callback_data="back"),
        ]
    ]
)

@router.callback_query(F.data == "btn_help")
async def btn_help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if await User.filter(telegram_id=user_id).exists():
        await callback.message.answer(
            text=f"Heya! {callback.from_user.first_name}\n\nThis bot is designed to assist members and coordinators with streamlined club operations and quick access to essential commands.\n\nPlease use the buttons below to view detailed help for a specific command or feature.\nEach option will guide you with clear and concise instructions.\n\nIf you require further assistance, feel free to reach out to the CodeX Club team.",
            reply_markup=helpButton,
            parse_mode="html",
        )
        await callback.answer()
        return
    await callback.answer(
        text="You’ll need to log in before even thinking about using this command.",
        show_alert=True
    )

@router.callback_query(F.data == "back")
async def help_resources(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if await User.filter(telegram_id=user_id).exists():
        await callback.message.edit_text(
            text=f"Heya! {callback.from_user.first_name}\n\nThis bot is designed to assist members and coordinators with streamlined club operations and quick access to essential commands.\n\nPlease use the buttons below to view detailed help for a specific command or feature.\nEach option will guide you with clear and concise instructions.\n\nIf you require further assistance, feel free to reach out to the CodeX Club team.",
            reply_markup=helpButton,
            parse_mode="html",
        )
        await callback.answer()
        return
    await callback.answer(
        text="You’ll need to log in before even thinking about using this command.",
        show_alert=True
    )

@router.callback_query(F.data == "help_resources")
async def help_resources(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if await User.filter(telegram_id=user_id).exists():
        await callback.message.edit_text(
            text=f"hey here is the resouces",
            reply_markup=backButton,
            parse_mode="html",
        )
        await callback.answer()
        return
    await callback.answer(
        text="You’ll need to log in before even thinking about using this command.",
        show_alert=True
    )

@router.callback_query(F.data == "help_resources")
async def help_resources(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if await User.filter(telegram_id=user_id).exists():
        await callback.message.edit_text(
            text=f"hey here is the resouces",
            reply_markup=backButton,
            parse_mode="html",
        )
        await callback.answer()
        return
    await callback.answer(
        text="You’ll need to log in before even thinking about using this command.",
        show_alert=True
    )

@router.callback_query(F.data == "help_admins")
async def help_admins(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if await User.filter(telegram_id=user_id).exists():
        await callback.message.edit_text(
            text=f"{html.bold('Admin Commands:')}\n\nThis section lists commands available only to authorized administrators.\n\n{html.bold('Available Commands:')}\n\n• /bcast\nSend a broadcast message to all registered users of the bot.\nUse this responsibly for important announcements only.\n\n• /ping\nCheck the bot’s responsiveness.\nReturns an immediate confirmation if the bot is online.\n\n• /uptime\nDisplays how long the bot has been running since the last restart.\nUseful for monitoring system stability.\n\n{html.bold('⚠️ Important Notice:')}\nThese commands are restricted to administrators.\nUnauthorized usage attempts may be logged or ignored.",
            reply_markup=backButton,
            parse_mode="HTML",
        )
        await callback.answer()
        return
    await callback.answer(
        text="You’ll need to log in before even thinking about using this command.",
        show_alert=True
    )