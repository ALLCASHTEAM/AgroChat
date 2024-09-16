import torch
import json
from AI_PRO_MAX.utils.model import resnet101
from torchvision import transforms
from PIL import Image

json_path = 'AI_PRO_MAX/ind2name.json'
eng_json_path = 'AI_PRO_MAX/ind2nameEng.json'

data_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.416, 0.468, 0.355], [0.210, 0.206, 0.213])
])
device = torch.device("cpu")

# Фиксация случайных состояний для воспроизводимости
torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(42)


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
    with torch.no_grad():
        output = model(image).to(device)
        tmp = torch.max(output, dim=1)[1]
        tmp = tmp.item()
        print_res = classes[0][str(tmp)]
        eng_results = classes[1][str(tmp)]
        print(print_res)
        return [print_res, eng_results]


model = model_init(120, "AI_PRO_MAX/ResNet_101-ImageNet-model-99.pth", device)
model.eval()


def main(image_path):
    classes = load_classes(json_path)
    eng_classes = load_classes(eng_json_path)
    image = image_process(image_path)
    return predict(model, image, [classes, eng_classes])


if __name__ == "__main__":
    result = main(image_path="opisanie-boleznej-tomatov-65.jpg")
    print(result)
