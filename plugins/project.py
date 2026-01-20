from aiogram import types, Router, F, html
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import User

projectButton = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="New Project", callback_data="new_project"),
            InlineKeyboardButton(text="Get Project", callback_data="get_project"),
        ],
        [
            InlineKeyboardButton(text="Back", callback_data="back"),
        ]
    ]
)

router = Router()

@router.callback_query(F.data == "btn_project_idea")
async def btn_project(callback: types.CallbackQuery):
    """
    Handles the 'Project Idea' button callback.
    Identifies the user using their Telegram ID and verifies
    whether the user exists in the database as a registered student
    before proceeding with project-related actions.
    """
    user_id = callback.from_user.id
    student = await User.filter(telegram_id=user_id).exists()
    if student:
        text = (
            f"{html.bold('Project Portal:')}\n\n"
            "Welcome to the Project Hub, your central point for managing and tracking all projects. This platform allows you to efficiently create new projects and stay updated with existing ones.\n\n"
            f"{html.bold('> New Project')} – Initiate a new project by defining its objectives, scope, and key details.\n"
            f"{html.bold('> Get Projects')} – Access a comprehensive list of all ongoing and completed projects for reference or review.\n\n"
            "Please select an option to proceed and take the next step in managing your projects.\n"
        )
        await callback.message.edit_text(
            text=text,
            reply_markup=projectButton,
            parse_mode="html",
        )
        await callback.answer()
        return
    else:
        await callback.answer(
            text=f"You must Login before attempting to log out.",
            show_alert=True
        )