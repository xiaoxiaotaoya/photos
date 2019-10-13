# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError


import os
import sys
import logging

# 腾讯云COSV5Python SDK, 目前可以支持Python2.6与Python2.7以及Python3.x
# pip安装指南:pip install -U cos-python-sdk-v5
# cos最新可用地域,参照https://www.qcloud.com/document/product/436/6224

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 设置用户属性, 包括secret_id, secret_key, region
# appid已在配置中移除,请在参数Bucket中带上appid。Bucket由bucketname-appid组成
secret_id = '###'     # 替换为用户的secret_id
secret_key = '###'     # 替换为用户的secret_key
region = 'ap-chengdu'    # 替换为用户的region
token = None               # 使用临时密钥需要传入Token，默认为空,可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  # 获取配置对象
client = CosS3Client(config)

#确定文件夹
list_dir = ['WLOP', '哈利波特','尼尔机械纪元']
img_dir, min_dir = "photos/", "min_photos/"

response = client.get_bucket_location(
    Bucket='hexo-1257031621'
)
print(response)


# 删除文件夹及其文件
def delete_dir(dir):
    response = client.list_objects(
        Bucket='hexo-1257031621',
        Prefix=dir,
    )
    Contents = response['Contents']
    print("正在删除{}文件夹".format(dir))
    for i in range(len(Contents)):
        keys = Contents[i]['Key']
        response = client.delete_object(
            Bucket='hexo-1257031621',
            Key=keys,
        )
    print("删除完成")


# 查询photos和min_photos文件夹是否存在，存在则删除，防止文件冗余
def inquire_dir():
    response = client.list_objects(
        Bucket='hexo-1257031621',
        Delimiter='/',
    )
    CommonPrefixes = response['CommonPrefixes']
    for i in range(len(CommonPrefixes)):
        Prefixes = CommonPrefixes[i]['Prefix']
        if (Prefixes == "photos/"):
            delete_dir("photos")
        elif (Prefixes == "min_photos/"):
            delete_dir("min_photos")


#上传文件夹
def img_upload(dir):
    for img_dir in list_dir:
        img_files = os.listdir(dir + img_dir)
        for i in range(len(img_files)):
            img_file = dir + img_dir + "/" + img_files[i]
            response = client.upload_file(
                Bucket='hexo-1257031621',
                Key=img_file,
                LocalFilePath=img_file,
                EnableMD5=False
            )
    print("上传{}文件夹完成".format(dir))

def upload():
    inquire_dir()
    img_upload(img_dir)  # 上传photos文件夹
    img_upload(min_dir)  # 上传min_photos文件夹
    print("上传完成")


# 生成datas.json数据文件
def data_json():
    if os.path.exists("data/datas.json"):
        os.remove("data/datas.json")
    for name in list_dir:
        data_name = "data/" + name + "_data.json"
        with open(data_name, 'w', encoding='utf-8') as file:
            data_head1 = '<div id="container">\n<div id="' + name + '"><center><strong><font size="4" color="#228B22">' + name + '</font></strong></center></div>\n'
            data_head2 = '<ul id="grid" class="group">\n'
            data_head = data_head1 + data_head2
            data_end = '</ul></div><div style="text-align:center;clear:both"></div>\n'
            file.write(data_head)
            response = client.list_objects(
                Bucket='hexo-1257031621',
                Prefix=min_dir + name,
            )
            Contents = response['Contents']
            for index in range(len(Contents)):
                urls = 'https://hexo-1257031621.cos.ap-chengdu.myqcloud.com/' + Contents[index]['Key']
                img_name = Contents[index]['Key'].replace("min_photos/", "").split(".")[0]
                data0 = '<li><div class="details"><h3>' + img_name.replace("/", " ") + '</h3></div>'
                data1 = '<a href="' + urls.replace("min_photos/","photos/") + '"><img  src="' + urls + ' "hight="180px" width="180px"></a></li>'
                data = data0 + data1
                file.write(data)
                file.write("\n")
            file.write(data_end)
        with open(data_name, 'r', encoding='utf-8') as file:
            content = file.read()
        with open("data/datas.json", 'a', encoding='utf-8') as file:
            file.write(content)
        os.remove(data_name)
    print("生成datas.json数据文件")


# 生成hrefs.json数据文件
def hrefs_json():
    with open("data/hrefs.json", 'w', encoding='utf-8') as file:
        data_href_head = '<center>['
        data_href_end = ']</center>'
        file.write(data_href_head)
        for name in list_dir:
            data_href = '<a href="#' + name + '">&emsp;' + name + '&emsp;</a>'
            file.write(data_href)
        file.write(data_href_end)
    print("生成hrefs.json数据文件")


# 写入数据到themes/yilia/layout/photos.ejs文件中
def data_write():
    hrefs_json()
    data_json()
    with open("D:/hexo-blog/themes/yilia/layout/photos.ejs", 'r', encoding='utf-8') as file:
        content = file.read()
        pos0 = content.find('<center>')
        with open("data/hrefs.json", 'r', encoding='utf-8') as file:
            content_hrefs = file.read()
        with open("data/datas.json", 'r', encoding='utf-8') as file:
            content_data = file.read()
        data = content[:pos0] + content_hrefs + '\n</header>\n</br>\n</br>\n' + content_data
        with open("D:/hexo-blog/themes/yilia/layout/photos.ejs", 'w', encoding='utf-8') as file:
            file.write(data)
    print("数据写入完毕")


if __name__ == "__main__":
    upload() # 文件上传
    data_write() #数据写入















































