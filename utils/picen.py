from utils.rc4 import RC4
import numpy as np

# def picen(key, src, dst):
#     from PIL import Image
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


# def picen(key, src, dst):
#     with open(src, 'rb') as f:
#         channel = np.array(list(f.read()), dtype=np.uint8)
#         f.close()
#         encrypter = RC4()
#         encrypter.init(key)
#         channel = np.array(encrypter.start(channel))
#         with open(dst, 'wb') as wf:
#             wf.write(channel)
#             wf.close()


def picen(key, src):
    channel = np.array(list(src), dtype=np.uint8)
    encrypter = RC4()
    encrypter.init(key)
    channel = np.array(encrypter.start(channel))

    return channel.tobytes()