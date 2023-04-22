# Vehicle Detection and Counting with YOLOv8 and PyQt5

This project is an implementation of vehicle detection and counting using YOLOv8 object detection model and PyQt5 GUI framework. The project is capable of detecting and counting vehicles in a given video.

## Requirements

- Python 3.6 or higher
- PyQt5
- OpenCV
- Pytorch

You can install these dependencies by running the following command:

pip install -r requirements.txt


## Usage

1. Clone the repository:

git clone https://github.com/IstakozNecmi/VehicleDetectCounting-PyQt5_GUI-Yolov8.git


2. Navigate to the cloned repository:

cd VehicleDetectCounting-PyQt5_GUI-Yolov8

3. Run the program:

python main.py


4. Select the input video file.

5. Press the Start button to start detecting and counting the vehicles in the video.

## Custom Model

This project comes with a pre-trained YOLOv8 object detection model. However, you can train your own custom model by following these steps:

1. Prepare the dataset by collecting and annotating images.

2. Generate the `train.txt` and `valid.txt` files containing the paths to the training and validation images.

3. Modify the `data/custom.data` file to specify the number of classes and the paths to the `train.txt` and `valid.txt` files.

4. Download the pre-trained weights file from the official YOLOv8 repository.

5. Train the model using the following command:

python train.py --data data/custom.data --cfg cfg/custom.cfg --weights weights/yolov8.weights --batch-size 32


6. Once the model is trained, modify the `config.py` file to specify the paths to the custom model weights and configuration files.

## Acknowledgements

This project was inspired by the [YOLOv5 repository](https://github.com/ultralytics/yolov5) and the [Vehicle Detection and Tracking project](https://github.com/udacity/CarND-Vehicle-Detection).
