from PIL import Image
import numpy as np

from rc4 import RC4

'''
参数：
key 秘钥 1-256位长度
src 源图片地址
dst 输出加密图片地址
---
该函数只可对单幅图片加密，不限图片大小及通道数
'''
# def picen(key, src, dst):
#     # image = cv2.imread(src)
#     image = np.array(Image.open(src))

#     #对不同通道分开加密，即每个通道加密过程一样
#     for i in range(max(1, int(image.shape[2] / 2))):
#         channel = image[:, :, i]
#         channel_shape = channel.shape
#         #二维数据转化为一维数组进行加密
#         data = np.array(channel).reshape(1, channel_shape[0] * channel_shape[1])[0]
#         encrypter = RC4()
#         encrypter.init(key)
#         image[:, :, i] = np.array(encrypter.start(data, True)).reshape(channel_shape[0],channel_shape[1])

#     Image.fromarray(image).save(dst)

def picen(key, src, dst):
    with open(src, 'rb') as f:
        channel = np.array(list(f.read()), dtype=np.uint8)
        f.close()
        encrypter = RC4()
        encrypter.init(key)
        channel = np.array(encrypter.start(channel))
        with open(dst, 'wb') as wf:
            wf.write(channel)
            wf.close()

if __name__ == "__main__":
    from sys import argv
    if len(argv) < 3:
        print("python PicEncrypt.py picture_path save_path key")

    src = argv[1]
    dst = argv[2]
    key = argv[3]
    picen(key, src, dst)