import requests
import os

# 创建一个简单的文本文件（不是PDF，但用于测试）
with open('test.txt', 'w') as f:
    f.write('This is a test file.')

# 准备请求数据
url = 'http://localhost:5000/api/add-watermark'
files = {'pdf': open('test.txt', 'rb')}
data = {'name': '张三', 'studentId': '20240001'}

# 发送请求
print('发送测试请求到API...')
try:
    response = requests.post(url, files=files, data=data)
    print(f'响应状态码: {response.status_code}')
    print(f'响应内容: {response.json()}')
except Exception as e:
    print(f'请求失败: {str(e)}')
finally:
    # 关闭文件
    files['pdf'].close()
    # 删除测试文件
    if os.path.exists('test.txt'):
        os.remove('test.txt')