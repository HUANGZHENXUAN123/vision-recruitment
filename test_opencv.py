import cv2

image = cv2.imread("test.jpg")

if image is None:
    print("图片读取失败，请检查路径")
else:
    print("图片读取成功")
    print("图片尺寸:", image.shape)
    print("OpenCV 版本:", cv2.__version__)

