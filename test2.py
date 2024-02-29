import asyncio

from modules.ScreenShot         import ScreenShot
from modules.TemplateDetector   import TemplateDetector


async def main():
    screenShot  = ScreenShot(2)
    td          = TemplateDetector({
        'icon1':    'templates/icon1.png',
        'icon2':    'templates/icon2.png',
        'icon3':    'templates/icon3.png',
        'icon4':    'templates/icon4.png',
        'icon5':    'templates/icon5.png',
    })

    print(await td.locateTemplate('icon1', screenShot.take()))


asyncio.run(main())
