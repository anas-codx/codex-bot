from aiogram.fsm.state import State, StatesGroup

class LoginState(StatesGroup):
    username = State()
    password = State()

from aiogram import Router, F, types, html
from aiogram.fsm.context import FSMContext
from models import User
from functions import dashboard

router = Router()

@router.callback_query(F.data == "btn_login")
async def login_btn(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    if await User.filter(telegram_id=user_id).exists():
        await dashboard(user_id, callback.message)
        await callback.answer()
        return

    await state.clear()
    await state.set_state(LoginState.username)

    await callback.message.answer(
        text=f"Please enter your {html.bold('username')} to proceed with authentication:",
        parse_mode="html"
    )
    await callback.answer()

@router.message(LoginState.username)
async def handle_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text.strip())
    await state.set_state(LoginState.password)

    await message.answer(
        text=f"Kindly enter your {html.bold('password')} to continue with the authentication process:",
        parse_mode="html"
    )
from functions import login

@router.message(LoginState.password)
async def handle_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data["username"]
    password = message.text.strip()

    msg = await message.answer(
        text="Processing your request...",
        parse_mode="html",
    )

    await login(username, password, message)

    await msg.delete()
    await state.clear()