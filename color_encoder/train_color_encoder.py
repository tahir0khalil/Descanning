import os
import sys

import random
import numpy as np
from datetime import datetime

import torch
from torch import nn, optim
from torch.utils.data import DataLoader

from dataset_color_encoder import ColorEncoderDataset
from utils_color_encoder import *
from color_encoder_trainer import *


def main(logging=False):

    if logging:
        time = datetime.now().strftime("%y%m%d_%H%M%S")
        sys.stdout = open("log_ColorEncoder_{}.txt".format(time), "w")

    train_path = '/home/tahir/workspace2/descan_extension/data_set/Descan_dataset/Train'
    valid_path = '/home/tahir/workspace2/descan_extension/data_set/Descan_dataset/Valid'

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device: ", device)

    seed = random.randint(1, 10000)    
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    print('Random seed: {}'.format(seed))

    batch_size = 8
    num_epochs = 10
    save_epoch = 2
    lr = 3e-4
    weight_decay = 1e-5
    MODEL = 'R34' # R50

    color_encoder_dataset = ColorEncoderDataset(train_path)
    train_dataloader = DataLoader(color_encoder_dataset, batch_size=batch_size, shuffle=True, drop_last=True, num_workers=0)
    print('The number of Data: ', len(color_encoder_dataset))

    model = initialize_model(device, MODEL)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

    model = train(model, train_dataloader, valid_path, criterion, optimizer, device, num_epochs, save_epoch)

    # Save last model
    weight_path = '../weights_final'
    os.makedirs(weight_path, exist_ok=True)
    torch.save(model.state_dict(), f'{weight_path}/color_encoder.h5')

    if logging:
        sys.stdout.close()

if __name__ == '__main__':
    main()
