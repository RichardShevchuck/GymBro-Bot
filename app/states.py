from aiogram.fsm.state import State, StatesGroup


class AddWorkoutStates(StatesGroup):
    waiting_for_exercise = State()
    waiting_for_weight = State()
    waiting_for_reps = State()
    waiting_for_sets = State()