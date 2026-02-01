import easyocr
import numpy as np
from PIL import Image

def get_easyocr_result(image_path):

    reader = easyocr.Reader(['ko', 'en'])

    results = reader.readtext(image_path)

    easy_text = ""
    for (bbox, text, prob) in results:
        easy_text += f"{text} "
        
    return easy_text