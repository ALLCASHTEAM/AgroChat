import os
import math
import argparse

import torch
import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler
from torch import nn
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms

from model import resnet101, resnet50
from my_dataset import MyDataSet

from utils import read_data, train_one_epoch, evaluate, read_split_data

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

def main(args):
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    print(args.model_name)
    num_classes = args.num_classes
    if os.path.exists("./weights") is False:
        os.makedirs("./weights")

    tb_writer = SummaryWriter()

    train_images_path, train_images_label, val_images_path, val_images_label ,num_classes = read_data(args.data_path)

    data_transform = {
        "train": transforms.Compose([transforms.RandomResizedCrop(224),
                                     transforms.RandomHorizontalFlip(),
                                     transforms.ToTensor(),
                                     transforms.Normalize([0.416, 0.468, 0.355], [0.210, 0.206, 0.213])]),
        "val": transforms.Compose([transforms.Resize(256),
                                   transforms.CenterCrop(224),
                                   transforms.ToTensor(),
                                   transforms.Normalize([0.416, 0.468, 0.355], [0.210, 0.206, 0.213])])}

    train_dataset = MyDataSet(images_path=train_images_path,
                              images_class=train_images_label,
                              transform=data_transform["train"])

    val_dataset = MyDataSet(images_path=val_images_path,
                            images_class=val_images_label,
                            transform=data_transform["val"])

    batch_size = args.batch_size
    nw = min([os.cpu_count(), batch_size if batch_size > 1 else 0, 8])  # number of workers
    print('Using {} dataloader workers every process'.format(nw))
    train_loader = torch.utils.data.DataLoader(train_dataset,
                                               batch_size=batch_size,
                                               shuffle=True,
                                               pin_memory=True,
                                               num_workers=nw,
                                               collate_fn=train_dataset.collate_fn)

    val_loader = torch.utils.data.DataLoader(val_dataset,
                                             batch_size=batch_size,
                                             shuffle=False,
                                             pin_memory=True,
                                             num_workers=nw,
                                             collate_fn=val_dataset.collate_fn)

    model = resnet50(num_classes=num_classes).to(device)

    if args.weights !='':
        model_dict = model.state_dict()
        model_weight_path = args.weights
        pretrained_dict = torch.load(model_weight_path, map_location='cpu')
        assert os.path.exists(model_weight_path), "file {} does not exist.".format(model_weight_path)
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if (k in model_dict and 'fc' not in k)}
        model_dict.update(pretrained_dict)
        model.load_state_dict(model_dict)

        # for param in model.parameters():
        #     param.requires_grad = False

        # change fc layer structure
        in_channel = model.fc.in_features
        model.fc = nn.Linear(in_channel, num_classes)
        model.to(device)


    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = optim.Adam(params, lr=args.lr)

    best_acc = 0.0
    for epoch in range(args.epochs):
        # train
        train_loss, train_acc = train_one_epoch(model=model,
                                                optimizer=optimizer,
                                                data_loader=train_loader,
                                                device=device,
                                                epoch=epoch)

        # validate
        val_loss, val_acc = evaluate(model=model,
                                     data_loader=val_loader,
                                     device=device,
                                     epoch=epoch)

        tags = ["train_loss", "train_acc", "val_loss", "val_acc", "learning_rate"]
        # tb_writer.add_scalar(tags[0], train_loss, epoch)
        # tb_writer.add_scalar(tags[1], train_acc, epoch)
        # tb_writer.add_scalar(tags[2], val_loss, epoch)
        # tb_writer.add_scalar(tags[3], val_acc, epoch)
        tb_writer.add_scalar(tags[4], optimizer.param_groups[0]["lr"], epoch)
        tb_writer.add_scalars(args.model_name + '_loss', {tags[0]: train_loss, tags[2]: val_loss}, epoch)
        tb_writer.add_scalars(args.model_name + '_acc', {tags[1]: train_acc, tags[3]: val_acc}, epoch)
        tb_writer.add_scalars(args.model_name,
                              {tags[0]: train_loss, tags[1]: train_acc, tags[2]: val_loss, tags[3]: val_acc,
                               tags[4]: optimizer.param_groups[0]["lr"]}, epoch)

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), "/home/xinyudong/program/agriculture/ResNet/weights/{}-model-{}.pth".format(args.model_name, epoch))
            print('save best acc {:.3f}'.format(best_acc))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_classes', type=int, default=120)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--batch-size', type=int, default=128)
    parser.add_argument('--lr', type=float, default=0.01)
    parser.add_argument('--lrf', type=float, default=0.01)

    parser.add_argument('--data-path', type=str,
                        default="/home/xinyudong/Datasets/PlantDiseased/")
    parser.add_argument('--model-name', default='ResNet50-Plant', help='model name')

    # 预训练权重路径，如果不想载入就设置为空字符
    parser.add_argument('--weights', type=str, default="",
                        help='initial weights path')
    # 是否冻结权重
    parser.add_argument('--freeze-layers', type=bool, default=False)
    parser.add_argument('--device', default='cuda:0', help='device id (i.e. 0 or 0,1 or cpu)')

    opt = parser.parse_args()

    main(opt)
