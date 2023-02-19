import torch



def load_model():
    run_model_path = './model-weights.pt'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=run_model_path)
    return model