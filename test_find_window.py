import screen_analysis_module as sam
from window_module import get_scale_factor

get_scale_factor() # Если строку комментировать то get_window_title_coord возвращает координаты в виртуальных пикселях
# без учета масштабирования, а если строка есть то всё ок хотя scale_factory не меняется


find_title = "mozilla firefox"
result = sam.get_window_title_coord(find_title)

if result is not None:
    if min(result) >= 0:
        print(f"Координаты окна: {find_title}: {result}")
    else:
        print(f"Окно {find_title} свёрнуто")
else:
    print(f"Окно {find_title} не найдено")
