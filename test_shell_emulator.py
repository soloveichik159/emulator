import pytest
from shell_emulator import handle_ls, handle_cd, handle_du, handle_find, handle_who

def test_handle_ls(tmpdir):
    test_dir = tmpdir.mkdir("test")
    test_dir.join("file1.txt").write("content1")
    test_dir.join("file2.txt").write("content2")

    files = handle_ls(str(test_dir))
    assert sorted(files) == ["file1.txt", "file2.txt"]

def test_handle_cd(tmpdir):
    test_dir = tmpdir.mkdir("test")
    sub_dir = test_dir.mkdir("subdir")

    current_dir = str(test_dir)
    command = f"cd {sub_dir.basename}"
    updated_dir = handle_cd(command, current_dir)
    assert updated_dir == str(sub_dir)

def test_handle_du(tmpdir):
    test_dir = tmpdir.mkdir("test")
    test_dir.join("file1.txt").write("content1\n")  # Добавляем символ новой строки
    test_dir.join("file2.txt").write("content2\n")  # Добавляем символ новой строки

    size_info = handle_du(str(test_dir))
    assert size_info == 20  # Теперь 10 + 10 (размеры двух файлов с символами новой строки)

def test_handle_find(tmpdir):
    test_dir = tmpdir.mkdir("test")
    test_dir.join("file_to_find.txt").write("content")

    found_files = handle_find(str(test_dir), "file_to_find.txt")
    assert len(found_files) == 1
    assert found_files[0] == str(test_dir.join("file_to_find.txt"))

def test_handle_find_not_found(tmpdir):
    test_dir = tmpdir.mkdir("test")
    test_dir.join("file1.txt").write("content")

    found_files = handle_find(str(test_dir), "non_existent_file.txt")
    assert len(found_files) == 0

def test_handle_who():
    user = "test_user"
    host = "test_host"
    expected_output = f"{user}@{host}"
    
    assert handle_who(user, host) == expected_output
