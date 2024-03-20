from modules.findWindow import FindWindow
from modules.findText import FindText
from modules.Screen import Screen

# findWindow = FindWindow(['gr', 'firefox', 'ch'])
#
# print(findWindow.getResult())
# for key, values in findWindow.getResult().items():
#     print(key)
#     for value in values:
#         print(value['title'])
#         print(value['coords'])
screen = Screen(1)

search_text = ["account", "mail or"]
lang = 'eng'

findText = FindText(screen.shot(), 'coming soon', lang=lang, scale_factor=1)

print(findText.getResult())
