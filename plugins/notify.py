from aiogram import types, Router, html
from aiogram.filters import Command
from internal import Config

router = Router()

in_bcast: dict[int, dict] = {}

@router.message(Command("bcast"))
async def bcast(message: types.Message):
    """Initiates the email broadcast workflow for authorized administrators."""
    user_id = message.from_user.id
    if user_id not in Config().authorId:
        await message.answer(
            text="This command is for admins only. Stay within your limits.",
            parse_mode="html",
        )
        return
    in_bcast[user_id] = {"step": "subject"}
    await message.answer(
        text=f"Enter the email {html.bold('subject')} to be broadcast:",
        parse_mode="html",
    )