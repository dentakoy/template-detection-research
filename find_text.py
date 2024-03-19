import math

import pytesseract
from PIL import Image, ImageEnhance, ImageDraw, ImageChops
import pandas as pd

from modules.Screen import Screen


def find_text_in_image(
        screen_shot,
        finding_text: str,
        confidence_threshold: int = 70,
        contrast_factor: float = 2.0,
        sharpness_factor: float = 2.0,
        scale_factor: int = 3,
        lang='eng'):

    # надо повернуть байты так как mss отдаёт BGRA
    image = Image.fromarray(screen_shot[:, :, (2, 1, 0)], 'RGB')
    # градации серого, можно сначала увеличивать, применять контрастность и прочее и потом градачии, но дольше выходит

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

    
    custom_config = r'--oem 3 --psm 11' # 11 или 12 показали лучшие результаты
    data_text = pytesseract.image_to_data(
        image, lang=lang,
        config=custom_config,
        output_type=pytesseract.Output.DATAFRAME)

    filtered_data = data_text[data_text.conf >= confidence_threshold]

    found_texts = []

    if len(finding_text.split(' ')) == 21:
        matches = filtered_data[filtered_data.text.str.contains(finding_text, case=False, na=False)]

        for index, row in matches.iterrows():
            bottom_right_x = row['left'] + row['width']
            bottom_right_y = row['top'] + row['height']
            found_texts.append({
                'text': row['text'],
                'coords': ((math.ceil(row['left'] / scale_factor), math.ceil(row['top'] / scale_factor)),
                          (math.ceil(bottom_right_x / scale_factor), math.ceil(bottom_right_y / scale_factor))),
                'confidence': row['conf']
            })

    else:
        grouped_lines = filtered_data.groupby(['page_num', 'block_num', 'par_num', 'line_num'])

        for _, line in grouped_lines:
            line_text = line['text'].str.cat(sep=' ').strip()
            print(line_text)
            if finding_text.casefold() in line_text.casefold():
                x, y, w, h = line['left'].min(), line['top'].min(), line['width'].sum(), line['height'].max()
                bottom_right_x = x + w
                bottom_right_y = y + h
                found_texts.append({
                    'text': line_text,
                    'coords': ((math.ceil(x / scale_factor), math.ceil(y / scale_factor)),

                              (math.ceil(bottom_right_x / scale_factor), math.ceil(bottom_right_y / scale_factor))),
                    'confidence': line['conf'].mean()
                })

    return found_texts


screen = Screen(1)

search_text = "next"
threshold = 10
contrast = 1.15
langue = 'eng'

found_texts_info = find_text_in_image(
                            screen.shot(),
                            search_text,
                            threshold,
                            contrast_factor=contrast,
                            scale_factor=5, 
                            lang=langue)

for text_info in found_texts_info:
    print(text_info)
