from aiogram.fsm.state import State, StatesGroup

# Defines FSM states for the login process:
# 'username' for entering the username
# 'password' for entering the password

class LoginState(StatesGroup):
    username = State()
    password = State()