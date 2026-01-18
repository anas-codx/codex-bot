from aiogram import Router, F, types, html
from models import User
from plugins.functions.dashBoard import dashboard

router = Router()

in_process: dict[int, dict] = {}

@router.callback_query(F.data == "btn_login")
async def login_btn(callback: types.CallbackQuery):
    """Callback handler for btn_login"""
    user_id = callback.from_user.id
    if await User.filter(telegram_id=user_id).exists():
        await dashboard(user_id, callback.message)
        await callback.answer()
        return
    in_process[user_id] = {"step": "username"}
    await callback.message.answer(
        text=f"Please enter your {html.bold('username')} to proceed with authentication:",
        parse_mode="html"
    )
    await callback.answer()