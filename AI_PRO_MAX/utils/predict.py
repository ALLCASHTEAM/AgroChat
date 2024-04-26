import argparse
import os
import json

import torch
from torchvision import transforms

from model import resnet101
from my_dataset import MyDataSet
from utils import read_test_data, evaluate
import ipdb

def main(args):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    batch_size = args.batch_size


    test_images_path, test_images_label,num_classes = read_test_data(args.data_path)

    data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.416, 0.468, 0.355], [0.210, 0.206, 0.213])])

    # load image
    # img_path = "../tulip.jpg"
    # assert os.path.exists(img_path), "file: '{}' dose not exist.".format(img_path)
    # img = Image.open(img_path)
    # plt.imshow(img)
    # [N, C, H, W]
    # img = data_transform(img)
    # # expand batch dimension
    # img = torch.unsqueeze(img, dim=0)

    nw = min([os.cpu_count(), batch_size if batch_size > 1 else 0, 8])

    test_dataset = MyDataSet(images_path=test_images_path,
                            images_class=test_images_label,
                            transform=data_transform)

    test_loader = torch.utils.data.DataLoader(test_dataset,
                                             batch_size=batch_size,
                                             shuffle=False,
                                             pin_memory=True,
                                             num_workers=nw,
                                             collate_fn=test_dataset.collate_fn)

    # read class_indict
    json_path = './class_indices.json'
    assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

    with open(json_path, "r") as f:
        class_indict = json.load(f)


    # create model
    model_weight_path = args.weights

    model = resnet101(num_classes=num_classes).to(device)
    pretrained_dict = torch.load(model_weight_path, map_location='cpu')
    model_dict = model.state_dict()
    pretrained_dict = {k: v for k, v in pretrained_dict.items() if (k in model_dict and 'fc' not in k)}
    model_dict.update(pretrained_dict)
    model.load_state_dict(model_dict)
    # in_channel = model.fc.in_features
    # model.fc = nn.Linear(in_channel, 120)
    # model.to(device)

    # # load model weights
    # model_weight_path = args.weights
    # model.load_state_dict(torch.load(model_weight_path))

    model.eval()
    evaluate(model=model, data_loader=test_loader, device=device, epoch=1)
    # with torch.no_grad():
    #     # predict class
    #     output = torch.squeeze(model(img.to(device))).cpu()
    #     predict = torch.softmax(output, dim=0)
    #     predict_cla = torch.argmax(predict).numpy()
    #
    # print_res = "class: {}   prob: {:.3}".format(class_indict[str(predict_cla)],
    #                                              predict[predict_cla].numpy())
    # plt.title(print_res)
    # for i in range(len(predict)):
    #     print("class: {:10}   prob: {:.3}".format(class_indict[str(i)],
    #                                               predict[i].numpy()))
    # plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_classes', type=int, default=120)
    parser.add_argument('--epochs', type=int, default=200)
    parser.add_argument('--batch-size', type=int, default=128)
    parser.add_argument('--data-path', type=str,
                        default="/home/xinyudong/Datasets/test_dataset/test/")
    parser.add_argument('--weights', type=str, default="/home/xinyudong/program/agriculture/test_weight/ResNet101-ImageNet-model-98.pth",
                        help='initial weights path')
    parser.add_argument('--freeze-layers', type=bool, default=False)
    parser.add_argument('--device', default='cuda:0', help='device id (i.e. 0 or 0,1 or cpu)')

    opt = parser.parse_args()
    main(opt)
