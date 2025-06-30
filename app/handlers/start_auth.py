from aiogram import F, Router
from aiogram.types import Message
from app.config import settings
from aiogram.fsm.context import FSMContext
from app.user_states import SearchForm


router = Router()


@router.message(F.text == "/auth")
async def start_auth(message: Message, state: FSMContext):
    await state.set_state(SearchForm.waiting_for_code)
    await message.answer(
        f"1️⃣ <b>Для начала нужно перейти и авторизоваться в hh:</b>\n "
        f"https://hh.ru/oauth/authorize?response_type=code&client_id={settings.CLIENT_ID}\n\n"
        f"2️⃣ После авторизации отправь мне <b>ссылку, на которую тебя перенаправил hh</b>\n\n"
        f"Она имеет вид: \nhttps://t.me/ResumeMatcherBot?code=<i>всякаябелиберда</i>",
        parse_mode="html",
    )
