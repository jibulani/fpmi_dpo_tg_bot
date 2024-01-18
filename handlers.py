from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F

from keyboards.row import make_row_keyboard

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        "Чтобы выбрать учебный курс воспользуйтесь командой /course, чтобы оставить контактные данные – /contact",
        reply_markup=ReplyKeyboardRemove()
    )


class ChooseCourse(StatesGroup):
    choosing_age = State()
    choosing_area = State()


available_ages = ["младшая школа (1-4 класс)", "средняя школа (5-8 класс)", "старшеклассники (9-11 класс)", "студенты", "взрослые"]
available_areas = ["Программирование", "Математика", "Soft-skills"]


@router.message(StateFilter(None), Command("course"))
async def message_handler(msg: Message, state: FSMContext):
    await msg.answer(
        text="Выберите возраст:",
        reply_markup=make_row_keyboard(available_ages)
    )
    # Устанавливаем пользователю состояние "выбирает возраст"
    await state.set_state(ChooseCourse.choosing_age)


@router.message(
    ChooseCourse.choosing_age,
    F.text.in_(available_ages)
)
async def age_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_age=message.text.lower())
    await message.answer(
        text="Выберите интересующее направление:",
        reply_markup=make_row_keyboard(available_areas)
    )
    await state.set_state(ChooseCourse.choosing_area)


@router.message(ChooseCourse.choosing_area, F.text.in_(available_areas))
async def area_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали направление: {message.text.lower()} для возрастной группы: {user_data['chosen_age']}.",
        reply_markup=ReplyKeyboardRemove()
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()


@router.message(Command("contact"))
async def contact_handler(msg: Message, state: FSMContext):
    await state.clear()
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Поделиться контактом", request_contact=True)
    )
    await msg.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@router.message(F.contact)
async def on_contact(message: types.Message):
    print(
        f"First name {message.contact.first_name}. "
        f"Phone: {message.contact.phone_number}"
    )
    await message.answer(
        text=f"Ваши данные успешно сохранены!",
        reply_markup=ReplyKeyboardRemove()
    )
