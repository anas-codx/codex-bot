from aiogram import Router, F, types, html
from aiogram.fsm.context import FSMContext
from models import User
from functions import dashboard
from states import LoginState
from functions import login

router = Router()

@router.callback_query(F.data == "btn_login")
async def handle_login_btn(callback: types.CallbackQuery, state: FSMContext):
    """
    Handles the login button click: checks if user exists,
    shows dashboard if registered, otherwise starts username input for login.
    """
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
    """
    Saves the entered username, updates FSM state to 'password',
    and prompts the user to enter their password.
    """
    await state.update_data(username=message.text.strip())
    await state.set_state(LoginState.password)
    await message.answer(
        text=f"Kindly enter your {html.bold('password')} to continue with the authentication process:",
        parse_mode="html"
    )

@router.message(LoginState.password)
async def handle_password(message: types.Message, state: FSMContext):
    """
    Retrieves username from state, gets the entered password,
    processes the login, deletes the processing message, and clears the FSM state.
    """
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