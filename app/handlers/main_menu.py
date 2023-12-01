import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from app.create_bot import dp
from app.utils.checker import check_wallet

from app.create_bot import bot

global users
users = []


@dp.message_handler(commands=['users'])
async def send_admin_menu(message: types.Message):
    if int(message.from_user.id) == 420881832 or int(message.from_user.id) == 740574479 or int(message.from_user.id) == 812233995:
        message_response = len(users)
        await message.answer(str(message_response), parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message, state: FSMContext):
    count_use = 1
    users.append(message.from_user.id)
    await state.update_data(count_use=count_use)
    await message.answer("<b> Enter list of Solana each with a new line (20 max at a time)</b>", parse_mode=types.ParseMode.HTML)


@dp.message_handler(lambda message: not message.text.startswith('/'))
async def handle_wallets(message: types.Message, state: FSMContext):
    max_wallet = 20
    wallets = message.text.split("\n")[:max_wallet]
    results = []

    length = len(wallets)
    wait_message = await message.answer("⏳ Getting information about wallets ...")
    counter = 0

    for wallet in wallets:
        await asyncio.sleep(2)

        result = await check_wallet(wallet=wallet)

        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ <b>{counter} / {length}</b>",
                                    parse_mode=types.ParseMode.HTML)

        results.append(f"{result}\n")
        counter += 1

    await bot.delete_message(chat_id=wait_message.chat.id, message_id=wait_message.message_id)
    await message.answer("\n".join(results), parse_mode=ParseMode.HTML)

    data = await state.get_data()
    count_use = data.get("count_use")

    if count_use == 1 or count_use == 3 or count_use == 7:
        await message.answer("*🤝 Поддержать/For support: *\n\n *EVM:* `0x7525dB31E32214610586979B944Eba80D0e27296`\n *SOL:* `6hQVZPJgLXRD3doLaySVXzTvNX2RcYA8dFP3bCJXk112`", parse_mode=ParseMode.MARKDOWN)
    count_use += 1
    await state.update_data(count_use=count_use)