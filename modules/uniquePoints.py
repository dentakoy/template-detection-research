def uniquePoints(points):
    dictionaryOfUniquePoints = {}

    for key, (x, y) in enumerate(points):
        dictionaryOfUniquePoints[f'{x}x{y}'] = key

    uniquePoints = []
    for key in dictionaryOfUniquePoints:
        uniquePoints.append(points[dictionaryOfUniquePoints[key]])

    return uniquePoints
