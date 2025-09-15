from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# 创建一个简单的PDF测试文件
c = canvas.Canvas('test_pdf.pdf', pagesize=letter)

# 添加标题
c.setFont("Helvetica-Bold", 24)
c.drawString(100, 750, "PDF水印测试文件")

# 添加正文
c.setFont("Helvetica", 12)
c.drawString(100, 700, "这是一个用于测试PDF水印功能的示例文件。")
c.drawString(100, 680, "您可以使用此文件测试添加姓名和学号水印的功能。")
c.drawString(100, 660, "添加水印后，每一页都会显示您的姓名和学号。")

# 添加页脚
c.setFont("Helvetica-Oblique", 10)
c.drawString(100, 50, "PDF水印测试文件 - 示例内容")

# 保存文件
c.save()

print("测试PDF文件已创建: test_pdf.pdf")