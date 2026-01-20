from aiogram.fsm.state import State, StatesGroup

# Defines FSM states for the broadcast process:
# 'subject' for entering the email subject
# 'mail' for entering the email body

class BroadcastState(StatesGroup):
    subject = State()
    mail = State()