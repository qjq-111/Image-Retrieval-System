from django.shortcuts import render
from PIL import Image
import torch
from torchvision import transforms
import os
from . import net
from . import models
import numpy as np
from django.utils import timezone


# Create your views here.
def search(request):
    if request.method == "POST":
        upload_time = timezone.now()
        img = request.FILES.get('uploadImage')
        img_name = img.name
        base_path = os.path.dirname(__file__).replace('\\', '/')
        path = base_path + '/static/ImageSearch/image/upload' + '/' + img_name
        img_path = 'ImageSearch/image/upload/' + img_name

        with open(path, 'wb') as f:
            f.write(img.read())
        top5_img_path, hash_code = top_5_imgs(base_path, path)
        describe = [file.split('/')[-2] for file in top5_img_path]
        # 写入数据库
        new_upload_img = models.Image()
        new_upload_img.img_url = img_path
        new_upload_img.hash_code = hash_code
        new_upload_img.upload_date = upload_time
        new_upload_img.save()

        top5_img = zip(top5_img_path, describe)
        return render(request, 'ImageSearch/result.html', {'img_path': img_path, 'top5_img': top5_img})
        # return render(request, 'ImageSearch/result.html',
        #               {'img_path': img_path, 'top5_img_path': top5_img_path, 'describe': describe})
    else:
        return render(request, 'ImageSearch/search.html')


# 返回与上传图片哈希码，以及最近似的5张图片
def top_5_imgs(base_path, img_path):
    img_list_path = base_path + '/static/ImageSearch/image_list.txt'
    hash_codes_path = base_path + '/static/ImageSearch/hash_code.npy'
    cnn_net = net.Net(48)
    net_path = base_path + '/static/ImageSearch/net.pth'
    cnn_net.load_state_dict(torch.load(net_path, map_location=lambda storage, location: storage))
    cnn_net.eval()

    # 读取检索数据库图片的哈希码
    database_codes = np.load(hash_codes_path)
    # 读取所有图片的地址
    with open(img_list_path, 'r') as f:
        img_list = ['ImageSearch/image/' +line[:-1] for line in f]

    img = Image.open(img_path)
    img = img.convert('RGB')
    transformations = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = transformations(img)
    img = img.unsqueeze(0)
    hash_code = torch.sign(cnn_net(img).data)
    database_codes = torch.from_numpy(database_codes).float()

    # 计算海明距离
    hamm = 0.5 * (48 - hash_code.mm(database_codes.transpose(0, 1)))
    # 取海明距离最小的前五张图片
    _, sorted_index = torch.topk(hamm, k=5, largest=False, dim=1)
    sorted_index = sorted_index.squeeze().numpy()
    top5_img_path = [img_list[i] for i in sorted_index]
    hash_code = hash_code.squeeze().numpy().astype(np.int32)
    return top5_img_path, B_to_Str(hash_code)


# 把二值化的哈希码(numpy)转化为字符串
def B_to_Str(hash_code):
    s = ''.join(str(i) for i in hash_code)
    return s


# def result(request):
#     return render(request, 'ImageSearch/result.html')




