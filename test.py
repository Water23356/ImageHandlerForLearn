import cv2

image_path = r"D:\Codes\Python\ImageHandler\sample\jpg-12.jpg"
image = cv2.imread(image_path)

if image is None:
    print("图像加载失败，请检查路径或文件完整性！")
else:
    # 如果图像加载成功，继续后续操作
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 其他处理...