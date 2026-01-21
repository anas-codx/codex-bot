from models import User
from aiogram import Router, F, types, html
from functions.onLogin import loginBtn
from internal import logger

router = Router()

@router.callback_query(F.data == "btn_logout")
async def handle_logout_btn(callback: types.CallbackQuery):
    """
    Handles the logout button click: deletes the user from database if exists,
    confirms logout, and shows the login button; alerts if user is not logged in.
    """
    user_id = callback.from_user.id
    user = await User.get_or_none(telegram_id=user_id)
    if user:
        msg = await callback.message.answer(
            text="Processing your request...",
            parse_mode="html",
        )
        await user.delete()
        await callback.message.answer(
            text=f"You have successfully {html.bold('logged out!')}",
            reply_markup=loginBtn,
            parse_mode="html",
        )
        logger.info(f"User - {user_id} has been logged out successfully.")
        await msg.delete()
        return
    await callback.answer(
        text=f"You are required to log in before attempting to use this command. Do not proceed without proper authentication.",
        show_alert=True
    )