# img2md
将文档的扫描件（图片），转换成markdown格式。

我还画蛇添足追加了翻译功能。

 - 使用Google Cloud Vision API进行OCR，获得非常好的OCR效果。
 - 而后利用Google Gemini 对OCR的结果进行重新排版，获得最佳的markdown输出。
 - 如果要顺便翻译一下的话，翻译功能也是由Google Gemini提供的

 **上述服务都通过Google Cloud获取，请准备Google Cloud的[认证JSON](https://cloud.google.com/iam/docs/service-accounts-create?hl=zh-CN)**

虽然只是重新组合了轮子，但使用此工具获得的输出结果超越了我之前尝试的多个不同的工具。

并且，对能够很好的对应日语、中文等非英语场景。感谢Google感谢CCTV。

如果你手头有一个PDF文件，想要将PDF文件完美转换成markdown的话，你可以使用我重新发明的另一个轮子：
[convert2img](https://github.com/wengzhiwen/convert2img)，快速将PDF变成可以喂给img2md的图片序列。

针对文字密集的文档，建议使用较高分辨率（**比如300dpi**）的图片

## 使用说明

1. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

2. 设置GOOGLE_APPLICATION_CREDENTIALS
    ```bash
    cp .env.sample .env
    ```
    使用你熟悉的编辑器在.env文件中设置你自己的认证JSON的路径（建议使用绝对路径，方便你在任何地方使用）

3. 运行转换命令：
    ```bash
    python img2md.py <img_folder>
    ```
    或者顺便翻译一下
    ```bash
    python img2md.py <img_folder> [--trans_to 中文]
    ```
    --trans_to的参数可以使用自然语言（“中文、英语、日语、English”），因为他会是翻译后的文本的文件名的一部分，请不要自己注入攻击自己。

程序会按照文件名顺序，一一处理每一个图片文件，并把结果存到同一个markdown文件中。
生成的markdown文件和你**输入的文件夹同名**，偷懒偷到烂。


# English

Convert scanned document images to markdown format. With AI powered, you will get the bast output ever.

And now we support **Translate** function also.

- Use **Google Cloud Vision API** for OCR to achieve excellent recognition results.  
- Use **Google Gemini AI** to reformat the OCR output for the best Markdown results.
- Use **Google Gemini AI** for Translate

**See [docs from google](https://cloud.google.com/iam/docs/service-accounts-create) to create JSON file for Google Cloud Auth.**

It also handles **Japanese, Chinese, and other non-English languages** extremely well.  

If you have a PDF-file that you want to convert perfectly into Markdown, seee another tool of mine:  
[**convert2img**](https://github.com/wengzhiwen/convert2img), which quickly turns PDF-file into a sequence of images that can be fed into **img2md**.

> **Note:** For text-heavy documents, it’s recommended to use higher-resolution images (e.g. **300 dpi**).

---

## Instructions

1. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Set GOOGLE_APPLICATION_CREDENTIALS**:
    ```bash
    cp .env.sample .env
    ```
    Use your preferred text editor to set your own JSON file for Google Cloud Auth in the **.env** file.

3. **Run the conversion command**:
    ```bash
    python img2md.py <img_folder>
    ```
    Or do Translate in the sametime
    ```bash
    python img2md.py <img_folder> [--trans_to English]
    ```
    Just use human langlage for '--trans_to' argument. e.g. '中文', '日本語', 'English'

The program processes each image file in alphabetical order and saves the output to a single Markdown file.  
The generated Markdown file has the **same name** as input folder name.


