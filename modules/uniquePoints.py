def uniquiePoints(points):
    uniqueDictionary = {}

    for point in points:
        uniqueDictionary[f'{point[0]}x{point[1]}'] = point

    points = []
    for key in uniqueDictionary:
        points.append(uniqueDictionary[key])

    return points
