import m_dlib.face_marks as fmarks
from PIL import Image

colour_dict = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "blue": (67, 142, 219)
}

def crop_photo(path, target, size_width, size_height, cl, size3, scale_ratio):
    # 获取人脸框
    shape, d = fmarks.predictor_face(path)
    
    face_width = d.right() - d.left()
    face_height = d.bottom() - d.top()
    
    # 获取目标证件照的宽高比
    target_ratio = size_width/size_height

    # 动态计算裁剪区域的宽高
    # 保持目标证件照的宽高比
    if face_width / face_height > target_ratio:
        # 如果人脸宽度占比大于目标宽高比，调整宽度
        crop_height = face_height * scale_ratio
        crop_width = crop_height * target_ratio
    else:
        # 如果人脸高度占比大于目标宽高比，调整高度
        crop_width = face_width * scale_ratio
        crop_height = crop_width / target_ratio
    
    # 计算人脸中心
    X_CENTRE = d.left() + face_width / 2
    Y_CENTER = d.top() + face_height / 2

    im = Image.open(path)

    # 裁剪图像（保证不会越界）
    left = max(0, int(X_CENTRE - crop_width / 2))
    upper = max(0, int(Y_CENTER - crop_height / 2))
    right = int(X_CENTRE + crop_width / 2)
    lower = int(Y_CENTER + crop_height / 2)

    im = im.crop((left, upper, right, lower))

    # 裁剪图像
    # im = im.crop((X_CENTRE - crop_width / 2, Y_CENTER - crop_height / 2,
    #               X_CENTRE + crop_width / 2, Y_CENTER + crop_height / 2))

    # 为裁剪图像添加背景
    p = Image.new('RGB', (im.size[0], size3), colour_dict[cl])
    im.paste(p, (0, 0))

    im = im.resize((size_width, size_height))

    # 保存裁剪后的图像
    im.save(target)

# def crop_photo(path, target,size_width,size_height,cl,size3):
#     path = path
#     shape, d = fmarks.predictor_face(path)

#     # WIDTH_2IN = 413
#     # HEIGHT_2IN = 626

#     WIDTH_2IN = size_width/2
#     HEIGHT_2IN = size_height/2

#     # 人像中心点
#     X_CENTRE = d.left()+(d.right()-d.left()) / 2
#     Y_CENTER = d.top()+(d.bottom()-d.top()) / 2

#     im = Image.open(path)
#     # i=im.size[0]
#     # j=im.size[1]
#     # print("图像的高")
#     # print(j)

#     im = im.crop((X_CENTRE-WIDTH_2IN, Y_CENTER-HEIGHT_2IN, X_CENTRE+WIDTH_2IN, Y_CENTER+HEIGHT_2IN))
#     # print(Y_CENTER-HEIGHT_2IN)
#     # print(Y_CENTER+HEIGHT_2IN)
#     # print(j-int((Y_CENTER+HEIGHT_2IN-(Y_CENTER-HEIGHT_2IN))/2))

#     #im.save(target)

#     p = Image.new('RGB',(im.size[0],size3), colour_dict[cl])
#     #p.save("p.png")
#     im.paste(p, (0, 0))
#     im.save(target)


# 通过识别人脸关键点，裁剪图像
# crop_photo("..//img//meinv_id.png","..//img//2in.jpg")
