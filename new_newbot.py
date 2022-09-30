from aiogram import Bot, Dispatcher, executor, types
from datetime import date

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from constant import *
import logging
from markups import *
import datetime
import gspread
from state import *



# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=bot_token, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
gc = gspread.service_account_from_dict(configs)
sh = gc.open('coworkers')
print(sh.sheet1.get('A1'))
worksheet = sh.worksheet("coworkers")
coworkers = worksheet.col_values(1)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    worksheet_users = sh.worksheet("users")
    users = worksheet_users.col_values(1)
    if str(chat_id) in users:
        if str(chat_id) in admin:
            first_name = message.from_user.first_name
            message_for_user = text[26] % (first_name, first_name)
            await message.answer(message_for_user, reply_markup=generate_admin_buttons())
        else:
            first_name = message.from_user.first_name
            message_for_user = text[25] % (first_name, first_name)
            await bot.send_message(chat_id, message_for_user)
            await bot.send_message(chat_id, text[2], reply_markup=generate_main_menu(coworkers[1::]))
            await Answer.coworkers_state.set()
    else:
        first_name = message.from_user.first_name
        message_for_user = text[0] % (first_name, first_name)
        await bot.send_message(chat_id, message_for_user, reply_markup=generate_phone_number())
        await Answer.contact.set()



@dp.message_handler(content_types=types.ContentType.CONTACT, state=Answer.contact)
async def send_contact(message: types.Message, state: FSMContext):
    '''Bu funksiya foydalanuvchi contact jo'natganda ushlab oladi'''
    chat_id = message.chat.id
    contact = message.contact.phone_number
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    coworkers = worksheet.col_values(1)
    worksheet_users = sh.worksheet('users')
    worksheet_users.append_row([chat_id, first_name, last_name, contact])

    await state.finish()
    if str(chat_id) in admin:
        first_name = message.from_user.first_name
        message_for_user = text[26] % (first_name, first_name)
        await message.answer(message_for_user, reply_markup=generate_admin_buttons())
    else:
        await bot.send_message(chat_id, text[2], reply_markup=generate_main_menu(coworkers[1::]))
        await Answer.coworkers_state.set()

'''Qo'shish'''

@dp.message_handler(text=text[19])
async def add_coworker(message: types.Message):
    chat_id = message.chat.id
    '''Bu funksiya google sheetsga list koworker qo'shadi.'''
    await bot.send_message(chat_id, "Введите имя и направление коворкера", reply_markup=generate_back_button())
    await Answer.add_coworker.set()

