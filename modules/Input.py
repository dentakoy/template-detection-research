from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as KeyboardController, Key, KeyCode
import random
import re
import time
from platform import system

# Создаем объект контроллера мыши и клавиатуры
__mouse = Controller()
__keyboard = KeyboardController()
random.seed()


def mouse_click(x: int, y: int, isRight: bool = False, isDoubleClick: bool = False):
    count_click = 1
    if isDoubleClick:
        count_click = 2
    __mouse.position = (x, y)

    if isRight:
        __mouse.click(Button.right, count_click)
    else:
        __mouse.click(Button.left, count_click)

    delay = random.uniform(0.1, 0.5)
    time.sleep(delay)


def input_text(text: str, delay_min: float = 0.1, delay_max: float = 0.7):

    for char in text:
        __keyboard.press(char)
        delay = random.uniform(delay_min, delay_max)  # Генерировать случайную задержку между нажатием кнопки
        time.sleep(delay)
        __keyboard.release(char)
        delay = random.uniform(delay_min, delay_max)  # Генерировать случайную задержку между отпусканием кнопки
        time.sleep(delay)


def press_key(key):
    if isinstance(key, str):
        __keyboard.tap(key)  # Использовать tap() вместо press() и release() для одиночных символов
    else:
        __keyboard.press(key)
        __keyboard.release(key)
    time.sleep(0.1)


def press_keys(keys):
    if any(isinstance(k, str) for k in keys):
        # Если есть одиночные символы, нажимаем их по отдельности
        for key in keys:
            press_key(key)
    else:
        # Если только комбинации клавиш, используем pressed()
        with __keyboard.pressed(keys[0].value):
            for key in keys[1:]:
                __keyboard.press(key)
                time.sleep(0.1)
                __keyboard.release(key)
        time.sleep(0.1)


def extract_key_name(key_list):
    pattern = re.compile(r'<(Key.w+):.*?>')

    # Используем генератор списка для обработки каждого элемента в исходном списке
    clean_keys = [pattern.sub(r'1', str(key)).strip("'") for key in key_list]

    return clean_keys


def rename_windows_key(key_list):
    replace_dict = {'ctrl': '^', 'alt': '%', 'shift': '+', 'space': ' ', 'page_down': 'pgdn', 'page_up': 'pgup'}

    renamed_keys = []
    for key in key_list:
        key = key.replace('Key.', '')  # Убираем 'Key.'
        for old_key, new_key in replace_dict.items():
            key = key.replace(old_key, new_key)

        key = key.upper()  # Переводим в верхний регистр
        if len(key) > 1:
            key = '{' + key + '}'

        renamed_keys.append(key)

    # как по другому пофиксить проблему с заменой backspace я не нашёл
    for i, key in enumerate(renamed_keys):
        if key == '{BACK }':
            renamed_keys[i] = '{BACKSPACE}'

    return renamed_keys


def press_windows_keys(keys):
    import win32com.client
    shell = win32com.client.Dispatch('WScript.Shell')
    extract_name = extract_key_name(keys)
    rename = rename_windows_key(extract_name)
    join_keys = ''.join(rename)

    shell.SendKeys(join_keys)
    time.sleep(0.1)


def press_combo_keys(keys: str):
    isWindows = False
    keys_combo = keys.split('+')
    keys_array = []
    if system() == 'Windows':
        isWindows = True

    for key in keys_combo:
        if len(key) == 1:  # Если это одиночная буква
            key_code = KeyCode.from_char(key.lower())
            keys_array.append(key_code)  # Добавляем ее как объект Key
        else:
            try:
                keys_array.append(eval(f'Key.{key}'))  # Попытка преобразовать строку в объект Key
            except AttributeError:
                print(f"Неизвестная комбинация клавиш: {key}")


    if len(keys_array) == 1 and not isWindows:
        press_key(keys_array[0])
    else:
        if isWindows:
            press_windows_keys(keys_array)
        else:
            press_keys(keys_array)
