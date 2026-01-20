from aiogram.fsm.state import State, StatesGroup

class BroadcastState(StatesGroup):
    subject = State()
    mail = State()

from aiogram import Router, types, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from internal import Config

router = Router()

@router.message(Command("bcast"))
async def bcast(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if user_id not in Config().authorId:
        await message.answer(
            text="This command is restricted to administrators only.",
            parse_mode="html",
        )
        return

    await state.clear()
    await state.set_state(BroadcastState.subject)

    await message.answer(
        text=f"Enter the email {html.bold('subject')} to be broadcast:",
        parse_mode="html",
    )

@router.message(BroadcastState.subject)
async def handle_bcast_subject(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text.strip())
    await state.set_state(BroadcastState.mail)

    await message.answer(
        text=f"Now, enter the email {html.bold('message')} to be broadcast:",
        parse_mode="html",
    )

from functions import sendmail

@router.message(BroadcastState.mail)
async def handle_bcast_mail(message: types.Message, state: FSMContext):
    data = await state.get_data()
    subject = data["subject"]
    mail = message.text.strip()

    await sendmail(subject, mail, message)

    await state.clear()
