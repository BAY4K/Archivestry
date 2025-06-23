import os
from pyzipper import *

# Пути к папкам и файлам
proj_dir = os.getcwd()

_source_folder_path = proj_dir + '\\Осень 2024'
_file_to_copy_path = proj_dir + '\\Сопровод.pdf'
_result_folder_path = proj_dir + '\\result'

# Создаем папку result, если она не существует
os.makedirs(_result_folder_path, exist_ok=True)


# Проходим по всем файлам в исходной папке
def archive_files(source_folder_path=_source_folder_path, result_folder_path=_result_folder_path,
                  is_password=False, password=None,
                  is_add_file=False, file_to_copy_path=None):
    os.makedirs(result_folder_path, exist_ok=True)
    for filename in os.listdir(source_folder_path):
        file_path = os.path.join(source_folder_path, filename)

        # Пропускаем папки
        if os.path.isdir(file_path):
            continue

        # Создаем имя для архива без расширения файла
        base_filename = os.path.splitext(filename)[0]
        zip_filename = f"{base_filename}.zip"
        zip_path = os.path.join(result_folder_path, zip_filename)

        if is_password:
            with AESZipFile(zip_path, mode='w', compression=ZIP_DEFLATED,
                            encryption=WZ_AES) as z:
                z.setpassword(password)  # Устанавливаем пароль
                z.write(file_path, filename)
                if is_add_file:
                    name = file_to_copy_path.split(r'/')[-1]
                    z.write(file_to_copy_path, name)
        else:
            with AESZipFile(zip_path, mode='w', compression=ZIP_DEFLATED) as z:
                z.write(file_path, filename)
                if is_add_file:
                    name = file_to_copy_path.split(r'/')[-1]
                    z.write(file_to_copy_path, name)