@dp.message_handler(state=Answer.add_coworker)
async def add_coworker_state(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == text[17]:
        await bot.send_message(chat_id, text[18] % message.from_user.first_name, reply_markup=generate_admin_buttons())
        await state.finish()
    else:
        teacher = message.text
        worksheet.col_values(1) # Birinchi ustundagi barcha qiymatlarni olish
        worksheet_list = [i.title for i in sh.worksheets()]
        if teacher not in worksheet_list[1::]:
            worksheet.append_row([teacher])
            new_worksheet = sh.add_worksheet(title=teacher, rows="1000", cols="15")
            new_worksheet.append_row(
                ['TG_ID', "Имя", "Фамилия", "Время", 'ВЕЖЛИВОСТЬ', 'СКОРОСТЬ', 'ЗНАНИЯ', 'ЧИСТОТА', 'КОММЕНТАРИЙ'])
            await bot.send_message(chat_id, f'Таблица {teacher} создана')
        else:
            # print(text[23] % (teacher))  # Agar o'qituvchi tablitsada bo'lsa
            await message.answer(text[23] % (teacher), reply_markup=generate_admin_buttons())
            await state.finish()

# Таблица Qobiljon python создана

'''Baholash'''

@dp.message_handler(text=text[22])
async def evaluation_coworker(message: types.Message):
    '''Bu funksiya yordamida koworkerlar baholanadi.'''
    '''Bu yerda funksiya ichida worksheetdan koworkerslar ro'yxatini olamiz. Yopilgan koworkersni o'chirish kerak'''
    await bot.send_message(message.chat.id, 'Пожалуйста подождите...')
    chat_id = message.chat.id
    coworkers = worksheet.col_values(1)
    await bot.send_message(chat_id, text[2], reply_markup=generate_main_menu(coworkers[1::]))
    await Answer.coworkers_state.set()


@dp.message_handler(state=Answer.coworkers_state)
async def send_evaluation_coworker(message: types.Message, state: FSMContext):
    coworkers = worksheet.col_values(1)
    chat_id = message.chat.id
    await bot.send_message(message.chat.id, 'Пожалуйста подождите...')
    try:
        if message.text == text[17]:
            if str(chat_id) in admin:
                await bot.send_message(chat_id, text[18] % message.from_user.first_name, reply_markup=generate_admin_buttons())
                await state.reset_state(with_data=False)
            else:
                pass
        elif message.text in coworkers[1::]:

            chat_id = message.chat.id

            now = datetime.datetime.now()
            today = now.strftime('%d-%m-%Y')

            worksheet_teacher = sh.worksheet(message.text)

            user_col_values = worksheet_teacher.col_values(1)
            date_col_values = worksheet_teacher.col_values(4)
            s = -1
            a = 1
            for i in user_col_values:
                s += a

                if user_col_values[s] == str(chat_id) and date_col_values[s] == today:
                    await bot.send_message(chat_id, text[3])
                    await bot.send_message(chat_id, '', reply_markup=generate_main_menu(coworkers[1::]))
            "Zo'r!!!!!!!!!"
            await state.update_data(
                {'teacher': message.text}
                    )

            data = await state.get_data()
            teacher = data.get('teacher')

            await message.answer(text[4] % (teacher, teacher))
            await message.answer(text[6] % (teacher, teacher), reply_markup=generate_marks())
            await Answer.next()
    except:
        coworkers = worksheet.col_values(1)
        if message.text not in coworkers:
            await bot.send_message(chat_id, text[5])



@dp.message_handler(state=Answer.politeness)
async def politeness(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    data = await state.get_data()
    teacher = data.get('teacher')

    if message.text == text[17]:
        await state.finish()
        await bot.send_message(chat_id, text[2], reply_markup=generate_main_menu(coworkers[1::]))
        await Answer.coworkers_state.set()
    elif message.text in ['1', '2', '3', '4', '5']:
        num1 = message.text
        await state.update_data(
            {'num1': num1}
        )

        await bot.send_message(chat_id, text[7] % (teacher, teacher), reply_markup=generate_marks())
        await Answer.next()


@dp.message_handler(state=Answer.speed)
async def speed(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    data = await state.get_data()
    teacher = data.get('teacher')

    if message.text == text[17]:
        await state.finish()
        await bot.send_message(chat_id, text[2], reply_markup=generate_main_menu(coworkers[1::]))
        await Answer.coworkers_state.set()
    elif message.text in ['1', '2', '3', '4', '5']:
        num2 = message.text
        await state.update_data(
            {'num2': num2}
        )
        await bot.send_message(chat_id, text[8] % (teacher, teacher), reply_markup=generate_marks())
        await Answer.next()


@dp.message_handler(state=Answer.knowledge)
async def knowledge(message: types.Message, state: FSMContext):
    '''Bu funksiya o'qituvchining bilimini baholaydi'''

    data = await state.get_data()
    teacher = data.get('teacher')

    chat_id = message.chat.id
    if message.text == text[17]:
        await state.finish()
        await bot.send_message(chat_id, text[2], reply_markup=generate_main_menu(coworkers[1::]))
        await Answer.coworkers_state.set()
    elif message.text in ['1', '2', '3', '4', '5']:
        num3 = message.text
        await state.update_data(
            {'num3': num3}
        )
        await bot.send_message(chat_id, text[9], reply_markup=generate_marks())
        await Answer.next()


@dp.message_handler(state=Answer.purity)
async def purity(message: types.Message, state: FSMContext):
    '''Bu funksiya coworkingdagi tozallikaga baho beradi'''

    data = await state.get_data()
    teacher = data.get('teacher')

    chat_id = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    now = datetime.datetime.now()
    today = now.strftime('%d-%m-%Y')

    if message.text == text[17]:
        await state.finish()
        await bot.send_message(chat_id, text[2], reply_markup=generate_main_menu(coworkers[1::]))
        await Answer.coworkers_state.set()
    elif message.text in ['1', '2', '3', '4', '5']:
        num4 = message.text
        await state.update_data(
            {'num4': num4}
        )

        data = await state.get_data()
        num1 = data.get('num1')
        num2 = data.get('num2')
        num3 = data.get('num3')
        num4 = data.get('num4')

        if (num1 == '5') and (num2 == '5') and (num3 == '5') and (num4 == '5'):
            await state.finish()
            worksheet_teacher = sh.worksheet(teacher)
            worksheet_teacher.append_row([chat_id, first_name, last_name, today, num1, num2, num3, num4])
            await bot.send_message(chat_id, text[11])
            await bot.send_message(chat_id, text[2], reply_markup=generate_main_menu(coworkers[1::]))
            await Answer.coworkers_state.set()

            col_values5 = worksheet_teacher.col_values(5)
            col_values6 = worksheet_teacher.col_values(6)
            col_values7 = worksheet_teacher.col_values(7)
            col_values8 = worksheet_teacher.col_values(8)
            lists = [col_values5, col_values6, col_values7, col_values8]
            await collar(lists, teacher)

        else:
            await bot.send_message(chat_id, text[10], reply_markup=generate_skip_button())
            await Answer.next()


@dp.message_handler(state=Answer.comment)
async def comments(message: types.Message, state: FSMContext):
    coworkers = worksheet.col_values(1)

    chat_id = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    now = datetime.datetime.now()
    today = now.strftime('%d-%m-%Y')

    await state.update_data(
        {'comment': message.text}
    )
    data = await state.get_data()
    teacher = data.get('teacher')
    num1 = data.get('num1')
    num2 = data.get('num2')
    num3 = data.get('num3')
    num4 = data.get('num4')
    comment = data.get('comment')

    worksheet_teacher = sh.worksheet(teacher)

    if message.text == text[17]:
        await state.finish()
        await bot.send_message(chat_id, text[2], reply_markup=generate_main_menu(coworkers[1::]))
        await Answer.coworkers_state.set()

    elif message.text == "Пропустить / Oʻtkazib yuborish":
        worksheet_teacher.append_row([chat_id, first_name, last_name, today, num1, num2, num3, num4])
        await bot.send_message(chat_id, text[11])
        await state.finish()
        await bot.send_message(chat_id, text[2], reply_markup=generate_main_menu(coworkers[1::]))
        await Answer.coworkers_state.set()

        col_values5 = worksheet_teacher.col_values(5)
        col_values6 = worksheet_teacher.col_values(6)
        col_values7 = worksheet_teacher.col_values(7)
        col_values8 = worksheet_teacher.col_values(8)
        lists = [col_values5, col_values6, col_values7, col_values8]
        await collar(lists, teacher)

    else:
        worksheet_teacher.append_row([chat_id, first_name, last_name, today, num1, num2, num3, num4, comment])

        await state.finish()
        await bot.send_message(chat_id, text[12])
        await bot.send_message(chat_id, text[2], reply_markup=generate_main_menu(coworkers[1::]))
        await Answer.coworkers_state.set()

        col_values5 = worksheet_teacher.col_values(5)
        col_values6 = worksheet_teacher.col_values(6)
        col_values7 = worksheet_teacher.col_values(7)
        col_values8 = worksheet_teacher.col_values(8)
        lists = [col_values5, col_values6, col_values7, col_values8]
        await collar(lists, teacher)



'''O'chirish'''

@dp.message_handler(text=text[20])
async def delete_coworker(message: types.Message):
    '''Bu funksiya google sheetsdagi coworker ni o'chiradi'''
    chat_id = message.chat.id
    coworkers = worksheet.col_values(1)
    await bot.send_message(chat_id, text[20], reply_markup=generate_main_menu(coworkers[1::]))
    await Answer.del_teacher.set()


@dp.message_handler(state=Answer.del_teacher)
async def delete_coworker_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    try:
        if message.text == text[17]:
            await state.finish()
            await bot.send_message(chat_id, text[18] % message.from_user.first_name, reply_markup=generate_admin_buttons())
        else:
            worksheet = sh.worksheet("coworkers")
            coworkers = worksheet.col_values(1)
            teachers = sh.worksheets()
            for teacher in teachers:
                if message.text == teacher.title:
                    index_co = coworkers.index(message.text)
                    a = worksheet.delete_rows((index_co + 1))

                    sh.del_worksheet(teacher)
                    await bot.send_message(chat_id, text[24] % (teacher.title))
    except Exception as e:
        await bot.send_message(chat_id, f"{e}")


async def collar(lists, teacher):
    coworkers = worksheet.col_values(1)

    for list_teacher in lists:
        length = len(list_teacher)-1
        sum_elements = 0
        for element in list_teacher:
            if element in ['3', '5', '3', '4', '5']:
                element = int(element)
                sum_elements += element

        average_value = round(sum_elements/length, 2)
        teacher_index = coworkers.index(teacher) + 1
        for coworker in coworkers:
            if coworker == teacher:
                if 'ВЕЖЛИВОСТЬ' in list_teacher:
                    worksheet.update_cell(teacher_index, 2, average_value)
                elif 'СКОРОСТЬ' in list_teacher:
                    worksheet.update_cell(teacher_index, 3, average_value)
                elif 'ЗНАНИЯ' in list_teacher:
                    worksheet.update_cell(teacher_index, 4, average_value)
                elif 'ЧИСТОТА' in list_teacher:
                    worksheet.update_cell(teacher_index, 5, average_value)

executor.start_polling(dp, skip_updates=True)