from aiogram.fsm.state import StatesGroup, State

# Defines FSM states for the project idea submission process:
# 'title' for entering the project title
# 'description' for entering the project description
# 'difficulty' for selecting the difficulty level
# 'category' for specifying the project category (optional)
# 'technologies' for listing technologies used
# 'duration' for providing the estimated completion time
# 'learning_outcomes' for expected skills or knowledge gained
# 'prerequisites' for required prior knowledge
# 'references' for reference links or resources

class ProjectIdeaForm(StatesGroup):
    title = State()
    description = State()
    difficulty = State()
    category = State()
    technologies = State()
    duration = State()
    learning_outcomes = State()
    prerequisites = State()
    references = State()