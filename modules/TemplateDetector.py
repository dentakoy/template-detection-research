import asyncio
import cv2


from .averagePoint import averagePoint
from .centroid import centroid


class LoadGrayImageException(Exception):
    pass


class MissingTemplatesException(Exception):
    pass


class TemplateDetector:
    # как передать параметры конструкторам детектора и матчера?
    def __init__(   self,
                    templates,
                    detector    = cv2.SIFT,
                    matcher     = cv2.BFMatcher
    ):
        self.detector   = detector.create()
        self.matcher    = matcher()
        self.templates  = {}

        for key in templates:
            grayImage = cv2.imread(templates[key], cv2.COLOR_BGR2GRAY)

            if grayImage is None:
                raise LoadGrayImageException('cv2.imread() returns None.')

            features = self.detector.detectAndCompute(grayImage, None)

            self.templates[key] = {
                'keypoints':    features[0],
                'descriptors':  features[1]
            }

        if len(self.templates) == 0:
            raise MissingTemplatesException('Missing templates.')


    def matchesToPoints(self, matches, keypoints):
        vertices = []
        for match in matches:
            vertices.append((   keypoints[match.queryIdx].pt[0],
                                keypoints[match.queryIdx].pt[1]))
        return vertices
            

    async def locateTemplate(   self,
                                templateKey,
                                image,
                                isGrayImage = False,
                                ratio       = 0.4,
                                maxMatches  = 4
    ):
        keypoints, descriptors = self.detector.detectAndCompute(
            image if isGrayImage else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
            None)
        
        all = self.matcher.knnMatch(
            descriptors, self.templates[templateKey]['descriptors'], 2)
        
        filtered = []
        for match in all:
            if match[0].distance < ratio * match[1].distance:
                filtered.append(match[0])

        matches = sorted(filtered, key=lambda x: x.distance)[:maxMatches]

        if len(matches) == 0:
            return False
        
        points          = self.matchesToPoints(matches, keypoints)
        pointsLength    = len(points)

        if pointsLength == 1:
            return points[0]

        if pointsLength == 2:
            return averagePoint(points, pointsLength)

        return centroid(points, pointsLength)
    
    async def locateTemplates(  self,
                                templatesKeys,
                                image,
                                isGrayImage = False,
                                ratio       = 0.4,
                                maxMatches  = 4,
                                timeout     = 7000,
                                returnWhen  = asyncio.FIRST_COMPLETED
    ):
        tasks = []
        for key in templatesKeys:
            tasks.append(
                self.locateTemplate(key, image, isGrayImage, ratio, maxMatches))

        done, pending = await asyncio.wait(
            fs=tasks, timeout=timeout, return_when=returnWhen)
        
        return done
