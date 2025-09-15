# PDF水印添加工具

一个基于Vue 3和Flask的PDF水印添加工具，可以在PDF的每一页插入姓名和学号水印，并支持下载处理后的文件。

## 功能特点

- 📄 上传PDF文件并添加个性化水印
- 🔤 支持自定义姓名和学号
- 🎨 水印以45度角均匀分布在每页
- 💾 自动下载处理后的PDF文件
- 📱 响应式设计，适配各种设备
- 🔐 本地处理，保障文件安全

## 技术栈

**前端：**
- Vue 3
- Vite
- Axios

**后端：**
- Python
- Flask
- PyPDF2
- reportlab

## 快速开始

### 1. 安装依赖

**前端依赖：**
```bash
npm install
```

**后端依赖：**
```bash
pip install -r requirements.txt
```

### 2. 启动服务

**启动后端服务：**
```bash
python server.py
```

服务将运行在 http://localhost:5000

**启动前端开发服务器：**
```bash
npm run dev
```

服务将运行在 http://localhost:5173

### 3. 使用方法

1. 打开浏览器，访问 http://localhost:5173
2. 在页面上输入您的姓名和学号
3. 点击"选择PDF文件"按钮，上传您要添加水印的PDF文件
4. 点击"添加水印并下载"按钮
5. 系统将自动处理文件并下载带有水印的PDF文件

## 测试文件

项目包含一个测试PDF文件 `test_pdf.pdf`，您可以直接使用它来测试功能。

## 项目结构

```
vue3/
├── src/           # 前端源代码
│   ├── App.vue    # 主组件
│   ├── main.js    # 入口文件
│   └── assets/    # 静态资源
├── server.py      # Flask后端服务
├── requirements.txt # Python依赖
└── package.json   # npm依赖配置
```

## 注意事项

- 请确保上传的文件是有效的PDF格式
- 较大的PDF文件可能需要更长的处理时间
- 程序会在处理完成后自动清理临时文件

## License

MIT
