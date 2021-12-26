import logging
from sqlite3.dbapi2 import Cursor
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import *
from asyncio import sleep
import random
import sqlite3
import datetime
from datetime import datetime
import os
import asyncio




#from config import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token='1373154390:AAHdUzaJv-YYSr31zNrFfDXPiR7cttj5gnc')
dp = Dispatcher(bot,storage=MemoryStorage())


WELCOME_MESSAGE = """Привет, я бот EZWORK👋
Я буду выполнять все школьные и университетские задания за тебя😱
Напиши мне "Сделать заказ" и спустя несколько вопросов я ПОМОГУ ТЕБЕ🤗

Если тебе не удобно кидать задания через бота, то пиши мне напрямую @PIR4T
Я не кусаюсь😉!"""
ORDER_MESSAGE = """Перед тем как делать заказ, я рекомендую ознакомиться со статьёй, в которой подробно расписано как грамотно оформить заявку. От того насколько грамотно вы скинете ТЗ зависит наше решение по поводу задания и цена.

https://telegra.ph/Obyazatelno-k-prochteniyu-EZWORK-01-20

‼️ВАЖНО‼️ Оплатив заказ, вы автоматически соглашаетесь с правилами:
https://docs.google.com/document/d/1dK5lvso6IKPw4PmZwLkVeEv-L3ywuPe1fN2xBs5r_q0/

Если тебе не удобно кидать задания или оплачивать через бота, то пиши мне напрямую @PIR4T"""
CANCEL_MESSAGE = """Заказ отменен!"""
FILLED_MESSAGE = """Номер вашего заказа: {}
Ищем воркера на ваш заказ👷‍♂️
Ожидайте...⏱

Начался чат с администрацией❗️"""
ACCEPTED_MESSAGE = """Ваш заказ выполнен✅"""
DENIED_OTMENA_MESSAGE = """Администрация отклонила ваш заказ❌"""
DENIED_AFK_MESSAGE = """Пока что никто из воркеров не отписал по поводу вашего заказа. Если в будущем кто-то отпишет - я свяжусь с тобой в ЛС😉"""
CONST_MESSAGE = """При оплате всю комиссию сторонних платёжных систем вы берёте на себя!
После оплаты надо обязательно меня уведомить🔥

Актуальные реквизиты:

🥝QIWI: +79992570891

💳QIWI card: 4890494735875163

🔸BTC (+10%): bc1qnnc4wkr78dvu3u7tk29lvgeqwhu0l3g85z6cde

🔹ETH (+10%): 0xcC5B68AdB60D39B9de083A2d73c4BF98671F343f"""
REVIEW = """Если тебе не сложно, можешь оставить свой отзыв по работе с нами тут? @ezywork_comment
Я бы тебе был очень благодарен💜"""
PROCESS = """Заказ принят в обработку. Я отписал всем воркерам, жду пока кто-нибудь возьмёт ваш заказ.

Также, вы можете назвать, либо, если вы уже предлагали, то обновить цену заказа. Тоже самое вы можете сделать со сроками сдачи и самим задание.

❗️Всё это может ускорить взятие вашего заказа❗️"""
requisites = """При оплате всю комиссию сторонних платёжных систем вы берёте на себя!
После оплаты надо обязательно меня уведомить🔥

Актуальные реквизиты:

🥝QIWI: +79992570891

💳QIWI card: 4890494735875163

🔸BTC (+10%): bc1qnnc4wkr78dvu3u7tk29lvgeqwhu0l3g85z6cde

🔹ETH (+10%): 0xcC5B68AdB60D39B9de083A2d73c4BF98671F343f"""

FIRST_QUESTION = """1. Отправь свою ссылку на профиль с форума.
Если ты не с форума - то просто напиши "минус"."""
SECOND_QUESTION = """2. Какой класс/курс?"""
THIRD_QUESTION = """3. Полное название предмета."""
FOURTH_QUESTION = """4. Задание.
В этом пункте ты должен скинуть всю информацию по заданию.
Требуется уточнить в каком виде тебе нужна работа - рукописном или печатном (печатный - решённое задание тебе скинут в файле doc, или просто текстом в тг; рукописный - тебе скинут фото листа с решением написанным от руки).

Бот умеет пересылать фото, документы, видео, любого размера в любых количествах, но если у тебя много файлов, то воспользуйся, пожалуйста, бесплатными облачными хранилищами, чтобы не засорять переписку:
disk.yandex.ru
drive.google.com
dropmefiles.com """
FIFTH_QUESTION = """5. Сроки.
Назови дату и время по МСК, до которого мы должны успеть отправить тебе готовую работу."""
SIXTH_QUESTION = """6. Цена заказа?
Если вы не знаете какую назвать цену - ставьте "минус". В этом случае мы сами вам её сообщим."""

