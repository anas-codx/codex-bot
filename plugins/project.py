from aiogram import types, Router, F, html, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import  ProjectIdea, User
from aiogram.fsm.context import FSMContext
from states import ProjectIdeaForm
from internal import Config

projectButton = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="New Project Idea", callback_data="new_project"),
            InlineKeyboardButton(text="Get Project Idea", callback_data="get_project"),
        ],
        [
            InlineKeyboardButton(text="Back", callback_data="back"),
        ]
    ]
)

router = Router()

@router.callback_query(F.data == "btn_project_idea")
async def handle_btn_project_idea(callback: types.CallbackQuery):
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
            f"{html.bold('> New Project Idea')} – Initiate a new project by defining its objectives, scope, and key details.\n\n"
            f"{html.bold('> Get Projects Idea')} – Access a comprehensive list of all ongoing and completed projects for reference or review.\n\n"
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
            text=f"You are required to log in before attempting to use this command. Do not proceed without proper authentication.",
            show_alert=True
        )

@router.callback_query(F.data == "new_project")
async def handle_new_project_btn(callback: types.CallbackQuery, state: FSMContext):
    """
    Starts the project submission process for a logged-in user.
    Prompts for the project title and sets the initial FSM state.
    """
    user_id = callback.from_user.id
    student = await User.filter(telegram_id=user_id).exists()
    if student:
        await callback.message.answer(
            text="Please enter the project title:",
            parse_mode="html",
        )
        await state.set_state(ProjectIdeaForm.title)
        await callback.answer()
        return
    else:
        await callback.answer(
            text=f"You are required to log in before attempting to use this command. Do not proceed without proper authentication.",
            show_alert=True
        )

@router.message(ProjectIdeaForm.title)
async def handle_get_title(message: types.Message, state: FSMContext):
    """
    Stores the project title and moves the user to the description step.
    """
    await state.update_data(title=message.text)
    await message.answer(
        text="Please enter a brief description of the project:",
        parse_mode="html",
    )
    await state.set_state(ProjectIdeaForm.description)


@router.message(ProjectIdeaForm.description)
async def handle_get_description(message: types.Message, state: FSMContext):
    """
    Saves the project description and asks for the difficulty level.
    """
    await state.update_data(description=message.text)
    await message.answer(
        text="Please select the appropriate difficulty level (Beginner / Intermediate / Advanced):",
        parse_mode="html",
    )
    await state.set_state(ProjectIdeaForm.difficulty)


@router.message(ProjectIdeaForm.difficulty)
async def handle_get_difficulty(message: types.Message, state: FSMContext):
    """
    Stores the difficulty level and prompts for the project category.
    """
    await state.update_data(difficulty_level=message.text)
    await message.answer(
        text="Please specify the project category (optional). Type skip to leave it blank:",
        parse_mode="html",
    )
    await state.set_state(ProjectIdeaForm.category)

@router.message(ProjectIdeaForm.category)
async def handle_get_category(message: types.Message, state: FSMContext):
    """
    Saves the optional project category and asks for technologies used.
    """
    category = None if message.text.lower() == "skip" else message.text
    await state.update_data(category=category)
    await message.answer(
        text="Please list the technologies used, separated by commas (e.g., Python, FastAPI):",
        parse_mode="html",
    )
    await state.set_state(ProjectIdeaForm.technologies)


@router.message(ProjectIdeaForm.technologies)
async def handle_get_technologies(message: types.Message, state: FSMContext):
    """
    Stores the technologies list and requests the project duration.
    """
    tech = [t.strip() for t in message.text.split(",")]
    await state.update_data(technologies=tech)
    await message.answer(
        text="Please provide the estimated duration for completing the project (e.g., 2 weeks):",
        parse_mode="html",
    )
    await state.set_state(ProjectIdeaForm.duration)


