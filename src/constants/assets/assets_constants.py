from src.constants.assets.assets_enums import assetsEnum


class AssetsConstants:
    _MODEL_DIR = 'assets/model'
    _IMAGE_DIR = 'assets/image'
    _ICON_DIR = 'assets/icons'
    _MASK_DIR = 'assets/mask'
    _VIDEO_DIR = 'assets/video'
    _THEME_DIR = "src/theme/qss"

    @staticmethod
    def get_model_path(filename : assetsEnum):
        return f'{AssetsConstants._MODEL_DIR}/{filename}'

    @staticmethod
    def get_image_path(filename : assetsEnum):
        return f'{AssetsConstants._IMAGE_DIR}/{filename}'

    @staticmethod
    def get_icon_path(filename : assetsEnum):
        return f'{AssetsConstants._ICON_DIR}/{filename}'

    @staticmethod
    def get_mask_path(filename : assetsEnum):
        return f'{AssetsConstants._MASK_DIR}/{filename}'

    @staticmethod
    def get_video_path(filename : assetsEnum):
        return f'{AssetsConstants._VIDEO_DIR}/{filename}'

    @staticmethod
    def get_theme_path(filename: assetsEnum):
        return f'{AssetsConstants._THEME_DIR}/{filename}'

    @staticmethod
    def get_classnames():
        return ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                  "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
                  "umbrella",
                  "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
                  "baseball bat",
                  "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                  "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                  "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                  "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                  "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                  "teddy bear", "hair drier", "toothbrush"
                  ]