BUTTON_1 = 'Сделать заказ'
BUTTON_2 = 'Отменить заказ'
BUTTON_3 = """Реквизиты"""
BUTTON_4 = 'Отменить заказ'
BUTTON_5 = 'Правила'
BUTTON_6 = 'Отзывы'
BUTTON_51 = 'Правила'
BUTTON_61 = 'Отзывы'


OWNER_ID = 702885050

texsts = "132"
kb_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(BUTTON_1)).add(KeyboardButton(BUTTON_3),KeyboardButton(BUTTON_51),KeyboardButton(BUTTON_61))
kb_2 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(BUTTON_2)).add(KeyboardButton(BUTTON_3),KeyboardButton(BUTTON_5),KeyboardButton(BUTTON_6))
kb_3 = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(BUTTON_3)).add(KeyboardButton(BUTTON_4))
kb_4 = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Да",callback_data='da')).add(InlineKeyboardButton(text="Нет",callback_data='net'))

users = {}
orders = {}

choi = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
q = types.KeyboardButton(text = "Да")
w = types.KeyboardButton(text = "Нет")
choi.add(q,w)

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Users (id,nik,date)")
cursor.execute("CREATE TABLE IF NOT EXISTS settings (id,st,st2,st3)")
cursor.execute("INSERT OR IGNORE INTO settings (id,st,st2,st3) VALUES (?,?,?,?)",(0,0,0,0))
conn.commit()

conn = sqlite3.connect("infous.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS us (id,num)")
conn.commit()


class getstates(StatesGroup):
    inputphoto = State()

class form(StatesGroup):
    datezkz = State()

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


@dp.message_handler(state=getstates.inputphoto)
async def inputphoto(message: types.Message, state: FSMContext):
    answer = message.text
    ids = set(get_users())
    good = bad = 0
    for id in ids:
        try:
            
            await bot.send_photo(id,f'{answer}',caption=f'{texsts}')
            good += 1
        except:
            bad += 1
    await bot.delete_message(message.chat.id,message.message_id)
    await message.answer(f'Рассылка завершена!\n\nУспешно: {good}\nОшибка: {bad}\nВсего: {good + bad}')            
    await state.finish()

@dp.message_handler(commands=['start'])
async def handler(message: Message):
    nik = message.from_user.username
    id = message.from_user.id
    if id in get_banneds():
        return

    ids = set(get_users())
    if id not in ids:
        ids.add(id)
        update_users(list(ids))
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO Users (id,nik,date) VALUES (?,?,?)",(id,nik,current_date))
        conn.commit()

    if id not in users.keys():
        users[id] = {
            'step': 0,
            'answers': []
        }
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(f'UPDATE Users SET date = "{current_date}" WHERE id = {id}')
        conn.commit()


    if users[id]['step'] == 7:
        return

    if id != OWNER_ID:
        await message.answer(WELCOME_MESSAGE, reply_markup=kb_1)
    else:
        await message.answer(WELCOME_MESSAGE)


#@dp.message_handler(content_types=['photo'])
@dp.callback_query_handler()
async def query_handler(call):
    user_id = call.message.chat.id
    ids = set(get_users())
    if call.message:
        if call.data == 'da':
            await bot.delete_message(call.message.chat.id,call.message.message_id)
            await call.message.answer('Введите ссылку на фото.(Сделать ссылку поможет этот бот - @imgurbot_bot)')
            await getstates.inputphoto.set()
        elif call.data == 'net':
            good = bad = 0
            for id in ids:
                try:
                    await bot.send_message(id, texsts)
                    good += 1
                except:
                    bad += 1
            await bot.delete_message(call.message.chat.id,call.message.message_id)
            await call.message.answer(f'Рассылка завершена!\n\nУспешно: {good}\nОшибка: {bad}\nВсего: {good + bad}')            


