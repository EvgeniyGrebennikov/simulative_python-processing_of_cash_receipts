import csv
from glob import glob
from re import match


def process_files(src_folder, dest_folder):
    all_files = glob(src_folder + '/*.csv')  # поиск всех файлов csv  в папке
    files_name_list = [fl.split('/')[-1] for fl in all_files]  # извлекаем название файлов из названия "путь/файл"

    format = r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d+.csv'

    required_files = sorted((match(format, fl).group() for fl in files_name_list if
                             match(format, fl)))  # список требуемых файлов (соответствующих нашему шаблону)

    with open(dest_folder + '/' + 'combined_data.csv', 'w', encoding='utf-8', newline='') as combined_data_file:
        header_columns = ['date', 'product', 'store', 'cost']  # список заголовков нового файла
        combined_data_writer = csv.DictWriter(combined_data_file, fieldnames=header_columns, delimiter=',')
        combined_data_writer.writeheader()  # записываем заголовки в файл

        for fl in required_files:
            with open(src_folder + '/' + fl, 'r', encoding='utf-8') as required_file:
                required_rows = csv.DictReader(required_file, delimiter=';')
                for row in required_rows:
                    combined_data_writer.writerow({key: value for key, value in row.items() if key in header_columns})


src_folder = 'reports-main'
dest_folder = 'comb_reports'
process_files(src_folder, dest_folder)