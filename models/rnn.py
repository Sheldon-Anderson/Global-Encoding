import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.nn.utils.rnn import pack_padded_sequence as pack
from torch.nn.utils.rnn import pad_packed_sequence as unpack
import models
import math
import numpy as np


class rnn_encoder(nn.Module):

    def __init__(self, config, embedding=None):
        super(rnn_encoder, self).__init__()

        self.embedding = embedding if embedding is not None else nn.Embedding(config.src_vocab_size, config.emb_size)
        self.hidden_size = config.hidden_size
        self.config = config
<<<<<<< HEAD

        if config.swish:
            self.sw1 = nn.Sequential(nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=1, padding=0), nn.BatchNorm1d(config.hidden_size), nn.ReLU())
            self.sw3 = nn.Sequential(nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=1, padding=0), nn.ReLU(), nn.BatchNorm1d(config.hidden_size),
                                     nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=3, padding=1), nn.ReLU(), nn.BatchNorm1d(config.hidden_size))
            self.sw33 = nn.Sequential(nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=1, padding=0), nn.ReLU(), nn.BatchNorm1d(config.hidden_size),
                                      nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=3, padding=1), nn.ReLU(), nn.BatchNorm1d(config.hidden_size),
                                      nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=3, padding=1), nn.ReLU(), nn.BatchNorm1d(config.hidden_size))
            self.linear = nn.Sequential(nn.Linear(2*config.hidden_size, 2*config.hidden_size), nn.GLU(), nn.Dropout(config.dropout))
            self.filter_linear = nn.Linear(3*config.hidden_size, config.hidden_size)
            self.tanh = nn.Tanh()
            self.sigmoid = nn.Sigmoid()

        if config.selfatt:
            if config.attention == 'None':
                self.attention = None
            elif config.attention == 'bahdanau':
                self.attention = models.bahdanau_attention(config.hidden_size, config.emb_size, config.pool_size)
            elif config.attention == 'luong':
                self.attention = models.luong_attention(config.hidden_size, config.emb_size, config.pool_size)
            elif config.attention == 'luong_gate':
                self.attention = models.luong_gate_attention(config.hidden_size, config.emb_size)

||||||| merged common ancestors
        self.dropout = nn.Dropout(p=0.02)
        self.sw1 = nn.Sequential(nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=1, padding=0), nn.BatchNorm1d(config.hidden_size), nn.ReLU())
        self.sw3 = nn.Sequential(nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=1, padding=0), nn.ReLU(), nn.BatchNorm1d(config.hidden_size), nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=3, padding=1), nn.ReLU(), nn.BatchNorm1d(config.hidden_size))
        self.sw33 = nn.Sequential(nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=1, padding=0), nn.ReLU(), nn.BatchNorm1d(config.hidden_size), nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=3, padding=1), nn.ReLU(), nn.BatchNorm1d(config.hidden_size), nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=3, padding=1), nn.ReLU(), nn.BatchNorm1d(config.hidden_size))
        self.swish = nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=5, padding=2)
        '''self.swish = nn.Sequential(nn.Conv1d(config.hidden_size, 128, kernel_size=7, padding=3), nn.SELU(), nn.MaxPool1d(5, stride=1, padding=2),
                                   nn.Conv1d(128, 128, kernel_size=5, padding=2), nn.SELU(), nn.AvgPool1d(3, stride=1, padding=1),
                                   nn.Conv1d(128, config.hidden_size, kernel_size=3, padding=1), nn.Sigmoid())'''
        self.linear = nn.Sequential(nn.Linear(2*config.hidden_size, 2*config.hidden_size), nn.GLU())
        self.filter_linear = nn.Linear(3*config.hidden_size, config.hidden_size)
        self.tanh = nn.Tanh()
        self.sigmoid = nn.Sigmoid()
        self.linear2 = nn.Linear(config.hidden_size, 1)
        self.sigmoid1 = nn.Sigmoid()
        self.PosEnc = PositionalEncoding(config)
        if config.attention == 'None':
            self.attention = None
        elif config.attention == 'bahdanau':
            self.attention = models.bahdanau_attention(config.hidden_size, config.emb_size, config.pool_size)
        elif config.attention == 'luong':
            self.attention = models.luong_attention(config.hidden_size, config.emb_size, config.pool_size)
        elif config.attention == 'luong_gate':
            self.attention = models.luong_gate_attention(config.hidden_size, config.emb_size)
