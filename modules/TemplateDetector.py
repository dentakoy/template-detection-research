import cv2


class ImageReadError(Exception):
    pass


class MissingTemplatesError(Exception):
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
            self.templates[key] = self.extractFeatures(
                self.readImage(templates[key]))

        if len(self.templates) is 0:
            raise MissingTemplatesError('Missing templates')


    def readImage(self, path):
        grayImage = cv2.imread(path, cv2.COLOR_BGR2GRAY)

        if grayImage is None:
            raise ImageReadError('cv2.imread() returns None')


    def extractFeatures(self, grayImage):
        keypoints, descriptors = self.detector.detectAndCompute(grayImage, None)

        return {
            'keypoints':    keypoints,
            'descriptors':  descriptors
        }


    async def find( self,
                    templateKey,
                    image,
                    isGrayImage = False,
                    ratio       = 0.4,
                    maxMatches  = 4
    ):
        keypoints, descriptors = self.detector.detectAndCompute(
            image if isGrayImage else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
            None
        )
        
        all = self.matcher.knnMatch(
            descriptors, self.templates[templateKey]['descriptors'], 2)
        
        filtered = []

        for match in all:
            if match[0].distance < ratio * match[1].distance:
                filtered.append(match[0])

        matches = sorted(filtered, key=lambda x: x.distance)[:maxMatches]

        if len(matches) > 0:
            # Инициализация сумм координат и подсчет количества точек
            sum_x = 0
            sum_y = 0
            num_points = len(good_matches)

            # Проход по всем точкам и накопление сумм координатye 

            for match in good_matches:
                # координата x точки из первого изображения
                sum_x += kp1[match.queryIdx].pt[0]
                # координата y точки из первого изображения
                sum_y += kp1[match.queryIdx].pt[1]
                point_x = kp1[match.queryIdx].pt[0]
                point_y = kp1[match.queryIdx].pt[1]

            # Рассчет средних координат x и y
            average_x = int(sum_x / num_points)
            average_y = int(sum_y / num_points)

            return average_x, average_y
        else:
            return False