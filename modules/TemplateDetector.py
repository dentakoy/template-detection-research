from time import sleep

import asyncio
import cv2

from .uniquePoints  import uniquiePoints
from .averagePoint  import averagePoint
from .centroid      import centroid
from .waitForTasks  import waitForTasks


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
    

    def lowesFilter(self, matches, ratioThreshold = 0.4):
        filtered = []
        for match in matches:
            if match[0].distance < ratioThreshold * match[1].distance:
                filtered.append(match[0])

        return filtered
        

    async def locateTemplate(   self,
                                templateKey,
                                image,
                                isGrayImage             = False,
                                lowesRatioThreshold     = 0.4,
                                maxMatches              = 4
    ):
        keypoints, descriptors = self.featuresDetector.detectAndCompute(
            image if isGrayImage else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
            None)
        
        if type(lowesRatioThreshold) == float and lowesRatioThreshold != 0:
            all = self.featuresMatcher.knnMatch(
                descriptors, self.templates[templateKey]['descriptors'], 2)

            matches = sorted(   self.lowesFilter(all, lowesRatioThreshold),
                                key=lambda x: x.distance)[:maxMatches]
        else:
            all = self.featuresMatcher.match(
                descriptors, self.templates[templateKey]['descriptors'])
            
            matches = sorted(all, key=lambda x: x.distance)[:maxMatches]

        if len(matches) == 0:
            return False
        
        points       = uniquiePoints(self.matchesToPoints(matches, keypoints))
        pointsLength = len(points)

        if pointsLength == 1:
            return points[0]

        if pointsLength == 2:
            return averagePoint(points, pointsLength)

        return centroid(points, pointsLength)
    

    async def locateTemplates(  self,
                                templatesKeys,
                                image,
                                isGrayImage         = False,
                                lowesRatioThreshold = 0.4,
                                maxMatches          = 4,
                                timeout             = 7,
                                returnWhen          = asyncio.FIRST_COMPLETED
    ):
        tasks = []
        for key in templatesKeys:
            tasks.append(asyncio.create_task(self.locateTemplate(
                key, image, isGrayImage, lowesRatioThreshold, maxMatches)))

        return waitForTasks(tasks, timeout, returnWhen)


    async def endlessWaitForTemplate(   self,
                                        templateKey,
                                        screen,
                                        isGrayImage             = False,
                                        lowesRatioThreshold     = 0.4,
                                        maxMatches              = 4,
                                        loopDelay               = 1,
    ):
        located = False

        while not located:
            located = await self.locateTemplate(    templateKey,
                                                    screen.shot(),
                                                    isGrayImage,
                                                    lowesRatioThreshold,
                                                    maxMatches)
            await asyncio.sleep(loopDelay)

        return located


    async def waitForTemplate(  self,
                                templateKey,
                                screen,
                                timeout,
                                isGrayImage             = False,
                                lowesRatioThreshold     = 0.4,
                                maxMatches              = 4,
                                loopDelay               = 1,
    ):
        return await asyncio.wait_for(
            self.endlessWaitForTemplate(
                templateKey,
                screen,
                isGrayImage,
                lowesRatioThreshold,
                maxMatches,
                loopDelay
            ),
            timeout
        )
