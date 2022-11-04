import urllib.request
import urllib.parse
import json
import re
import csv

# 1.指定url
url = 'http://www.lamost.org/publications/bars/barGetPaperInfo.php'

# 发起POST请求之前，要处理POST请求携带的参数 流程:
# 一、将POST请求封装到字典
data = {
    # 将POST请求所有携带参数放到字典中
    "page": "1",
    "limit": "1000",
    "year": "all"
}

# 二、使用parse模块中的urlencode(返回值类型是字符串类型)进行编码处理
data = urllib.parse.urlencode(data)
# print(data)   # page=1&limit=1000&year=all
# 三、将步骤二的编码结果转换成byte类型
data = data.encode()
# print(data)


'''2. 发起POST请求:urlopen函数的data参数表示的就是经过处理之后的
POST请求携带的参数
'''
# url = urllib.request.quote(url, ':/=&?')
response = urllib.request.urlopen(url=url, data=data)
data = response.read()
# print(data)
data = json.loads(data)  # 转换成字典
lst = data['data']
# print(lst)
n = 1  # 测试

with open("lamostpapers.csv", 'a', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    # 先写入columns_name
    writer.writerow(["no", "title", "authors", "download_link", "journal", "updatetime", "year", "status"])
    for item in lst:
        if item['link'] == '':  # 有没有提供下载按钮的
            continue
        #  print(item['title'])
        file_url = "http://www.lamost.org" + item['link']
        # 写入多行用writerows
        writer.writerows([[n, item['title'], item['author'], file_url, item['journal'], item['updatetime'], item['year'], item['status']]])
        # file_url = file_url.replace(" ", "%20")
        # # 把空格换成%20，原因（三篇文章）：
        # # https://blog.csdn.net/qq_30242609/article/details/62896170
        # # https://blog.csdn.net/qq_24601279/article/details/104210993
        # # https://cloud.tencent.com/developer/article/1074824
        #
        # print(n, file_url)
        n += 1  # 测试
        # res = urllib.request.urlopen(url=file_url)
        # file_data = res.read()  # 读pdf
        # merge_title = title + ".pdf"  # 合并命名
        # final_title = re.sub(r'[\\/:*?"<>|]', '', merge_title)  # 利用re模块实现pdf规范命名

        # with open(final_title, 'wb') as f:
        #     f.write(file_data)  # 写入字节数据
