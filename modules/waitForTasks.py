import asyncio

async def waitForTasks( tasks,
                        timeout         = None,
                        returnWhen      = asyncio.FIRST_COMPLETED,
                        cancelPendings  = True
):
    results, pendings = await asyncio.wait(
        tasks, timeout=timeout, return_when=returnWhen)
    
    if cancelPendings:
        for key in pendings:
            pendings[key].cancel()
    
    return results
