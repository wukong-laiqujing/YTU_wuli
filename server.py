from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 确保临时文件夹存在
TEMP_DIR = 'temp'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.route('/api/add-watermark', methods=['POST'])
def add_watermark():
    try:
        # 获取表单数据
        name = request.form.get('name', '')
        student_id = request.form.get('studentId', '')
        
        # 验证必填字段
        if not name or not student_id:
            return jsonify({'success': False, 'message': '姓名和学号不能为空'}), 400
        
        # 设置使用根目录下的实验报告纸.pdf
        input_filename = '实验报告纸.pdf'
        
        # 验证文件是否存在
        if not os.path.exists(input_filename):
            return jsonify({'success': False, 'message': '实验报告纸.pdf文件不存在'}), 500
        
        # 验证文件是有效的PDF
        try:
            with open(input_filename, 'rb') as f:
                pdf_header = f.read(4)
                if pdf_header != b'%PDF':
                    return jsonify({'success': False, 'message': '实验报告纸.pdf不是有效的PDF文件'}), 500
        except Exception as e:
            return jsonify({'success': False, 'message': f'验证文件时出错: {str(e)}'}), 500
        
        # 生成唯一的输出文件名
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = uuid.uuid4().hex[:6]
        output_filename = os.path.join(TEMP_DIR, f'output_{timestamp}_{random_str}.pdf')
        
        # 创建水印
        watermark_text = f'{name} | {student_id}'
        
        # 添加水印到PDF文件
        try:
            add_watermark_to_pdf(input_filename, output_filename, watermark_text)
        except Exception as e:
            # 清理临时文件
            if os.path.exists(output_filename):
                os.remove(output_filename)
            raise e
        
        # 修复文件下载和清理逻辑
        # 读取文件内容到内存，然后发送
        try:
            with open(output_filename, 'rb') as f:
                file_data = f.read()
                
            # 设置下载文件名
            download_name = f'实验报告纸_{name}_{student_id}_{timestamp}_已添加水印.pdf'
            
            # 发送文件数据
            response = send_file(
                io.BytesIO(file_data),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=download_name
            )
            
            # 注意：不删除实验报告纸.pdf文件
            
            # 对于Windows，使用延迟删除策略
            def delayed_delete():
                import threading
                import time
                
                def delete_file():
                    time.sleep(2)  # 等待2秒后再尝试删除
                    try:
                        if os.path.exists(output_filename):
                            os.remove(output_filename)
                    except Exception as e:
                        print(f'警告: 无法删除临时文件 {output_filename}: {str(e)}')
                        
                # 启动后台线程执行延迟删除
                thread = threading.Thread(target=delete_file)
                thread.daemon = True
                thread.start()
            
            # 启动延迟删除
            delayed_delete()
            
            return response
            
        except Exception as e:
              # 注意：不删除实验报告纸.pdf文件
              if os.path.exists(output_filename):
                  try:
                      os.remove(output_filename)
                  except:
                      pass
              raise e
        
    except Exception as e:
        print(f'错误详情: {str(e)}')
        import traceback
        print(f'错误栈: {traceback.format_exc()}')
        return jsonify({'success': False, 'message': f'处理文件时发生错误: {str(e)}'}), 500

