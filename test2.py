import asyncio

from modules.Screen             import Screen
from modules.TemplateDetector   import TemplateDetector
from modules.waitForTasks       import waitForTasks


async def main():
    screen              = Screen(1)
    templateDetector    = TemplateDetector({
        'icon1':    'templates/icon1.png',
        'icon2':    'templates/icon2.png',
        'icon3':    'templates/icon3.png',
        'icon4':    'templates/icon4.png',
        'icon5':    'templates/icon5.png',
    })

    finded = await templateDetector.waitForTemplates(   [ 'icon1', 'icon2' ],
                                                        screen,
                                                        10)
    for key in finded:
        print(key, finded[key])
        screen.aim(finded[key])

    # screenShot = screen.shot()
    # print(await waitForTasks([
    #     templateDetector.locateTemplate('icon1', screenShot),
    #     templateDetector.locateTemplate('icon5', screenShot),
    # ]))

    # print(
    #     await waitForTasks(
    #         [
    #             templateDetector.waitForTemplate('icon1', screen, 20),
    #             templateDetector.waitForTemplate('icon5', screen, 20),
    #         ],
    #         10
    #     )
    # )


asyncio.run(main())
