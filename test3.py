from modules.findWindow import FindWindow

findWindow = FindWindow(['gr', 'firefox', 'ch'])

print(findWindow.getResult())
for key, values in findWindow.getResult().items():
    print(key)
    for value in values:
        print(value['title'])
        print(value['coords'])