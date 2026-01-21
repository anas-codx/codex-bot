from aiogram import Router, types, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import BroadcastState
from internal import Config
from functions import sendmail

router = Router()

@router.message(Command("bcast"))
async def handle_bcast(message: types.Message, state: FSMContext):
    """
    Starts the broadcast process for admins: checks authorization,
    clears previous state, sets state to subject, and asks for email subject.
    """
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
    """
    Saves the entered email subject, updates FSM state to 'mail',
    and prompts the admin to enter the email message body.
    """
    await state.update_data(subject=message.text.strip())
    await state.set_state(BroadcastState.mail)
    await message.answer(
        text=f"Now, enter the email {html.bold('message')} to be broadcast:",
        parse_mode="html",
    )

@router.message(BroadcastState.mail)
async def handle_bcast_mail(message: types.Message, state: FSMContext):
    """
    Retrieves the saved subject, gets the email body from input,
    sends the broadcast email, and clears the FSM state.
    """
    data = await state.get_data()
    subject = data["subject"]
    mail = message.text.strip()
    await sendmail(subject, mail, message)
    await state.clear()