@router.message(ProjectIdeaForm.duration)
async def handle_get_duration(message: types.Message, state: FSMContext):
    """
    Saves the estimated project duration and asks for learning outcomes.
    """
    await state.update_data(estimated_duration=message.text)
    await message.answer(
        text="Please list the expected learning outcomes, separated by commas (e.g., Problem Solving, API Development, Database Management):",
        parse_mode="html",
    )
    await state.set_state(ProjectIdeaForm.learning_outcomes)

@router.message(ProjectIdeaForm.learning_outcomes)
async def handle_get_learning_outcomes(message: types.Message, state: FSMContext):
    """
    Stores learning outcomes and prompts for prerequisites.
    """
    outcomes = [o.strip() for o in message.text.split(",")]
    await state.update_data(learning_outcomes=outcomes)
    await message.answer(
        text="Please list the prerequisites, separated by commas (type none if there are no prerequisites, e.g., Python Basics, HTML/CSS):",
        parse_mode="html",
    )
    await state.set_state(ProjectIdeaForm.prerequisites)


@router.message(ProjectIdeaForm.prerequisites)
async def handle_get_prerequisites(message: types.Message, state: FSMContext):
    """
    Saves prerequisites and asks for reference links.
    """
    prereq = [] if message.text.lower() == "none" else [p.strip() for p in message.text.split(",")]
    await state.update_data(prerequisites=prereq)
    await message.answer(
        text="Please provide any reference links, separated by commas (type none if not available, e.g., https://docs.python.org, https://docs.python.org):",
        parse_mode="html",
        disable_web_page_preview=True,
    )
    await state.set_state(ProjectIdeaForm.references)


@router.message(ProjectIdeaForm.references)
async def handle_save_project(message: types.Message, state: FSMContext, bot: Bot):
    """
    Finalizes project submission, saves it to the database,
    and sends it to admins for review.
    """
    user_id = message.from_user.id
    data = await state.get_data()
    references = [] if message.text.lower() == "none" else [
        r.strip() for r in message.text.split(",")
    ]
    student = await User.get_or_none(telegram_id=user_id)
    student_name = student.student_name
    project = await ProjectIdea.create(
        title=data["title"],
        description=data["description"],
        difficulty_level=data["difficulty_level"],
        category=data.get("category"),
        technologies=data["technologies"],
        estimated_duration=data["estimated_duration"],
        learning_outcomes=data["learning_outcomes"],
        prerequisites=data["prerequisites"],
        reference_links=references,
        submitted_by=student
    )
    await message.answer(
        text="Your project idea has been successfully submitted.\n\nIt will become visible once it has been reviewed and approved by admins."
    )
    await state.clear()
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Approve",
                    callback_data=f"approve_{project.id}"
                ),
                InlineKeyboardButton(
                    text="Reject",
                    callback_data=f"reject_{project.id}"
                ),
            ]
        ]
    )
    await bot.send_message(
        Config().loggerId,
        text=(
            f"{html.bold('New Project Idea')}\n\n"
            f"{html.bold('Title:')} {project.title}\n\n"
            f"{html.bold('Description:')} {project.description}\n\n"
            f"Project Idea Submitted By {student_name}\n"
        ),
        parse_mode="html",
        reply_markup=buttons
    )

