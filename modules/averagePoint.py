def averagePoint(points, pointsLength = None):
    sumX = 0;
    sumY = 0;

    for point in points:
        sumX += point[0]
        sumY += point[1]

    pointsLength = len(points) if pointsLength is None else pointsLength
    
    return (round(sumX / pointsLength),
            round(sumY / pointsLength))
