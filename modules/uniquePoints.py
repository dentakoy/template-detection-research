def uniquiePoints(points):
    dictionaryOfUniquies = {}

    for key, (x, y) in enumerate(points):
        dictionaryOfUniquies[f'{x}x{y}'] = key

    uniquiePoints = []
    for key in dictionaryOfUniquies:
        uniquiePoints.append(points[dictionaryOfUniquies[key]])

    return uniquiePoints
