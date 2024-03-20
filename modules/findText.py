import math

import pytesseract
from PIL import Image, ImageEnhance
import pandas as pd


class FindText:
    def __init__(self,
                 screen_shot,
                 textTemplates={},
                 confidence_threshold: int = 70,
                 contrast_factor: float = 2.0,
                 sharpness_factor: float = 2.0,
                 scale_factor: int = 3,
                 lang: str = 'eng'):
        self.textTemplate = {}
        self.find_text_in_image(
            screen_shot,
            textTemplates,
            confidence_threshold=confidence_threshold,
            contrast_factor=contrast_factor,
            sharpness_factor=sharpness_factor,
            scale_factor=scale_factor,
            lang=lang)

    def find_text_in_image(
            self,
            screen_shot,
            finding_text,
            confidence_threshold: int = 70,
            contrast_factor: float = 2.0,
            sharpness_factor: float = 2.0,
            scale_factor: int = 3,
            lang='eng'):
        # надо повернуть байты так как mss отдаёт BGRA
        image = Image.fromarray(screen_shot[:, :, (2, 1, 0)], 'RGB')
        # градации серого, можно сначала увеличивать, применять контрастность и прочее и потом градачии, но дольше
        # выходит

        image = image.convert('L')

        width, height = image.size

        # Создаем объект для увеличения контрастности
        enhancer = ImageEnhance.Contrast(image)

        # Увеличиваем контраст
        image = enhancer.enhance(contrast_factor)

        # Увеличение резкости
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness_factor)

        # Увеличиваем размер изображения
        image = image.resize((width * scale_factor, height * scale_factor), Image.BILINEAR)

        custom_config = r'--oem 3 --psm 11'  # 11 или 12 показали лучшие результаты
        # If you don't have tesseract executable in your PATH, include the following:
        pytesseract.pytesseract.tesseract_cmd = r'H:\Tesseract-OCR\tesseract'
        # Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

        data_text = pytesseract.image_to_data(
            image, lang=lang,
            config=custom_config,
            output_type=pytesseract.Output.DATAFRAME)

        filtered_data = data_text[data_text.conf >= confidence_threshold]

        found_texts = []

        if isinstance(finding_text, str):
            finding_texts = [finding_text]
        else:
            finding_texts = finding_text

        for search_text in finding_texts:
            if len(search_text.split(' ')) == 1:
                matches = filtered_data[filtered_data.text.str.contains(search_text, case=False, na=False)]

                for index, row in matches.iterrows():
                    bottom_right_x = row['left'] + row['width']
                    bottom_right_y = row['top'] + row['height']
                    self.textTemplate.setdefault(search_text, []).append({
                        'text': row['text'],
                        'coords': ((math.ceil(row['left'] / scale_factor), math.ceil(row['top'] / scale_factor)),
                                   (
                                       math.ceil(bottom_right_x / scale_factor),
                                       math.ceil(bottom_right_y / scale_factor))),
                        'confidence': row['conf']
                    })

            else:
                grouped_lines = filtered_data.groupby(['page_num', 'block_num', 'par_num', 'line_num'])

                for _, line in grouped_lines:
                    line_text = line['text'].str.cat(sep=' ').strip()
                    if search_text.casefold() in line_text.casefold():
                        x, y, w, h = line['left'].min(), line['top'].min(), line['width'].sum(), line['height'].max()
                        bottom_right_x = x + w
                        bottom_right_y = y + h
                        self.textTemplate.setdefault(search_text, []).append({
                            'text': line_text,
                            'coords': ((math.ceil(x / scale_factor), math.ceil(y / scale_factor)),
                                       (math.ceil(bottom_right_x / scale_factor),
                                        math.ceil(bottom_right_y / scale_factor))),
                            'confidence': line['conf'].mean()
                        })

        return found_texts

    def getResult(self):
        return self.textTemplate
