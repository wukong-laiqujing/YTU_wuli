import requests
import os
from datetime import datetime

# 设置API端点
url = 'http://localhost:5000/api/add-watermark'

# 要测试的中文名字和学号
chinese_name = '张三'
student_id = '20230001'

# 上传文件
files = {'pdf': open('test_pdf.pdf', 'rb')}

# 表单数据
data = {'name': chinese_name, 'studentId': student_id}

try:
    # 发送POST请求
    print(f'正在发送请求，测试中文水印: {chinese_name} | {student_id}')
    response = requests.post(url, files=files, data=data)
    
    # 检查响应状态
    if response.status_code == 200:
        # 保存响应内容为PDF文件，使用唯一文件名避免冲突
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        output_filename = f'watermarked_chinese_test_{timestamp}.pdf'
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        
        print(f'响应状态码: {response.status_code}')
        print(f'成功: 已生成带中文水印的PDF文件并保存为 {output_filename}')
        print(f'请打开文件检查中文水印 "{chinese_name} | {student_id}" 是否以宋体正确显示')
    else:
        print(f'请求失败: 状态码 {response.status_code}')
        try:
            # 尝试获取错误信息
            print(f'错误信息: {response.json()}')
        except:
            print(f'无法解析错误响应')
finally:
    # 关闭文件
    files['pdf'].close()