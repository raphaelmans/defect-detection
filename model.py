import torch
from torchvision import transforms as T
import torch.nn.functional as F
import streamlit as st
from features.models.classification_result import ClassificationResultInsertDTO

from helper import get_mysql_timestamp


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def load_model():
    run_model_path = './model-weights.pt'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=run_model_path)

    return model


def predict(model, image):

    IMAGENET_MEAN = 0.485, 0.456, 0.406
    IMAGENET_STD = 0.229, 0.224, 0.225

    def classify_transforms(size=224):
        return T.Compose([T.ToTensor(), T.Resize(size), T.CenterCrop(size), T.Normalize(IMAGENET_MEAN, IMAGENET_STD)])

    transformations = classify_transforms()
    convert_tensor = transformations(image)
    convert_tensor = convert_tensor.unsqueeze(0)

    output = model(convert_tensor)
    return output


def evaluate(model, result, batch_id)->ClassificationResultInsertDTO:
    pred = F.softmax(result, dim=1)

    for i, prob in enumerate(pred):
        top5i = prob.argsort(0, descending=True)[:1].tolist()
        test_res = top5i[0]
        label = model.names[test_res]
        # prob_result = prob[test_res]

        eval_result = ClassificationResultInsertDTO(
            class_name=label,
            created_at=get_mysql_timestamp(),
            batch_id=batch_id
        )
    
        return eval_result
