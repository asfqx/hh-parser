from aiogram import Router, F
from aiogram.types import (
    Message,
    FSInputFile,
    ReplyKeyboardMarkup,
    KeyboardButton,
    CallbackQuery,
)
import logging
from app.user_states import SearchForm
from app.services.search import search
from aiogram.fsm.context import FSMContext
from app.data import data
from app.services.search_resumes import search_resumes
from app.services.save_resumes import save_resumes_to_excel
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


router = Router()


@router.message(F.text == "Поиск резюме")
async def cmd_search(message: Message, state: FSMContext):
    logging.info(f"{message.chat.id}:{message.from_user.username}: {message.text}")
    await state.set_state(SearchForm.text)
    await message.answer(
        "Напишите должность вакансии. Чтобы выйти из поиска напишите 'Exit'"
    )


@router.message(SearchForm.text)
async def set_text(message: Message, state: FSMContext):
    if message.text.lower() == "exit":
        await exit_from_search(message, state)
        return 0
    search.text = str(message.text)
    await state.set_state(SearchForm.gender)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Мужской", callback_data="1")],
            [InlineKeyboardButton(text="Женский", callback_data="2")],
            [InlineKeyboardButton(text="Пропустить", callback_data="-")],
            [InlineKeyboardButton(text="Выйти", callback_data="exit")],
        ]
    )
    await message.answer(
        "Укажите пол\nЕсли это поле необязательно поставьте -", reply_markup=keyboard
    )


@router.callback_query(SearchForm.gender)
async def set_gender(callback: CallbackQuery, state: FSMContext):
    text = callback.data

    if text == "exit":
        await exit_from_search(callback, state)
        return

    if text == "-":
        await state.set_state(SearchForm.age_from)
        await callback.message.answer(
            "Введите минимальный возраст соискателя\n"
            "Если это поле необязательно — введите '-'"
        )
        await callback.answer()
        return

    search.gender = data["gender"][int(text) - 1]
    await state.set_state(SearchForm.age_from)

    await callback.message.answer(
        "Введите минимальный возраст соискателя\n"
        "Если это поле необязательно поставьте '-'"
    )
    await callback.answer()


@router.message(SearchForm.age_from)
async def set_age_from(message: Message, state: FSMContext):
    text = message.text.strip().lower()

    if text == "exit":
        await exit_from_search(message, state)
        return

    if text == "-":
        await state.set_state(SearchForm.age_to)
        await message.answer(
            "Введите максимальный возраст соискателя\n"
            "Если это поле необязательно — введите -"
        )
        return
    if not text.isdigit():
        await message.answer(
            "Неверный формат. Введите число, либо - для пропуска, либо 'exit' для выхода."
        )
        return
    if int(text) not in range(1, 100):
        await message.answer(
            "Неверное число. Введите настоящий возраст, либо отправьте -"
        )
        return
    search.age_from = message.text
    await state.set_state(SearchForm.age_to)
    await message.answer(
        "Введите максимальный возраст соискателя\n"
        "Если это поле необязательно поставьте -"
    )


@router.message(SearchForm.age_to)
async def set_age_to(message: Message, state: FSMContext):
    text = message.text.strip().lower()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Полная занятость", callback_data="1")],
            [InlineKeyboardButton(text="Частичная занятость", callback_data="2")],
            [InlineKeyboardButton(text="Проектная работа", callback_data="3")],
            [InlineKeyboardButton(text="Волонтерство", callback_data="4")],
            [InlineKeyboardButton(text="Стажировка", callback_data="5")],
            [InlineKeyboardButton(text="Пропустить", callback_data="-")],
            [InlineKeyboardButton(text="Выйти", callback_data="exit")],
        ]
    )
    if text == "exit":
        await exit_from_search(message, state)
        return

    if text == "-":
        await state.set_state(SearchForm.employment)
        await message.answer(
            "Укажите тип занятости\nЕсли поле необязательно поставьте '-'",
            reply_markup=keyboard,
        )

        return
    if not text.isdigit():
        await message.answer(
            "Неверный формат. Введите число, либо '-' для пропуска, либо 'exit' для выхода."
        )
        return

    if int(text) < int(search.age_from):
        await message.answer(
            "Число должно быть больше, чем минимальный возраст. Введите число, либо '-' "
            "или 'exit' для выхода."
        )
        return

    search.age_to = message.text
    await state.set_state(SearchForm.employment)
    await message.answer(
        "Укажите тип занятости.\nЕсли поле необязательно поставьте -",
        reply_markup=keyboard,
    )


