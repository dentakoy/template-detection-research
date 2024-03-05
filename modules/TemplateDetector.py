import asyncio
import cv2

from .averagePoint  import averagePoint
from .centroid      import centroid


class LoadGrayImageException(Exception):
    pass


class MissingTemplatesException(Exception):
    pass


class TemplateDetector:
    def __init__(   self,
                    templates,
                    featuresDetector            = cv2.SIFT,
                    featuresDetectorArguments   = {},
                    featuresMatcher             = cv2.FlannBasedMatcher,
                    featuresMatcherArguments    = {}
    ):
        self.featuresDetector   = featuresDetector.create(
                                    **featuresDetectorArguments)
        
        self.featuresMatcher    = featuresMatcher.create(
                                    **featuresMatcherArguments)    
        self.templates = {}
        for key in templates:
            grayImage = cv2.imread(templates[key], cv2.COLOR_BGR2GRAY)

            if grayImage is None:
                raise LoadGrayImageException('cv2.imread() returns None.')

            features = self.featuresDetector.detectAndCompute(grayImage, None)

            self.templates[key] = {
                'keypoints':    features[0],
                'descriptors':  features[1]
            }

        if len(self.templates) == 0:
            raise MissingTemplatesException('Missing templates.')


    def matchesToPoints(self, matches, keypoints):
        points = []
        for match in matches:
            points.append(( keypoints[match.queryIdx].pt[0],
                            keypoints[match.queryIdx].pt[1]))
        return points
            

    async def locateTemplate(   self,
                                templateKey,
                                image,
                                isGrayImage             = False,
                                lowesRatioThreshold     = 0.45,
                                maxMatches              = 3
    ):
        keypoints, descriptors = self.featuresDetector.detectAndCompute(
            image if isGrayImage else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
            None)
        
        all = self.featuresMatcher.knnMatch(
            descriptors, self.templates[templateKey]['descriptors'], 2)
        
        if lowesRatioThreshold:
            filtered = []
            for match in all:
                if match[0].distance < lowesRatioThreshold * match[1].distance:
                    filtered.append(match[0])

            matches = sorted(filtered,  key=lambda x: x.distance)[:maxMatches]
        else:
            matches = sorted(all,       key=lambda x: x.distance)[:maxMatches]

        # нужно добавить удаление дубилкатов в matches перед срезом maxMatches,
        # иначе может происходить деление на ноль в функции centroid()

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
                                isGrayImage         = False,
                                lowesRatioThreshold = 0.45,
                                maxMatches          = 3,
                                timeout             = 7000,
                                returnWhen          = asyncio.FIRST_COMPLETED
    ):
        tasks = []
        for key in templatesKeys:
            tasks.append(asyncio.create_task(self.locateTemplate(
                key, image, isGrayImage, lowesRatioThreshold, maxMatches)))

        done, pending = await asyncio.wait(
            tasks, timeout=timeout, return_when=returnWhen)
        
        # нужно ли вызывать .cancel для всех pending tasks?
        
        return done


    # async def waitForTemplate(  self,
    #                             templateKey,
    #                             screen,
    #                             timeout,
    #                             lowesRatioThreshold     = 0.45,
    #                             maxMatches              = 3
    # ):
    #     ...