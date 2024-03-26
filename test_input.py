import modules.Input as input


text_to_type = "Hello"
input.mouse_click(400, 400)
input.press_combo_keys('ctrl+A')
input.press_combo_keys('delete')
input.press_combo_keys('home')
input.input_text(text_to_type)


input.press_combo_keys('ctrl+a')  # Выделит весь текст
input.press_combo_keys('ctrl+c')  # Скопировать весь текст
input.press_combo_keys('page_down') 

input.press_combo_keys('enter')
input.press_combo_keys('ctrl+v')  # Вставит скопированный текст
input.press_combo_keys('alt+f4')  # Закроет текущее окно