@router.callback_query(SearchForm.employment)
async def set_employment(callback: CallbackQuery, state: FSMContext):
    text = callback.data
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Нет опыта", callback_data="1")],
            [InlineKeyboardButton(text="От 1 года до 3 лет", callback_data="2")],
            [InlineKeyboardButton(text="От 3 до 6 лет", callback_data="3")],
            [InlineKeyboardButton(text="Более 6 лет", callback_data="4")],
            [InlineKeyboardButton(text="Пропустить", callback_data="-")],
            [InlineKeyboardButton(text="Выйти", callback_data="exit")],
        ]
    )
    if text == "exit":
        await exit_from_search(callback, state)
        return

    if text == "-":
        await state.set_state(SearchForm.experience)
        await callback.message.answer(
            "Укажите опыт\nЕсли поле необязательно поставьте -", reply_markup=keyboard
        )
        await callback.answer()
        return

    search.employment = data["employment"][int(text) - 1]
    await state.set_state(SearchForm.experience)
    await callback.message.answer(
        "Укажите опыт\nЕсли поле необязательно поставьте '-'", reply_markup=keyboard
    )
    await callback.answer()


@router.callback_query(SearchForm.experience)
async def set_experience(callback: CallbackQuery, state: FSMContext):
    text = callback.data

    if text == "exit":
        await exit_from_search(callback, state)
        return

    if text == "-":
        await state.set_state(SearchForm.vacancy_id)
        await callback.message.answer("Укажите ID вакансии (если не нужно, введите -)")
        await callback.answer()
        return

    await state.set_state(SearchForm.vacancy_id)
    search.experience = data["exp"][int(text) - 1]
    await callback.message.answer("Укажите ID вакансии (если не нужно, введите '-')")


@router.message(SearchForm.vacancy_id)
async def set_vacancy_id(message: Message, state: FSMContext):
    text = message.text.strip().lower()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Среднее", callback_data="1")],
            [InlineKeyboardButton(text="Среднее специальное", callback_data="2")],
            [InlineKeyboardButton(text="Неоконченное высшее", callback_data="3")],
            [InlineKeyboardButton(text="Высшее", callback_data="4")],
            [InlineKeyboardButton(text="Бакалавр", callback_data="5")],
            [InlineKeyboardButton(text="Магистр", callback_data="6")],
            [InlineKeyboardButton(text="Кандидат наук", callback_data="7")],
            [InlineKeyboardButton(text="Доктор наук", callback_data="8")],
            [InlineKeyboardButton(text="Пропустить", callback_data="-")],
            [InlineKeyboardButton(text="Выйти", callback_data="exit")],
        ]
    )
    if text == "exit":
        await exit_from_search(message, state)
        return

    if text == "-":
        await state.set_state(SearchForm.education_level)
        await message.answer(
            "Укажите уровень образования\nЕсли поле необязательно поставьте '-'",
            reply_markup=keyboard,
        )
        return
    if not text.isdigit():
        await message.answer(
            "Неверный формат. Введите число - id, либо '-' для пропуска, либо 'exit' для выхода."
        )
        return

    search.vacancy_id = message.text
    await state.update_data(vacancy_id=message.text if message.text != "-" else "")
    await state.set_state(SearchForm.education_level)
    await message.answer(
        "Укажите уровень образования\nЕсли поле необязательно поставьте '-'",
        reply_markup=keyboard,
    )


@router.callback_query(SearchForm.education_level)
async def set_education_level(callback: CallbackQuery, state: FSMContext):
    text = callback.data

    if text == "exit":
        await exit_from_search(callback, state)
        return
    if text == "-":
        await state.clear()
        await callback.answer(
            "Поисковый запрос успешно сформирован! Отправляю таблицу..."
        )
        await send_csv(callback)
        await callback.answer()
        return

    search.education_level = data["education"][int(text) - 1]
    await state.clear()
    await callback.message.answer(
        "Поисковый запрос успешно сформирован! Отправляю таблицу..."
    )
    await send_csv(callback)
    await callback.answer()


async def send_csv(message: CallbackQuery):
    resumes = await search_resumes(search)
    if save_resumes_to_excel(resumes, message.message.chat.id):
        document = FSInputFile(f"resumes_for_{message.message.chat.id}.xlsx")
        await message.message.answer_document(document, caption="Вот ваша таблица")

        file_path = f"resumes_for_{message.message.chat.id}.xlsx"

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Файл {file_path} удалён.")
        else:
            print(f"Файл {file_path} не найден.")
    else:
        await message.message.answer("По вашему запросу не было найдено резюме")


async def exit_from_search(message, state: FSMContext):
    await state.clear()
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поиск резюме")]], resize_keyboard=True
    )
    await message.answer("Выход из поиска", reply_markup=keyboard)
