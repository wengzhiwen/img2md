# img2md

把图片里的文字转换成markdown格式。

## 功能

- 使用OpenAI兼容接口的多模态模型做OCR识别
- 保持原始格式结构，包括表格、标题等

## 使用

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 配置环境变量（创建.env文件）：
   ```
   BASE_URL=你的API地址
   MODEL_FOR_OCR=模型名称
   API_KEY_FOR_OCR=API密钥（可选）
   TIMEOUT_FOR_OCR=120
   ```

3. 运行：
   ```bash
   python img2md.py <图片文件夹路径>
   ```

程序会按文件名顺序处理图片，生成带时间戳的markdown文件。

## 注意事项

- 需要支持多模态的OpenAI兼容接口
- 文字密集的文档建议用300dpi分辨率
- 如果有PDF需要转换，可以用[convert2img](https://github.com/wengzhiwen/convert2img)先转成图片

## 测试记录

### qwen/qwen2.5-vl-7b

识别日语文档，会有神出鬼没的幻觉，非常的不安全。而且是那种单靠语法检查很难察觉的幻觉，非常的危险。
