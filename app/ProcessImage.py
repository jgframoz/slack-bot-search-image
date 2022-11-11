import pytesseract
import cv2

from services.log import LogService

class ProcessImage:

    def image_to_text(path_to_image):
        try:
            image = cv2.imread(path_to_image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            LogService.log(e)
            return ''