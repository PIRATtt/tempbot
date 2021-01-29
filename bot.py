import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
from asyncio import sleep
import random


from config import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


WELCOME_MESSAGE = """Привет, я бот EZWORK👋
Я буду выполнять все школьные и университетские задания за тебя😱

Напиши мне "Сделать заказ" и спустя несколько вопросов я ПОМОГУ ТЕБЕ🤗

Если тебе не удобно кидать задания через бота, то пиши мне напрямую @PIR4T
Я не кусаюсь😉!"""
ORDER_MESSAGE = """Перед тем как делать заказ, я рекомендую ознакомиться со статьёй, в которой подробно расписано как грамотно оформить заявку. От того насколько грамотно вы скинете ТЗ зависит наше решение по поводу задания и цена.

https://telegra.ph/Obyazatelno-k-prochteniyu-EZWORK-01-20

ВРЕМЯ ПРОЧТЕНИЯ 4 МИНУТЫ🔥

‼️ВАЖНО‼️ Оплатив заказ, вы автоматически соглашаетесь с правилами:
https://docs.google.com/document/d/1dK5lvso6IKPw4PmZwLkVeEv-L3ywuPe1fN2xBs5r_q0/

Если тебе не удобно кидать задания или оплачивать через бота, то пиши мне напрямую @PIR4T
Я не кусаюсь😉"""
CANCEL_MESSAGE = """Заказ отменен!"""
FILLED_MESSAGE = """Номер вашего заказа: {}
Ищем воркера на ваш заказ👷‍♂️
Ожидайте...⏱"""
ACCEPTED_MESSAGE = """Ваш заказ принят✅"""
DENIED_MESSAGE = """Пока что никто из воркеров не отписал по поводу вашего заказа. Если в будущем кто-то отпишет - я свяжусь с тобой в ЛС😉"""
CONST_MESSAGE = """При оплате всю комиссию сторонних платёжных систем вы берёте на себя!
После оплаты надо обязательно меня уведомить🔥

Актуальные реквизиты:

QIWI: +79672256773
QIWI card: 4890494698257425
YOOmoney: 4100115308938360
BTC: 1LN26u4NyScT3WqdBkzdgxRN3jfgg4MGcs
PAYEER: P1023042699"""

FIRST_QUESTION = """1. Отправь свою ссылку на профиль с форума.
Если ты не с форума - то просто напиши "минус"."""
SECOND_QUESTION = """2. Какой класс/курс?"""
THIRD_QUESTION = """3. Полное название предмета."""
FOURTH_QUESTION = """4. Задание.

В этом пункте ты должен скинуть всю информацию по заданию.
Требуется уточнить в каком виде тебе нужна работа - рукописном или печатном (печатный - решённое задание тебе скинут в файле doc, или просто текстом в тг; рукописный - тебе скинут фото листа с решением написанным от руки).

Если надо скинуть несколько файлов, то воспользуйся бесплатными облачными хранилищами:
disk.yandex.ru
drive.google.com
files.dp.ua
dropmefiles.com """
FIFTH_QUESTION = """5. Сроки.
Назови дату и время по МСК, до которого мы должны успеть отправить тебе готовую работу."""
SIXTH_QUESTION = """6. Цена заказа?
Если вы не знаете какую назвать цену - ставьте "минус". В этом случае мы сами вам её сообщим."""

BUTTON_1 = 'Сделать заказ'
BUTTON_2 = 'Отменить заказ'
BUTTON_3 = """Реквизиты"""

OWNER_ID = 702885050

kb_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(BUTTON_1)).add(KeyboardButton(BUTTON_3))
kb_2 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(BUTTON_2)).add(KeyboardButton(BUTTON_3))

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
        if message.reply_to_message:
            txt = message.reply_to_message.text
            order_id = int(txt.split(': ')[1].split('\n')[0])
            user_id = orders[order_id]
            await bot.forward_message(chat_id=user_id, from_chat_id=OWNER_ID, message_id=message.message_id)
            await message.answer('Отправлено!')
        elif tx.startswith('/accept_'):
            order_id = int(tx.split('_')[1])
            user_id = orders[order_id]
            del orders[order_id]
            users[user_id]['step'] = 0
            await bot.send_message(user_id, ACCEPTED_MESSAGE, reply_markup=kb_1)
            await message.answer('Заказ принят!')
        elif tx.startswith('/decline_'):
            order_id = int(tx.split('_')[1])
            user_id = orders[order_id]
            del orders[order_id]
            users[user_id]['step'] = 0
            await bot.send_message(user_id, DENIED_MESSAGE, reply_markup=kb_1)
            await message.answer('Заказ отклонен!')
        elif tx.startswith('/ban '):
            id_ban = int(tx.split()[-1])
            banneds = set(get_banneds())
            banneds.add(id_ban)
            update_banneds(list(banneds))
            await message.answer('Забанен!')
        elif tx.startswith('/unban '):
            id_ban = int(tx.split()[-1])
            banneds = set(get_banneds())
            banneds.discard(id_ban)
            update_banneds(list(banneds))
            await message.answer('Разбанен!')
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
        elif tx == '/users':
            await message.answer(f'Юзеров в боте: {len(get_users())}\nИз них забаненных: {len(get_banneds())}')

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

    elif tx == BUTTON_3:
        await message.answer(CONST_MESSAGE)

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
        users[id]['step'] = 7

        await bot.send_message(OWNER_ID, f'Новый заказ!\n\nID Заказа: {order_id}\nПользователь: [{id}](tg://user?id={id})\n\nЧто бы задать вопрос пользователю, ответьте на это сообщение.\n\nЧто бы принять заказ отправьте команду /accept\\_{order_id}\nЧто бы отклонить заказ отправьте команду /decline\\_{order_id}', parse_mode=ParseMode.MARKDOWN)
        for msg in users[id]['answers']:
            await bot.forward_message(chat_id=OWNER_ID, from_chat_id=id, message_id=msg)

        users[id]['answers'] = []

        await sleep(3 * 3600)

        await message.answer(DENIED_MESSAGE, reply_markup=kb_1)
        del orders[order_id]

    elif users[id]['step'] == 7:
        for order_id, user_id in orders.items():
            if user_id == id:
                break
        await bot.send_message(OWNER_ID, f'Новое сообщение по заказу: {order_id}\n\nЧто бы задать вопрос пользователю, ответьте на это сообщение.\n\nЧто бы принять заказ отправьте команду /accept_{order_id}\nЧто бы отклонить заказ отправьте команду /decline_{order_id}')
        await bot.forward_message(chat_id=OWNER_ID, from_chat_id=id, message_id=message.message_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