=======
        self.dropout = nn.Dropout(p=0.02)
        self.sw1 = nn.Sequential(nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=1, padding=0), nn.BatchNorm1d(config.hidden_size), nn.ReLU())
        self.sw3 = nn.Sequential(nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=1, padding=0), nn.ReLU(), nn.BatchNorm1d(config.hidden_size), nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=3, padding=1), nn.ReLU(), nn.BatchNorm1d(config.hidden_size))
        self.sw33 = nn.Sequential(nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=1, padding=0), nn.ReLU(), nn.BatchNorm1d(config.hidden_size), nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=3, padding=1), nn.ReLU(), nn.BatchNorm1d(config.hidden_size), nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=3, padding=1), nn.ReLU(), nn.BatchNorm1d(config.hidden_size))
        self.swish = nn.Conv1d(config.hidden_size, config.hidden_size, kernel_size=5, padding=2)
        self.linear = nn.Sequential(nn.Linear(2*config.hidden_size, 2*config.hidden_size), nn.GLU(), nn.Dropout(config.dropout))
        self.filter_linear = nn.Linear(3*config.hidden_size, config.hidden_size)
        self.tanh = nn.Tanh()
        self.sigmoid = nn.Sigmoid()
        self.PosEnc = PositionalEncoding(config)
        if config.attention == 'None':
            self.attention = None
        elif config.attention == 'bahdanau':
            self.attention = models.bahdanau_attention(config.hidden_size, config.emb_size, config.pool_size)
        elif config.attention == 'luong':
            self.attention = models.luong_attention(config.hidden_size, config.emb_size, config.pool_size)
        elif config.attention == 'luong_gate':
            self.attention = models.luong_gate_attention(config.hidden_size, config.emb_size)
>>>>>>> b020a51dce99c2d814cf2beaf01ca842dadff7f6
        if config.cell == 'gru':
            self.rnn = nn.GRU(input_size=config.emb_size, hidden_size=config.hidden_size,
                              num_layers=config.enc_num_layers, dropout=config.dropout,
                              bidirectional=config.bidirectional)
        else:
            self.rnn = nn.LSTM(input_size=config.emb_size, hidden_size=config.hidden_size,
                               num_layers=config.enc_num_layers, dropout=config.dropout,
                               bidirectional=config.bidirectional)

    def forward(self, inputs, lengths):
<<<<<<< HEAD
        embs = pack(self.embedding(inputs), lengths)
        outputs, state = self.rnn(embs)
        outputs = unpack(outputs)[0]
        if self.config.bidirectional:
||||||| merged common ancestors
        if self.config.resRNN:
            embs = pack(self.embedding(inputs), lengths)
            inputs = unpack(embs)[0]
            embeds = inputs
        else:
            embs = pack(self.embedding(inputs), lengths)
            embeds = unpack(embs)[0]
            if self.config.attemb:
                outputs, state = self.rnnpos(embs)
                outputs = unpack(outputs)[0]
                self.attention.init_context(context = outputs)
                out_attn = []
                for i, emb in enumerate(embeds.split(1)):
                    output, attn = self.attention(emb.squeeze(0), embeds)
                    out_attn.append(output)
                embs = torch.stack(out_attn)
            outputs, state = self.rnn(embeds)
            if self.config.attemb:
                outputs = outputs
            else:
                outputs = outputs
            if self.config.bidirectional:
                #outputs = outputs[:, :, :self.hidden_size] + outputs[:, :, self.hidden_size:]
                outputs = self.linear(outputs)
=======
        embs = pack(self.embedding(inputs), lengths)
        embeds = unpack(embs)[0]
        outputs, state = self.rnn(embs)
        outputs = unpack(outputs)[0]
        if self.config.bidirectional:
>>>>>>> b020a51dce99c2d814cf2beaf01ca842dadff7f6
            if self.config.swish:
<<<<<<< HEAD
                outputs = self.linear(outputs)
            else:
                outputs = outputs[:,:,:self.config.hidden_size] + outputs[:,:,self.config.hidden_size:]
        if self.config.swish:
            outputs = outputs.transpose(0,1).transpose(1,2)
            conv1 = self.sw1(outputs)
            conv3 = self.sw3(outputs)
            conv33 = self.sw33(outputs)
            conv = torch.cat((conv1, conv3, conv33), 1)
            conv = self.filter_linear(conv.transpose(1,2))
            if self.config.selfatt:
                conv = conv.transpose(0,1)
                outputs = outputs.transpose(1,2).transpose(0,1)
            else:
||||||| merged common ancestors
                outputs = self.PosEnc(outputs)
                outputs = outputs.transpose(0,1).transpose(1,2)
                conv1 = self.sw1(outputs)
                conv3 = self.sw3(outputs)
                conv33 = self.sw33(outputs)
                conv = torch.cat((conv1, conv3, conv33), 1)
                conv = self.filter_linear(conv.transpose(1,2))#.transpose(0,1)
                #outputs = outputs.transpose(1,2).transpose(0,1)
