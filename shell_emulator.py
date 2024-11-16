import os
import json
import sys
import tarfile

# Функции для обработки команд
def handle_ls(current_dir):
    """Возвращает список файлов в текущей директории."""
    return os.listdir(current_dir)

def handle_cd(command, current_dir):
    """Обрабатывает команду 'cd' и возвращает новую директорию."""
    _, dir_name = command.split()  # предполагается, что команда в формате "cd <dir_name>"
    new_dir = os.path.join(current_dir, dir_name)

    if os.path.isdir(new_dir):
        return new_dir
    else:
        raise FileNotFoundError(f"Директория {new_dir} не найдена.")

def handle_du(current_dir):
    """Возвращает размер всех файлов в текущей директории."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(current_dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def handle_find(current_dir, filename):
    """Возвращает список файлов с заданным именем в текущей директории."""
    found_files = []
    for dirpath, dirnames, filenames in os.walk(current_dir):
        if filename in filenames:
            found_files.append(os.path.join(dirpath, filename))
    return found_files

def handle_who(user, host):
    """Возвращает информацию о пользователе и хосте."""
    return f"{user}@{host}"

def shell_emulator(user, host, fs_archive, log_file):
    """Основная функция эмулятора командной строки."""
    if not tarfile.is_tarfile(fs_archive):
        print("Ошибка: Некорректный формат архива.")
        sys.exit(1)

    with tarfile.open(fs_archive, 'r') as archive:
        archive.extractall("/tmp/virtual_fs")

    current_dir = "/tmp/virtual_fs"
    log_data = []

    while True:
        command = input(f"{user}@{host}:{current_dir}$ ")
        if command == "exit":
            break

        try:
            if command.startswith("ls"):
                files = handle_ls(current_dir)
                print("\n".join(files))
                log_data.append({"command": command, "output": files})

            elif command.startswith("cd"):
                current_dir = handle_cd(command, current_dir)
                log_data.append({"command": command, "output": current_dir})

            elif command.startswith("du"):
                size_info = handle_du(current_dir)
                print(f"Общий размер: {size_info} байт")
                log_data.append({"command": command, "output": size_info})

            elif command.startswith("find"):
                _, filename = command.split()
                found_files = handle_find(current_dir, filename)
                print("\n".join(found_files))
                log_data.append({"command": command, "output": found_files})

            elif command.startswith("who"):
                who_info = handle_who(user, host)
                print(who_info)
                log_data.append({"command": command, "output": who_info})

            else:
                print("Неизвестная команда.")

        except Exception as e:
            print(f"Ошибка: {e}")
            log_data.append({"command": command, "error": str(e)})

    # Запись логов в файл
    with open(log_file, 'w') as f:
        json.dump(log_data, f)

# Код для запуска программы из командной строки
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--user", required=True, help="Имя пользователя")
    parser.add_argument("--host", required=True, help="Имя хоста")
    parser.add_argument("--fs", required=True, help="Путь к архиву с файловой системой")
    parser.add_argument("--log", required=True, help="Путь к лог-файлу")
    
    args = parser.parse_args()
    
    shell_emulator(args.user, args.host, args.fs, args.log)
