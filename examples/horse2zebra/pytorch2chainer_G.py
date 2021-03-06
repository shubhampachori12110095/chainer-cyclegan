#!/usr/bin/env python

import os.path as osp

import chainer
import numpy as np
import torch

import chainer_cyclegan


here = osp.dirname(osp.realpath(__file__))

model_file = osp.join(here, 'data/G_horse2zebra.pth')
state_dict = torch.load(model_file)

params = []
for k, v in state_dict.items():
    print(k)
    if 'running' not in k:
        params.append(v.numpy().flatten())
params = np.hstack(params)
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
print('G original (PyTorch)')
print(params.size, params.min(), params.mean(), params.max())
print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

model = chainer_cyclegan.models.ResnetGenerator()

params = []
for param in model.params():
    params.append(param.array.flatten())
params = np.hstack(params)
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
print('G init (Chainer)')
print(params.size, params.min(), params.mean(), params.max())
print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

np.copyto(model.l1.W.array, state_dict['model.1.weight'].numpy())
np.copyto(model.l1.b.array, state_dict['model.1.bias'].numpy())
np.copyto(model.l2.avg_mean, state_dict['model.2.running_mean'].numpy())
np.copyto(model.l2.avg_var, state_dict['model.2.running_var'].numpy())
np.copyto(model.l4.W.array, state_dict['model.4.weight'].numpy())
np.copyto(model.l4.b.array, state_dict['model.4.bias'].numpy())
np.copyto(model.l5.avg_mean, state_dict['model.5.running_mean'].numpy())
np.copyto(model.l5.avg_var, state_dict['model.5.running_var'].numpy())
np.copyto(model.l7.W.array, state_dict['model.7.weight'].numpy())
np.copyto(model.l7.b.array, state_dict['model.7.bias'].numpy())
np.copyto(model.l8.avg_mean, state_dict['model.8.running_mean'].numpy())
np.copyto(model.l8.avg_var, state_dict['model.8.running_var'].numpy())

for i in range(10, 19):
    l_dst = getattr(model, 'l{:d}'.format(i))
    np.copyto(
        l_dst.l1.W.array,
        state_dict['model.{:d}.conv_block.1.weight'.format(i)].numpy())
    np.copyto(
        l_dst.l1.b.array,
        state_dict['model.{:d}.conv_block.1.bias'.format(i)].numpy())
    np.copyto(
        l_dst.l2.avg_mean,
        state_dict['model.{:d}.conv_block.2.running_mean'.format(i)].numpy())
    np.copyto(
        l_dst.l2.avg_var,
        state_dict['model.{:d}.conv_block.2.running_var'.format(i)].numpy())
    np.copyto(
        l_dst.l5.W.array,
        state_dict['model.{:d}.conv_block.5.weight'.format(i)].numpy())
    np.copyto(
        l_dst.l5.b.array,
        state_dict['model.{:d}.conv_block.5.bias'.format(i)].numpy())
    np.copyto(
        l_dst.l6.avg_mean,
        state_dict['model.{:d}.conv_block.6.running_mean'.format(i)].numpy())
    np.copyto(
        l_dst.l6.avg_var,
        state_dict['model.{:d}.conv_block.6.running_var'.format(i)].numpy())

np.copyto(model.l19.W.array, state_dict['model.19.weight'].numpy())
np.copyto(model.l19.b.array, state_dict['model.19.bias'].numpy())
np.copyto(model.l20.avg_mean, state_dict['model.20.running_mean'].numpy())
np.copyto(model.l20.avg_var, state_dict['model.20.running_var'].numpy())
np.copyto(model.l22.W.array, state_dict['model.22.weight'].numpy())
np.copyto(model.l22.b.array, state_dict['model.22.bias'].numpy())
np.copyto(model.l23.avg_mean, state_dict['model.23.running_mean'].numpy())
np.copyto(model.l23.avg_var, state_dict['model.23.running_var'].numpy())
np.copyto(model.l26.W.array, state_dict['model.26.weight'].numpy())
np.copyto(model.l26.b.array, state_dict['model.26.bias'].numpy())

params = []
for param in model.params():
    params.append(param.array.flatten())
params = np.hstack(params)
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
print('G copied (Chainer)')
print(params.size, params.min(), params.mean(), params.max())
print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

model_file = osp.join(here, 'data/G_horse2zebra_from_pytorch.npz')
chainer.serializers.save_npz(model_file, model)
print('Saved model file: {:s}'.format(model_file))
