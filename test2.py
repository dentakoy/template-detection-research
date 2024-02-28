from modules.TemplateDetector import TemplateDetector

td = TemplateDetector({
    'icon1':    'templates/icon1.png',
    'icon2':    'templates/icon2.png',
    'icon3':    'templates/icon3.png',
    'icon4':    'templates/icon4.png',
    'icon5':    'templates/icon5.png',
})

# import matplotlib.pyplot as plt

# # Создание пустой фигуры и осей
# fig = plt.figure()
# ax = fig.add_axes([0, 0, 1, 1])

# # Установка свойств окна
# fig.canvas.manager.window.attributes('-fullscreen', True)
# fig.canvas.manager.window.attributes('-topmost', True)
# fig.canvas.manager.window.wm_attributes('-alpha', 1)

# # Скрытие панели инструментов
# fig.canvas.toolbar_visible = False

# Отрисовка фигуры
#plt.show()

#plt.figure()
#plt.plot([1,2], [1,2])

# # Option 1
# # QT backend
# manager = plt.get_current_fig_manager()
# manager.window.showMaximized()

# # Option 2
# # TkAgg backend
# manager = plt.get_current_fig_manager()
# manager.resize(*manager.window.maxsize())

# Option 3
# WX backend
# manager = plt.get_current_fig_manager()
# manager.frame.Maximize(True)

# plt.show()
# plt.savefig('templates/icon1.png')
