# -*- coding: UTF-8 -*-

from urllib.parse import urljoin
from qiniu import Auth, put_file, etag

# 空间名称与空间网址的对应字典
space2url ={
    "xinhaitui":"http://qp2bm1bf4.hn-bkt.clouddn.com"
}

def up2qiniu(local_img,space_name,img_name):
    """
    本图图片的上传
    :param local_img: 本地图片路径
    :param space_name: 云服务器的空间名称
    :param img_name: 上传后的网络上保存的图片名称
    :return img_url: 远程图片的路径(绝对路径)
    """
    access_key = '9NOdpqP-j_RWKsmDyJ9UGau08sFDfpSbULVnCT6F'
    secret_key = 'x-h8gpjwWIRbzk_dqzO3tk3GOy1yQAGw-UK6OUEm'
    q = Auth(access_key, secret_key)# 构建鉴权对象
    bucket_name = space_name# 要上传的空间
    key = img_name# 上传后保存的文件名
    token = q.upload_token(bucket_name, key, 3600)# 生成上传 Token，可以指定过期时间等
    localfile = local_img# 要上传文件的本地路径
    ret, info = put_file(token, key, localfile)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)
    # img_url = 空间名称 拼接 远程图片名称
    # img_url = urljoin("http://q57wyk04l.bkt.clouddn.com", img_name)
    img_url = urljoin(space2url[space_name], img_name)
    return img_url
res = up2qiniu("C:/Users/18003/Pictures/2.jpg", "xinhaitui","2111.jpg")
print(res)


