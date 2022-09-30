import gspread


creds = {'<spreadsheet_token>'}



gc = gspread.service_account_from_dict(creds)

sh = gc.open('testspython')
worksheet = sh.worksheet("coworkers")
coworkers = worksheet.col_values(1)
worksheet_list = [i.title for i in sh.worksheets()]
print(worksheet_list)

for coworker in coworkers[1::]:
    if coworker not in worksheet_list[1::]:
        worksheet = sh.add_worksheet(title=coworker, rows="100", cols="15")
        print(f'{coworker} Создана')
        worksheet.append_row(['TG_ID', "Имя", "Фамилия", "Время", 'ВЕЖЛИВОСТЬ', 'СКОРОСТЬ', 'ЗНАНИЯ', 'ЧИСТОТА', 'КОММЕНТАРИЙ'])

    else:
        print(f'{coworker} уже существует в таблице')