def add_watermark_to_pdf(input_pdf_path, output_pdf_path, watermark_text):
    # 创建一个PDF读取器
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    # 为每一页创建水印
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        
        # 创建一个PDF文件来保存水印
        packet = io.BytesIO()
        
        # 使用页面实际大小创建canvas
        page_width, page_height = page.mediabox.width, page.mediabox.height
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        # 尝试使用Windows系统中常见的中文字体
        # 简化字体设置，使用更直接的方法确保中文显示
        fonts_to_try = [
            ("C:/Windows/Fonts/simsun.ttc", "SimSun"),  # 宋体
            ("C:/Windows/Fonts/simhei.ttf", "SimHei"),  # 黑体
            ("C:/Windows/Fonts/msyh.ttc", "Microsoft YaHei")  # 微软雅黑
        ]
        
        font_set = False
        # 尝试加载中文字体
        for font_path, font_name in fonts_to_try:
            try:
                # 直接注册并使用字体
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                c.setFont(font_name, 36)
                font_set = True
                print(f"成功加载字体: {font_name}")
                break
            except Exception as e:
                print(f"无法加载字体 {font_name}: {str(e)}")
                continue
        
        # 如果无法加载中文字体，尝试使用reportlab默认支持的字体
        if not font_set:
            try:
                c.setFont("Helvetica", 36)
                print("警告: 无法加载中文字体，使用默认字体")
            except:
                print("严重警告: 无法设置任何字体")
        
        c.setFillColorRGB(0, 0, 0, 0.1)  # 半透明黑色
        
        # 水印设置
        font_size = 36
        angle = 45  # 旋转角度
        
        # 计算水印的实际宽度（使用reportlab的stringWidth函数获得更精确的宽度）
        text_width = pdfmetrics.stringWidth(watermark_text, font_name if font_set else "Helvetica", font_size)
        
        # 考虑旋转45度后，水印的实际占用空间会变大
        # 计算旋转后的文本占用宽度
        import math
        rotated_width = text_width * math.cos(math.radians(angle)) + font_size * math.sin(math.radians(angle))
        
        # 调整水印间距，确保水印不会太密集
        # 基于旋转后的文本宽度和页面大小计算合适的间距
        horizontal_spacing = max(280, rotated_width * 1.6)
        vertical_spacing = max(280, rotated_width * 1.4)
        
        # 在页面上添加水印网格
        # 将Decimal类型转换为float类型以进行计算
        page_width_float = float(page_width)
        page_height_float = float(page_height)
        
        # 计算需要多少行和列的水印
        cols = int(page_width_float / horizontal_spacing) + 2
        rows = int(page_height_float / vertical_spacing) + 2
        
        # 计算页面中心点
        center_x = page_width_float / 2
        center_y = page_height_float / 2
        
        # 首先计算基础起始位置
        base_start_x = (page_width_float - (cols - 1) * horizontal_spacing) / 2
        base_start_y = (page_height_float - (rows - 1) * vertical_spacing) / 2
        
        # 计算网格中心点
        grid_center_x = base_start_x + ((cols - 1) * horizontal_spacing) / 2
        grid_center_y = base_start_y + ((rows - 1) * vertical_spacing) / 2
        
        # 计算偏移量，使网格中心与页面中心对齐
        offset_x = center_x - grid_center_x
        offset_y = center_y - grid_center_y
        
        # 调整起始位置
        start_x = base_start_x + offset_x
        start_y = base_start_y + offset_y
        
        # 逐行逐列添加水印
        for i in range(cols):
            for j in range(rows):
                c.saveState()
                
                # 计算水印位置
                x = start_x + i * horizontal_spacing
                y = start_y + j * vertical_spacing
                
                # 移动到水印位置并旋转
                c.translate(x, y)
                c.rotate(angle)
                
                # 计算文本宽度和高度，确保文本居中对齐
                text_width = pdfmetrics.stringWidth(watermark_text, font_name if font_set else "Helvetica", font_size)
                text_height = font_size
                
                # 计算文本居中的偏移量
                text_x_offset = -text_width / 2
                text_y_offset = -text_height / 4  # PDF文本的基线在底部，所以只需要向上偏移高度的一部分
                
                # 绘制水印文本（居中显示）
                c.drawString(text_x_offset, text_y_offset, watermark_text)
                
                c.restoreState()
        
        c.save()
        
        # 移动到开始处并读取水印PDF
        packet.seek(0)
        watermark_pdf = PdfReader(packet)
        watermark_page = watermark_pdf.pages[0]
        
        # 合并页面和水印
        page.merge_page(watermark_page)
        writer.add_page(page)
    
    # 写入输出文件
    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)

if __name__ == '__main__':
    print('启动Flask服务器，运行在 http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)