=======
                outputs = self.linear(outputs)
            else:
                outputs = outputs[:,:,:self.config.hidden_size] + outputs[:,:,self.config.hidden_size:]
        if self.config.swish:
            outputs = self.PosEnc(outputs)
            outputs = outputs.transpose(0,1).transpose(1,2)
            conv1 = self.sw1(outputs)
            conv3 = self.sw3(outputs)
            conv33 = self.sw33(outputs)
            conv = torch.cat((conv1, conv3, conv33), 1)
            conv = self.filter_linear(conv.transpose(1,2))
            if self.config.selfatt:
                conv = conv.transpose(0,1)
                outputs = outputs.transpose(1,2).transpose(0,1)
            else:
>>>>>>> b020a51dce99c2d814cf2beaf01ca842dadff7f6
                gate = self.sigmoid(conv)
                outputs = outputs * gate.transpose(1,2)
                outputs = outputs.transpose(1,2).transpose(0,1)

        if self.config.selfatt:
            self.attention.init_context(context=conv)
            out_attn, weights = self.attention(conv, selfatt=True)
            gate = self.sigmoid(out_attn)
            outputs = outputs * gate

        if self.config.cell == 'gru':
            state = state[:self.config.dec_num_layers]
        else:
            state = (state[0][::2], state[1][::2])

        return outputs, state



class rnn_decoder(nn.Module):

    def __init__(self, config, embedding=None, use_attention=True):
        super(rnn_decoder, self).__init__()
        self.embedding = embedding if embedding is not None else nn.Embedding(config.tgt_vocab_size, config.emb_size)

        input_size = config.emb_size

        if config.cell == 'gru':
            self.rnn = StackedGRU(input_size=input_size, hidden_size=config.hidden_size,
                                  num_layers=config.dec_num_layers, dropout=config.dropout)
        else:
            self.rnn = StackedLSTM(input_size=input_size, hidden_size=config.hidden_size,
                                   num_layers=config.dec_num_layers, dropout=config.dropout)

        self.linear = nn.Linear(config.hidden_size, config.tgt_vocab_size)
        self.linear_ = nn.Linear(config.hidden_size, config.hidden_size)
        self.sigmoid = nn.Sigmoid()

        if not use_attention or config.attention == 'None':
            self.attention = None
        elif config.attention == 'bahdanau':
            self.attention = models.bahdanau_attention(config.hidden_size, config.emb_size, config.pool_size)
        elif config.attention == 'luong':
            self.attention = models.luong_attention(config.hidden_size, config.emb_size, config.pool_size)
        elif config.attention == 'luong_gate':
            self.attention = models.luong_gate_attention(config.hidden_size, config.emb_size, prob=config.dropout)

        self.hidden_size = config.hidden_size
        self.dropout = nn.Dropout(config.dropout)
        self.config = config

    def forward(self, input, state):
        embs = self.embedding(input)
        output, state = self.rnn(embs, state)
        if self.attention is not None:
            if self.config.attention == 'luong_gate':
                output, attn_weights = self.attention(output)
            else:
                output, attn_weights = self.attention(output, embs)
        else:
            attn_weights = None
        
        output = self.compute_score(output)

        return output, state, attn_weights

    def compute_score(self, hiddens):
        scores = self.linear(hiddens)
        return scores


class StackedLSTM(nn.Module):
    def __init__(self, num_layers, input_size, hidden_size, dropout):
        super(StackedLSTM, self).__init__()
        self.dropout = nn.Dropout(dropout)
        self.num_layers = num_layers
        self.layers = nn.ModuleList()

        for i in range(num_layers):
            self.layers.append(nn.LSTMCell(input_size, hidden_size))
            input_size = hidden_size

    def forward(self, input, hidden):
        h_0, c_0 = hidden
        h_1, c_1 = [], []
        for i, layer in enumerate(self.layers):
            h_1_i, c_1_i = layer(input, (h_0[i], c_0[i]))
            input = h_1_i
            if i + 1 != self.num_layers:
                input = self.dropout(input)
            h_1 += [h_1_i]
            c_1 += [c_1_i]

        h_1 = torch.stack(h_1)
        c_1 = torch.stack(c_1)

        return input, (h_1, c_1)


class StackedGRU(nn.Module):
    def __init__(self, num_layers, input_size, hidden_size, dropout):
        super(StackedGRU, self).__init__()
        self.dropout = nn.Dropout(dropout)
        self.num_layers = num_layers
        self.layers = nn.ModuleList()

        for i in range(num_layers):
            self.layers.append(nn.GRUCell(input_size, hidden_size))
            input_size = hidden_size

    def forward(self, input, hidden):
        h_0 = hidden
        h_1 = []
        for i, layer in enumerate(self.layers):
            h_1_i = layer(input, h_0[i])
            input = h_1_i
            if i + 1 != self.num_layers:
                input = self.dropout(input)
            h_1 += [h_1_i]

        h_1 = torch.stack(h_1)

        return input, h_1
