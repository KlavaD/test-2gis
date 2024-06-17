Для запуска тестов клонируйте репозиторий:
```
git clone https://github.com/KlavaD/test-2gis.git
```

активируйте виртуальное окружение, установите зависимости из файла requirements.txt
```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

Обновить pip:

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```


Запустите тесты командой:
```
python -m unittest
```