@router.callback_query(F.data.startswith("approve_"))
async def approve_project(callback: types.CallbackQuery, bot: Bot):
    """
    Approves a submitted project idea.
    Updates project status, notifies admins, and broadcasts the approved project to all users.
    """
    user_id = callback.from_user.id
    if user_id not in Config().authorId:
        await callback.answer(
            text="This command is restricted to administrators only.",
            show_alert=True,
        )
        return
    project_id = int(callback.data.split("_")[1])
    project = await ProjectIdea.get_or_none(id=project_id)
    if not project:
        await callback.answer(
            text="The project idea does not exist. Verify the details before wasting time.",
            show_alert=True,
        )
        return
    project.is_approved = True
    project.is_active = True
    await project.save()
    await callback.message.edit_text(
        text=f"{html.bold('Project Idea Approved Successfully')}\n\n"
        f"{html.bold('Title:')} {project.title}\n\n"
        f"{html.bold('Description:')} {project.description}\n\n"
        f"Project Idea Approved By {callback.from_user.first_name}\n",
        parse_mode="html"
    )
    await callback.answer("The project Idea has been approved. Consider yourself fortunate.")
    telegram_ids = await User.all().values_list("telegram_id", flat=True)
    await project.fetch_related('submitted_by')
    student_name = project.submitted_by.student_name
    ibutton = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Show Details", callback_data=f"showdetails_{project.id}")
            ]
        ]
    )
    for userid in telegram_ids:
        await bot.send_message(
            userid,
            text=f"{html.bold('New Project Idea')}\n\n"
                 f"{html.bold('Title:')} {project.title}\n\n"
                 f"{html.bold('Description:')} {project.description}\n\n"
                 f"Project Idea Submitted By {student_name}\n",
            reply_markup=ibutton,
            parse_mode="html",
        )

@router.callback_query(F.data.startswith("reject_"))
async def reject_project(callback: types.CallbackQuery):
    """
    Rejects a submitted project idea and disables its visibility.
    """
    user_id = callback.from_user.id
    if user_id not in Config().authorId:
        await callback.answer(
            text="This command is restricted to administrators only.",
            show_alert=True,
        )
        return
    project_id = int(callback.data.split("_")[1])
    project = await ProjectIdea.get_or_none(id=project_id)
    if not project:
        await callback.answer(
            text="The project idea does not exist. Verify the details before wasting time.",
            show_alert=True,
        )
        return
    project.is_approved = False
    project.is_active = False
    await project.save()
    await callback.message.edit_text(
        text=f"{html.bold('Project Idea Rejected Successfully')}\n\n"
        f"{html.bold('Title:')} {project.title}\n\n"
        f"{html.bold('Description:')} {project.description}\n\n"
        f"Project Idea Rejected By {callback.from_user.first_name}\n",
        parse_mode="html"
    )
    await callback.answer("The project idea has been rejected. Consider yourself fortunate.")

@router.callback_query(F.data.startswith("showdetails_"))
async def reject_project(callback: types.CallbackQuery):
    """
    Displays full project details and provides a contact button for the submitter.
    """
    user_id = callback.from_user.id
    student = await User.filter(telegram_id=user_id).exists()
    if student:
        project_id = int(callback.data.split("_")[1])
        project = await ProjectIdea.get_or_none(id=project_id)
        if not project:
            await callback.answer(
                text="The project idea does not exist. Verify the details before wasting time.",
                show_alert=True,
            )
            return
        await project.fetch_related('submitted_by')
        projectowner = project.submitted_by.telegram_id
        buttoni = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Contact Submitter", url=f"tg://user?id={projectowner}")
                ]
            ]
        )
        await callback.message.answer(
            text=f"{html.bold('New Project Idea')}\n\n"
            f"{html.bold('Title:')} {project.title}\n\n"
            f"{html.bold('Description:')} {project.description}\n\n"
            f"{html.bold('Difficulty level:')} {project.difficulty_level}\n\n"
            f"{html.bold('Category:')} {project.category}\n\n"
            f"{html.bold('Technologies:')} {project.technologies}\n\n"
            f"{html.bold('Estimated duration:')} {project.estimated_duration}\n\n"
            f"{html.bold('Learning outcomes:')} {project.learning_outcomes}\n\n"
            f"{html.bold('Prerequisites:')} {project.prerequisites}\n\n"
            f"{html.bold('Reference links:')} {project.reference_links}\n\n"
            f"Project Idea Submitted By {project.submitted_by.student_name}\n",
            reply_markup=buttoni,
            parse_mode="html",
        )
        await callback.answer()
        return
    else:
        await callback.answer(
            text=f"You are required to log in before attempting to use this command. Do not proceed without proper authentication.",
            show_alert=True
        )
