import torch
import json
from AI_PRO_MAX.utils.model import resnet101
from torchvision import transforms
from PIL import Image

json_path = 'AI_PRO_MAX/ind2name.json'

data_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.416, 0.468, 0.355], [0.210, 0.206, 0.213])
])
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def image_process(image_path):
    image = (Image.open(image_path)).convert('RGB')
    image = data_transform(image).unsqueeze(dim=0)
    image = image.to(device)
    return image


def load_classes(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def model_init(num_classes: int, model_path: str, device: str):
    model = resnet101(num_classes=num_classes).to(device)
    model_dict = model.state_dict()
    pretrained_dict = {k: v for k, v in torch.load(model_path, map_location=device).items() if
                       (k in model_dict and 'fc' not in k)}
    model_dict.update(pretrained_dict)
    model.load_state_dict(model_dict)
    return model


def predict(model, image, classes):
    model.eval()
    with torch.no_grad():
        output = model(image)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        max_prob, preds = torch.max(probabilities, dim=1)
        predicted_class = classes[str(preds.item())]
        return predicted_class, max_prob.item()


def main(image_path):
    model = model_init(120, "AI_PRO_MAX/ResNet_101-ImageNet-model-99.pth", device)
    classes = load_classes(json_path)
    image = image_process(image_path)
    prediction, probability = predict(model, image, classes)
    return [prediction, probability]


if __name__ == "__main__":
    result, probability = main(image_path="opisanie-boleznej-tomatov-65.jpg")
    print(f"Predicted Class: {result}, Probability: {probability:.2f}")
