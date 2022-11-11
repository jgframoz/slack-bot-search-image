class ImageService:
    @staticmethod
    def save_image(file_name, file_data):
        with open(file_name , 'w+b') as f:
            f.write(bytearray(file_data))