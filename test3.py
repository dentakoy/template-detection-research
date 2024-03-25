from modules.findWindow import FindWindow
import re
from modules.findText import FindText
from modules.Screen import Screen


pattern_gr = re.compile(r'gr', re.IGNORECASE)
pattern_firefox = re.compile(r'Firefox')
pattern_chrome = re.compile(r'chrome', re.IGNORECASE)


findWindow = FindWindow([pattern_gr, pattern_firefox, pattern_chrome])

print(findWindow.getResult())
for key, values in findWindow.getResult().items():
    print(key)
    for value in values:
        print(value['title'])
        print(value['coords'])

exit(0)
screen = Screen(1)

search_text = ["account", "mail or"]
lang = 'eng'

findText = FindText(screen.shot(), 'coming soon', lang=lang, scale_factor=1)

print(findText.getResult())
