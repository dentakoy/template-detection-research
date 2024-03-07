import asyncio

from modules.Screen             import Screen
from modules.TemplateDetector   import TemplateDetector
from modules.waitForTasks       import waitForTasks


async def main():
    screen              = Screen(2)
    templateDetector    = TemplateDetector({
        'icon1':    'templates/icon1.png',
        'icon2':    'templates/icon2.png',
        'icon3':    'templates/icon3.png',
        'icon4':    'templates/icon4.png',
        'icon5':    'templates/icon5.png',
    })

    #print(await templateDetector.locateTemplate('icon1', screen.shot()))

    # print(await templateDetector.locateTemplates(['icon1', 'icon5'],
    #                                              screen.shot()))

    #print(await templateDetector.waitForTemplate('icon1', screen, 10))

    print(await templateDetector.waitForTemplates(  ['icon1', 'icon5'],
                                                    screen,
                                                    10))

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
