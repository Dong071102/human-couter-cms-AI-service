# from ultralytics import YOLO

# # Load a model
# model = YOLO("models/best.pt")  # load a custom trained model

# # Export the model
# model.export(format="onnx")

from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("models/best.pt")

# Export the model to TensorRT format
model.export(format="engine")  # creates 'yolo11n.engine'

# Load the exported TensorRT model
tensorrt_model = YOLO("yolo11n.engine")