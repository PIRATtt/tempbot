import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
from asyncio import sleep
import random


API_TOKEN = '1071345929:AAE9zHlNo9Xmvf1q0JXOEVZnsZeg3ZmP2Mg'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


WELCOME_MESSAGE = 'Привет!'
ORDER_MESSAGE = 'Сообщение'
CANCEL_MESSAGE = 'Заказ отменен!'
FILLED_MESSAGE = 'Номер вашего заказа: {}\nОжидайте ответа'
ACCEPTED_MESSAGE = 'Ваш заказ принят'
DENIED_MESSAGE = 'Заказ отклонен!'

FIRST_QUESTION = 'Первый вопрос?'
SECOND_QUESTION = 'Второй вопрос?'
THIRD_QUESTION = 'Третий вопрос?'
FOURTH_QUESTION = 'Четвертый вопрос?'
FIFTH_QUESTION = 'Пятый вопрос?'
SIXTH_QUESTION = 'Шестой вопрос?'

BUTTON_1 = 'Сделать заказ'
BUTTON_2 = 'Отменить заказ'

OWNER_ID = 702885050

kb_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(BUTTON_1))
kb_2 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(BUTTON_2))

users = {}
orders = {}


def get_users():
    with open('users.txt', 'r') as f:
        return [int(i) for i in f.readlines()]


def update_users(users):
    with open('users.txt', 'w') as f:
        f.write('\n'.join([str(i) for i in users]))


def get_banneds():
    with open('banneds.txt', 'r') as f:
        return [int(i) for i in f.readlines()]


def update_banneds(banneds):
    with open('banneds.txt', 'w') as f:
        f.write('\n'.join([str(i) for i in banneds]))


@dp.message_handler(commands=['start'])
async def handler(message: Message):
    id = message.from_user.id

    if id in get_banneds():
        return

    ids = set(get_users())
    if id not in ids:
        ids.add(id)
        update_users(list(ids))

    if id not in users.keys():
        users[id] = {
            'step': 0,
            'answers': []
        }

    if users[id]['step'] == 7:
        return

    if id != OWNER_ID:
        await message.answer(WELCOME_MESSAGE, reply_markup=kb_1)
    else:
        await message.answer(WELCOME_MESSAGE)


@dp.message_handler(content_types=ContentType.ANY)
async def handler(message: Message):
    id, tx = message.from_user.id, message.text

    if id in get_banneds():
        return

    ids = set(get_users())
    if id not in ids:
        ids.add(id)
        update_users(list(ids))

    if id == OWNER_ID:
        if tx.startswith('/accept_'):
            order_id = int(tx.split('_')[1])
            user_id = orders[order_id]
            del orders[order_id]
            users[user_id]['step'] = 0
            await bot.send_message(user_id, ACCEPTED_MESSAGE, reply_markup=kb_1)
            await message.answer('Заказ принят!')
        elif tx.startswith('/ban '):
            id_ban = int(tx[5:])
            banneds = set(get_banneds())
            banneds.add(id_ban)
            update_banneds(list(banneds))
            message.answer('Забанен!')
        elif tx.startswith('/unban '):
            id_ban = int(tx[5:])
            banneds = set(get_banneds())
            banneds.discard(id_ban)
            update_banneds(list(banneds))
            message.answer('Разбанен!')
        elif tx.startswith('/broadcast '):
            text = tx[11:]
            good = bad = 0
            for id in ids:
                try:
                    await bot.send_message(id, text)
                    good += 1
                except:
                    bad += 1
            await message.answer(f'Рассылка завершена!\n\nУспешно: {good}\nОшибка: {bad}\nВсего: {good + bad}')
        elif '/accept_' in message.reply_to_message.text:
            txt = message.reply_to_message.text
            order_id = int(txt.split('/accept_')[1])
            user_id = orders[order_id]
            await bot.forward_message(chat_id=user_id, from_chat_id=OWNER_ID, message_id=message.message_id)
            users[user_id]['step'] = 7

    elif id not in users.keys():
        users[id] = {
            'step': 0,
            'answers': []
        }

    elif tx == BUTTON_1 and users[id]['step'] != 7:
        await message.answer(ORDER_MESSAGE)
        await sleep(1)
        await message.answer(FIRST_QUESTION, reply_markup=kb_2)
        users[id]['step'] = 1

    elif tx == BUTTON_2 and users[id]['step'] != 7:
        users[id] = {
            'step': 0,
            'answers': []
        }
        await message.answer(CANCEL_MESSAGE, reply_markup=kb_1)

    elif users[id]['step'] == 1:
        await message.answer(SECOND_QUESTION)
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 2

    elif users[id]['step'] == 2:
        await message.answer(THIRD_QUESTION)
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 3

    elif users[id]['step'] == 3:
        await message.answer(FOURTH_QUESTION)
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 4

    elif users[id]['step'] == 4:
        await message.answer(FIFTH_QUESTION)
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 5

    elif users[id]['step'] == 5:
        await message.answer(SIXTH_QUESTION)
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 6

    elif users[id]['step'] == 6:
        order_id = random.randint(1000, 9999)
        while order_id in orders.keys():
            order_id = random.randint(1000, 9999)

        orders[order_id] = id

        await message.answer(FILLED_MESSAGE.format(order_id), reply_markup=kb_1)
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 0

        await bot.send_message(OWNER_ID, f'Новый заказ!\n\nID Заказа: {order_id}\nПользователь: [{id}](tg://user?id={id})\n\nЧто бы задать вопрос пользователю, ответьте на это сообщение.\n\nЧто бы принять заказ отправьте команду /accept\\_{order_id}', parse_mode=ParseMode.MARKDOWN)
        for msg in users[id]['answers']:
            await bot.forward_message(chat_id=OWNER_ID, from_chat_id=id, message_id=msg)

        users[id]['answers'] = []

        await sleep(7200)

        await message.answer(DENIED_MESSAGE, reply_markup=kb_1)
        del orders[order_id]

    elif users[id]['step'] == 7:
        for order_id, user_id in orders.items():
            if user_id == id:
                break
        await bot.send_message(OWNER_ID, f'Новое сообщение по заказу {order_id}!\n\nЧто бы задать вопрос пользователю, ответьте на это сообщение.\n\nЧто бы принять заказ отправьте команду /accept_{order_id}')
        await bot.forward_message(chat_id=OWNER_ID, from_chat_id=id, message_id=message.message_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
