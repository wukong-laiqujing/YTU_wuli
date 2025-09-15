import os
import os
import requests

# 准备请求数据
url = 'http://localhost:5000/api/add-watermark'
data = {'name': '测试用户', 'studentId': '20240001'}

# 发送请求
print('发送测试请求到API...')
try:
    # 直接发送表单数据
    response = requests.post(url, data=data)
    print(f'响应状态码: {response.status_code}')
    
    if response.status_code == 200:
        # 保存响应文件
        with open('watermarked_test_pdf.pdf', 'wb') as f:
            f.write(response.content)
        print('成功: 已生成带水印的PDF文件: watermarked_test_pdf.pdf')
    else:
        try:
            print(f'响应内容: {response.json()}')
        except:
            print(f'响应内容: {response.text}')
except Exception as e:
    print(f'请求失败: {str(e)}')