import torch.nn as nn
import torch

class EffNetb0(nn.Module):
    def __init__(self, output_size=52):
        super(EffNetb0, self).__init__()
        self.model_name = 'effnet'

        # Create model
        torch.hub.list('rwightman/gen-efficientnet-pytorch')
        self.effnet = torch.hub.load('rwightman/gen-efficientnet-pytorch', 'efficientnet_b0', pretrained=False)
        
        self.effnet.conv_stem = nn.Conv2d(1, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
        # Modify last linear layer
        num_ftrs = self.effnet.classifier.in_features
        self.effnet.classifier= nn.Linear(num_ftrs, output_size)
        # print (self.effnet)
        
    def forward(self, x):
        out = self.effnet(x)
        # print(out.shape)
        # [batch, output_size]

        onset_logits = out[:, 0]
        offset_logits = out[:, 1]
        pitch_logits = out[:, 2:]

        return onset_logits, offset_logits, pitch_logits

class EffNet(nn.Module):
    def __init__(self, output_size=52):
        super(EffNet, self).__init__()
        self.model_name = 'effnet'

        # Create model
        torch.hub.list('rwightman/gen-efficientnet-pytorch')
        self.effnet = torch.hub.load('rwightman/gen-efficientnet-pytorch', 'efficientnet_b3', pretrained=False)
        
        self.effnet.conv_stem = nn.Conv2d(1, 40, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
        # Modify last linear layer
        num_ftrs = self.effnet.classifier.in_features
        self.effnet.classifier= nn.Linear(num_ftrs, output_size)
        #print (self.effnet)

    def forward(self, x):
        out = self.effnet(x)
        # print(out.shape)
        # [batch, output_size]

        onset_logits = out[:, 0]
        offset_logits = out[:, 1]
        pitch_logits = out[:, 2:]

        return onset_logits, offset_logits, pitch_logits


if __name__ == '__main__':
    from torchsummary import summary
    model = EffNetb0().cuda()
    summary(model, input_size=(1, 1795, 7))

    model = EffNet().cuda()
    summary(model, input_size=(1, 1795, 7))
