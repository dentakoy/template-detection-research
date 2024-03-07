import asyncio

async def waitForTasks( tasks,
                        timeout         = None,
                        returnWhen      = asyncio.FIRST_COMPLETED,
                        cancelPending   = True
):
    done, pending = await asyncio.wait(
        tasks, timeout=timeout, return_when=returnWhen)

    if cancelPending:
        for task in pending:
            task.cancel()
    
    if len(tasks) == len(pending):
        raise asyncio.exceptions.TimeoutError        

    results = {}
    for task in done:
        if task.result():
            results[task.get_name()] = task.result()

    return results
