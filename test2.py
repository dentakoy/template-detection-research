import asyncio

from modules.Screen             import Screen
from modules.TemplateDetector   import TemplateDetector


async def main():
    screen              = Screen()
    templateDetector    = TemplateDetector({
        'icon1':    'templates/icon1.png',
        'icon2':    'templates/icon2.png',
        'icon3':    'templates/icon3.png',
        'icon4':    'templates/icon4.png',
        'icon5':    'templates/icon5.png',
    })

    print(await templateDetector.locateTemplate('icon1', screen.shot()))

    ss = screen.shot()
    r = await templateDetector.locateTemplates(['icon1', 'icon5'],
                                                ss)
    print(r)


asyncio.run(main())