@dp.message_handler(content_types=ContentType.ANY)
async def handler(message: Message):
    global name
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
            global order_id
            order_id = int(txt.split(': ')[1].split('\n')[0])
            user_id = orders[order_id]
            if users[user_id]['step'] != 7:
                await message.answer('У пользователя нет активных заказов')
            else:
                await bot.forward_message(chat_id=user_id, from_chat_id=OWNER_ID, message_id=message.message_id)
                await message.answer('Отправлено!')
        elif message.text.startswith('/broadcast '):
            text = tx[11:]
            global texsts
            texsts = text
            await message.answer('Хотите отправить фото?',reply_markup=kb_4)
        elif tx == '/users':
            await message.answer(f'Юзеров в боте: {len(get_users())}\nИз них забаненных: {len(get_banneds())}')        
        elif tx.startswith('/accept_'):
            order_id = int(tx.split('_')[1])
            if not any( x == order_id for x in orders):
                await message.answer('Заказ не актуален')
            else:
                user_id = orders[order_id]
                del orders[order_id]
                users[user_id]['step'] = 0
                await bot.send_message(user_id, "Ваш заказ успешно выполнен✅ Спасибо большое, что выбираете нас💜", reply_markup=kb_1)
                await message.answer(f'Ваш заказ успешно выполнен✅ Спасибо большое, что выбираете нас💜')
                await bot.send_sticker(user_id,"CAACAgIAAxkBAAEDbuthr4qKT0lIn-vpzI9v1TpN7IRZmAAC8REAAm2RaUkL2Jbo4iBBFSME")
        elif tx.startswith('/review_'):
            order_id = int(tx.split('_')[1])
            if not any( x == order_id for x in orders):
                await message.answer('Заказ не актуален')
            else:
                user_id = orders[order_id]
                
                await bot.send_message(user_id,REVIEW)
                await message.answer("Отправлено")
        elif tx.startswith('/process_'):
            order_id = int(tx.split('_')[1])
            if not any( x == order_id for x in orders):
                await message.answer('Заказ не актуален')
            else:
                user_id = orders[order_id]
  
                
                await bot.send_message(user_id,PROCESS)
                await message.answer("Отправлено")

        elif tx.startswith('/money_'):
            order_id = int(tx.split('_')[1])
            if not any( x == order_id for x in orders):
                await message.answer('Заказ не актуален')
            else:
                user_id = orders[order_id]
                
                await bot.send_message(user_id,requisites)
                await message.answer("Отправлено")


        elif tx.startswith('/decline_'):
            order_id = int(tx.split('_')[1])
            if not any( x == order_id for x in orders):
                await message.answer('Заказ не актуален')
            else:
                await message.answer("Введите время завершения")
                await form.datezkz.set()
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
        elif tx.startswith("/getus"):
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            userr = cursor.execute("SELECT id FROM Users")
            print(1)
            for user in userr:
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()
                info = cursor.execute(f'SELECT date FROM Users WHERE id = {user[0]}').fetchone()[0]
                nk = cursor.execute(f'SELECT nik FROM Users WHERE id = {user[0]}').fetchone()[0]
                print(user[0])
                my_file = open(f"date.txt", "a+")
                my_file.write(str(user[0])+"  "+"@"+nk+"  "+str(info)+"\n")
                my_file.close()
            with open(f"date.txt", "r") as f:
                text = f.read()
                await bot.send_message(message.chat.id, text = f"{text}")
            path = os.path.join(r"C:\Users\atoma\Desktop\Исходники", 'date.txt')
            os.remove(path)
    elif id not in users.keys():
        users[id] = {
            'step': 0,
            'answers': []
        }

    elif tx == BUTTON_1 and users[id]['step'] != 7:
        await bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEDbulhr4mSAaZw4Kl0vgYQcoYyyMzIaAACFxIAAsLlaUknrwiorP3jRSME")
        usid = message.from_user.id
        await message.answer(ORDER_MESSAGE)
        await sleep(1)
        conn = sqlite3.connect("infous.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO us (id,num) VALUES (?,?)",(usid,1))
        conn.commit()
        await message.answer(FIRST_QUESTION, reply_markup=kb_2)
        users[id]['step'] = 1

    elif tx == BUTTON_2 and users[id]['step'] != 7:
        users[id] = {
            'step': 0,
            'answers': []
        }
        await message.answer("Вы уверены, что хотите отменить заказ?🥺",reply_markup=choi)
        

    elif tx == BUTTON_3:
        await message.answer(CONST_MESSAGE)

    elif tx == BUTTON_4 and users[id]['step'] == 7:
        users[id] = {
            'step': 0,
            'answers': []
        }
        await message.answer("Вы уверены, что хотите отменить заказ?🥺",reply_markup=choi)     
    elif tx == "Правила":
        await message.answer("❗️Сделав заказ, вы автоматически соглашаетесь с правилами: https://docs.google.com/document/d/1dK5lvso6IKPw4PmZwLkVeEv-L3ywuPe1fN2xBs5r_q0/edit")
    elif tx == "Отзывы":
        await message.answer("Если тебе не сложно, можешь оставить свой отзыв по работе с нами тут: @ezywork_comment 🥺💜")
    elif tx == "Нет":
        usid = message.from_user.id
        conn = sqlite3.connect("infous.db")
        cursor = conn.cursor()
        try:
            num = cursor.execute(f"SELECT num FROM us WHERE id = {usid}").fetchone()[0]
            if num == 1:
                await message.answer(FIRST_QUESTION,reply_markup=kb_2)
                users[id]['answers'].append(message.message_id)
                users[id]['step'] = 1
            if num ==2:
                await message.answer(SECOND_QUESTION,reply_markup=kb_2)
                users[id]['answers'].append(message.message_id)
                users[id]['step'] = 2

            if num == 3:
                await message.answer(THIRD_QUESTION,reply_markup=kb_2)
                users[id]['answers'].append(message.message_id)
                users[id]['step'] = 3
            
            if num == 4:
                await message.answer(FIFTH_QUESTION,reply_markup=kb_2)
                users[id]['answers'].append(message.message_id)
                users[id]['step'] = 5

            if num == 5:
                await message.answer(SIXTH_QUESTION,reply_markup=kb_2)
                users[id]['answers'].append(message.message_id)
                users[id]['step'] = 6
        except:
            await message.answer("Введите сообщение для отправки",reply_markup=kb_2)
            users[id]['step'] = 100

    elif users[id]['step'] == 100:
        users[id]['answers'].append(message.message_id)
        for msg in users[id]['answers']:
            print(msg)
            await bot.forward_message(chat_id=OWNER_ID, from_chat_id=id, message_id=msg)
            await message.answer("Отправлено")

        
        
    elif users[id]['step'] == 1:
        usid = message.from_user.id
        conn = sqlite3.connect("infous.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE us SET num = 2 WHERE id = {usid}")
        conn.commit()
        await message.answer(SECOND_QUESTION)
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 2

    elif users[id]['step'] == 2:
        usid = message.from_user.id
        conn = sqlite3.connect("infous.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE us SET num = 3 WHERE id = {usid}")
        conn.commit()
        await message.answer(THIRD_QUESTION)
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 3

    elif users[id]['step'] == 3:
        usid = message.from_user.id
        conn = sqlite3.connect("infous.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE us SET num = 4 WHERE id = {usid}")
        conn.commit()
        await message.answer(FOURTH_QUESTION)
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 4

    elif users[id]['step'] == 4:
        usid = message.from_user.id
        conn = sqlite3.connect("infous.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE us SET num = 5 WHERE id = {usid}")
        conn.commit()
        await message.answer(FIFTH_QUESTION)
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 5

    elif users[id]['step'] == 5:
        usid = message.from_user.id
        conn = sqlite3.connect("infous.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE us SET num = 6 WHERE id = {usid}")
        conn.commit()
        await message.answer(SIXTH_QUESTION)
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 6

    elif users[id]['step'] == 6:
        usid = message.from_user.id
        order_id = random.randint(10000, 99999)
        while order_id in orders.keys():
            order_id = random.randint(10000, 99999)

        orders[order_id] = id

        await message.answer(FILLED_MESSAGE.format(order_id))
        users[id]['answers'].append(message.message_id)
        users[id]['step'] = 7
        conn = sqlite3.connect("infous.db")
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM us WHERE id = {usid}")
        conn.commit()
        await bot.send_message(OWNER_ID, f'Новый заказ!\n\nID Заказа: {order_id}\nПользователь: [{id}](tg://user?id={id})\n\nЧто бы задать вопрос пользователю, ответьте на это сообщение.\n\nЧто бы принять заказ отправьте команду /accept\\_{order_id}\nЧто бы отклонить заказ отправьте команду /decline\\_{order_id}\n/review\\_{order_id}\n/process\\_{order_id}\n/money\\_{order_id}',parse_mode=ParseMode.MARKDOWN)
        for msg in users[id]['answers']:
            await bot.forward_message(chat_id=OWNER_ID, from_chat_id=id, message_id=msg)

        users[id]['answers'] = []

     
    elif tx == "Да":
        await message.answer(f"Заказ отменён❗️", reply_markup=kb_1)
        await bot.send_message(OWNER_ID,f'Пользователь {message.from_user.mention} отменил заказ') 


    elif users[id]['step'] == 7:
        usid = message.from_user.id
        for order_id, user_id in orders.items():
            if user_id == id:
                break
        await bot.send_message(OWNER_ID, f'Новое сообщение по заказу: {order_id}\n\nЧто бы задать вопрос пользователю, ответьте на это сообщение.\n\nЧто бы принять заказ отправьте команду /accept_{order_id}\nЧто бы отклонить заказ отправьте команду /decline_{order_id}\n/review_{order_id}\n/process_{order_id}\n/money_{order_id}')
        await bot.forward_message(chat_id=OWNER_ID, from_chat_id=id, message_id=message.message_id)

@dp.message_handler(state = form.datezkz)
async def dat_dat(message:types.Message,state = FSMContext):
    zkz = message.text
    await state.finish()
    new = int(zkz)*60*60
    await asyncio.sleep(new)
    user_id = orders[order_id]
    del orders[order_id]
    users[user_id]['step'] = 0
    await bot.send_message(user_id, DENIED_OTMENA_MESSAGE, reply_markup=kb_1)
    await message.answer(f'Заказ № {order_id} отклонен!') 

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
