import cv2
path="D:\mindx_hack\static\css/Register.jpg"
img = cv2.imread(path)
print(img)
img = cv2.resize(img,(1500,800))
cv2.imwrite(img,"out_1.png")