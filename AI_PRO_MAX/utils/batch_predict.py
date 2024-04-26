import os
import json

import torch
from PIL import Image
from torchvision import transforms

from model import resnet101


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.416, 0.468, 0.355], [0.210, 0.206, 0.213])])

    # load image
    # 指向需要遍历预测的图像文件夹
    root = "/home/xinyudong/Datasets/test_dataset/test/"
    assert os.path.exists(root), f"file: '{root}' dose not exist."
    # 读取指定文件夹下所有jpg图像路径
    diseased_path_list = sorted([os.path.join(root, i) for i in os.listdir(root)])

    # read class_indict
    json_path = 'class_indices.json'
    assert os.path.exists(json_path), f"file: '{json_path}' dose not exist."

    json_file = open(json_path, "r")
    class_indict = json.load(json_file)

    # create model
    model = resnet101(num_classes=20).to(device)

    pic_num=0
    true_num =0

    # load model weights
    weights_path = "/home/xinyudong/program/agriculture/test_weight/ResNet101-ImageNet&Plant-model-89.pth"
    assert os.path.exists(weights_path), f"file: '{weights_path}' dose not exist."
    model.load_state_dict(torch.load(weights_path, map_location=device))
    for num, disease_class in enumerate(diseased_path_list):
        imgs_root = disease_class + '/'
        img_path_list = [os.path.join(imgs_root, i) for i in os.listdir(imgs_root) if i.endswith(".jpg")]
        # prediction
        model.eval()
        batch_size = 8  # 每次预测时将多少张图片打包成一个batch
        count = 0
        with torch.no_grad():
            for ids in range(0, len(img_path_list) // batch_size):
                img_list = []
                for img_path in img_path_list[ids * batch_size: (ids + 1) * batch_size]:
                    assert os.path.exists(img_path), f"file: '{img_path}' dose not exist."
                    img = Image.open(img_path)
                    img = data_transform(img)
                    img_list.append(img)

                # batch img
                # 将img_list列表中的所有图像打包成一个batch
                batch_img = torch.stack(img_list, dim=0)
                # predict class
                output = model(batch_img.to(device)).cpu()
                predict = torch.softmax(output, dim=1)
                probs, classes = torch.max(predict, dim=1)
                for cls in classes:
                    if cls.numpy() != num:
                        count=count+1

                for idx, (pro, cla) in enumerate(zip(probs, classes)):
                    print("image: {}  class: {}  prob: {:.3}".format(img_path_list[ids * batch_size + idx],
                                                                     class_indict[str(cla.numpy())],
                                                                     pro.numpy()))
        pic_num = pic_num+len(img_path_list)
        true_num = true_num+(len(img_path_list)-count)
        print('一共有'+str(len(img_path_list))+'图片,预测对的图片有：'+str(len(img_path_list)-count))
    print(true_num/pic_num)
if __name__ == '__main__':
    main()
