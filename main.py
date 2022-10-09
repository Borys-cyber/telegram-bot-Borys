from aiogram import Bot, Dispatcher, executor, types
import os
import sqlite3

TOKEN = os.environ['token']
# print(TOKEN)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users={}
def add_db(users_id, u_name, email, phone):
    connect = sqlite3.connect('user_inews.db')
    cursor = connect.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS USERSiNEWS(users_id integer AUTOINCREMENT, u_name text NOT NULL, email text, phone text)')
    cursor.execute(f'INSERT INTO USERSiNEWS (users_id, u_name, email, phone) VALUES (?, ?, ?, ?)', (users_id, u_name, email, phone))
    connect.commit()
    connect.close()
@dp.message_handler()
async def echo(message: types.Message):
    print(message.from_user.id, ' - ', message.from_user.first_name, ' - ', message.text)
    users.update({message.from_user.id: message.from_user.first_name})

    for i in users:
        await bot.send_message(chat_id=i, text=message.text)
    text = f'"Пользователь" {message.from_user.first_name} "написал" {message.text}'
    for i in users.keys():
        if i != message.from_user.id:
            await bot.send_message(chat_id=i,
                                   text=text)
    users_id = message.from_user.id
    u_name = message.from_user.first_name
    email = "?"
    phone = "?"
    add_db(users_id=users_id, u_name=u_name, email=email, phone=phone)


if __name__ == '__main__':
    executor.start_polling(dp)




