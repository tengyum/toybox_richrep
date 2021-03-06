import torch
import torch.nn as nn
import util

from nets.classic_net import get_classicnet
from exps.trainer import ToyboxTrainer

torch.backends.cudnn.benchmark = True


def exp_main(ratios, trs, nview, net_name, pretrained, batch_size, epochs, preload):
    net = get_classicnet(net_name=net_name, pretrained=pretrained)
    net.cuda()

    optimizer = torch.optim.Adam(net.parameters(), lr=5e-05, weight_decay=0.0)
    loss_func = nn.CrossEntropyLoss()
    hyper_p = util.HyperP(
        lr=0.5,
        batch_size=batch_size,
        num_workers=0,
        epochs=epochs,
        preload=preload,
        pretrain='pretrain' if pretrained else 'no_pretrain'
    )
    tb_trainer = ToyboxTrainer(
        tr=trs,
        nview=nview,
        ratio=ratios,
        mode='sv',
        img_size=(299, 299),
        net=net,
        net_name=net_name,
        optimizer=optimizer,
        loss_func=loss_func,
        hyper_p=hyper_p
    )
    print(f'=== {tb_trainer.exp_name} ===')
    tb_trainer.train_test_save()


def main():
    ratios = [100]
    trs = ['rzplus', 'rzminus']
    nview = 12  # need to <18
    net_name = 'resnext50_32x4d'
    exp_main(ratios, trs, nview, net_name)


if __name__ == '__main__':
    main()
