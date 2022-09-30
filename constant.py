admin = ['<admins>']

configs = {'<spreadsheet_token>'}

bot_token = '<api_token>'


text = {
0: f'''🇷🇺 👋Здравствуйте %s!
Это бот оценки работы преподавателей коворкинга учебного центра PROWEB.
Здесь вы можете оценить работу преподавателей и условия коворкинга.
Отправьте свой контакт для завершения регистрации по кнопке ниже  👇
-----------------------

🇺🇿 👋Assalomu aleykum %s!
Ushbu bot Proweb o`quv markazining kovorkingdagi o'qituvchilariga baho berish uchun. 
Bunda siz kovorkingdagi sharoit va qulayliklar hamda o'qituvchilarga baho berishingiz mumkin.  
Ro'yxatdan o'tish uchun kontaktingizni quyidagi tugma orqali yuboring
''',
1:
'''🇷🇺 Введена неверная команда
-----------------------
🇺🇿 Noto`g`ri buyruq kiritilgan
''',
2:'''🇷🇺 Мы собираем оценки студентов для улучшения качества коворкинга. 
Для того чтобы оставить отзыв о работе коворкинга выберите преподавателя коворкинга из списка ниже 👇
-----------------------

🇺🇿 Kovorking sifatini oshirish uchun baho bering. 
Kovorking faoliyati haqida izoh qoldirish uchun, quyidagi ro`yxatdan o`qituvchini tanlang 👇
''',
3:'''🇷🇺 К сожалению Вы уже оставляли отзыв о данном преподавателе сегодня
-----------------------

🇺🇿 Afsuski Siz ushbu o’qituvchi haqida izoh qoldirdingiz
''',
4:f'''🇷🇺 Пожалуйста дайте оценку преподавателю
<b>%s</b>
по следующим пунктам:
-----------------------

🇺🇿 Iltimos quyidagi mezonlar bo`yicha o'qituvchiga baho bering 
<b>%s</b>
''',
5:'''🇷🇺 Такого преподавателя не существует. Пожалуйста выберите преподавателя из списка ниже 👇
-----------------------
🇺🇿 Bunaqa o`qituvchi yo`q. Iltimos quyidagi ro`yxatdan o`qituvchini  tanlang  👇
''',



6:f'''🇷🇺 Оцените вежливость преподавателя <b>%s</b>
-----------------------
🇺🇿 O`qituvchini xushmuomilaligi haqida baho bering <b>%s</b>
''',

7:f'''🇷🇺 Оцените как быстро преподаватель <b>%s</b> справляется с помощью студентам
-----------------------
🇺🇿 O’qituvchi qay darajada tez muammoni hal qilganligi haqida baho bering <b>%s</b>
''',

8:f'''🇷🇺 Оцените знания преподавателя <b>%s</b>
-----------------------
🇺🇿 O`qituvchi bilimga baho bering <b>%s</b>
''',
9:'''🇷🇺 Оцените обстановку в коворкинге (шум, чистота, удобство)
-----------------------
🇺🇿 Kovorkingdagi muhitga baho bering (shovqin, tozzalik, qulayliklar)
''',
10:'''🇷🇺 Пожалуйста оставьте комментарий по поводу своих оценок
-----------------------
🇺🇿 Iltimos baholar haqida izoh qoldiring
''',
11:'''🇷🇺 Спасибо за Вашу оценку 👍
-----------------------
🇺🇿 Baho berganingiz uchun rahmat 👍
''',
12:'''🇷🇺 Спасибо за Вашу оценку 👍
В ближайшее время мы исправим все недостатки 
-----------------------
🇺🇿 Baho berganingiz uchun rahmat 👍
Tez orada kamchiliklar bartaraf etiladi 👍
''',
13:'''🇷🇺 Нажмите на кнопку Поделитесь контактом!
-----------------------
🇺🇿 Kontaktni ulashish  tugmasini bosing!
''',
14:'''🇷🇺 Оцените от 1 до 5 или выберите оценку ниже 👇
-----------------------
🇺🇿 1-5 gacha bo’lgan baholash tizimida baho bering 👇
''',
15:'''🇷🇺 Оставить отзыв на преподавателя коворкинга
-----------------------
🇺🇿 Kovorking o`qituvchisi haqida izoh qoldiring 
''',
16:'''✏️Написать / ✏️Yozish''',

17:'''◀️ Назад / ◀️Orqaga''',
18:f'''%s что желаете сделать?''',
19:'''Добавить коворкера''',
20:'''Удалить коворкера''',
21:'''Введите имя и направление коворкера''',
22:'''Оценить коворкера''',
23:f'''%s уже существует в таблице''',
24:f'''Вы удалили %s''',
25: f'''🇷🇺 👋Здравствуйте %s!
Это бот оценки работы преподавателей коворкинга учебного центра PROWEB.
Здесь вы можете оценить работу преподавателей и условия коворкинга.
-----------------------

🇺🇿 👋Assalomu aleykum %s!
Ushbu bot Proweb o`quv markazining kovorkingdagi o'qituvchilariga baho berish uchun. 
Bunda siz kovorkingdagi sharoit va qulayliklar hamda o'qituvchilarga baho berishingiz mumkin.  
''',
26: f'''🇷🇺 👋Здравствуйте %s!
Это бот оценки работы преподавателей коворкинга учебного центра PROWEB.
Здесь вы можете добавить преподавателей в таблицу коворкинга, удалить преподавателей из таблицы и поставить ему оценку.
-----------------------

🇺🇿 👋Assalomu aleykum %s!
Ushbu bot Proweb o`quv markazining kovorkingdagi o'qituvchilariga baho berish uchun.
Bu yerda siz kovorking jadvaliga o'qituvchi qo'shishingiz, jadvaldan o'qituvchini o'chirishingiz hamda ularni baholashingiz mumkin.  
'''
}
