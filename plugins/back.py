from aiogram import types, Router, F, html
from models import User
from functions.dashBoard import btn

router = Router()

@router.callback_query(F.data == "back")
async def handle_btn_back(callback: types.CallbackQuery):
    """
    Handles the 'back' button callback by identifying the user via Telegram ID.
    Checks whether the user exists in the database as a student and, if found,
    retrieves the student's dashboard.
    """
    user_id = callback.from_user.id
    student = await User.filter(telegram_id=user_id).exists()
    if student:
        stud = await User.get_or_none(telegram_id=user_id)
        student_name = stud.student_name
        roll_number = stud.roll_number
        branch = stud.branch
        session = stud.session
        created_at = stud.created_at
        # Prepare the dashboard message with formatted text
        text = (
            f"Hey, {student_name}\n\n"
            "Welcome to your dashboard!\n\n"
            f"{html.bold('Profile:')}\n"
            f"Roll Number: {roll_number}\n"
            f"Branch: {branch}\n"
            f"Session: {session}\n"
            f"Profile Created On: {created_at}\n\n"
            "Manage your activities and stay connected with the club effortlessly."
        )
        await callback.message.edit_text(
            text=text,
            reply_markup=btn,
            parse_mode="html",
        )
        await callback.answer()
        return
    else: # if user is not registered
        await callback.answer(
            text=f"You must Login before attempting to log out.",
            show_alert=True
        )