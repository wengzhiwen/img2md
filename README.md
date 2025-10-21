# img2md
将文档的扫描件（图片），转换成markdown格式。
当前版本只聚焦OCR识别与Markdown排版，不再内置翻译功能。

 - 使用Google Cloud Vision API进行OCR，获得非常好的OCR效果。
 - 而后利用Google Gemini 对OCR的结果进行重新排版，获得最佳的markdown输出。

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

程序会按照文件名顺序，一一处理每一个图片文件，并把结果存到同一个markdown文件中。
生成的markdown文件和你**输入的文件夹同名**，偷懒偷到烂。

## 关于汉字文档的OCR ##

不论日语还是中文，虽然没有测试过，但我相信韩文也有一样的问题：并没有什么特别好的OCR解决方案。
而各个国家都有一些“民族企业”，研发和运营一些具有针对性的OCR软件，我试用过其中一些，很抱歉的讲并没有获得什么特别好的使用体验。

为了能够扫描我手头的百来个日语的PDF，我尝试了各种奇奇怪怪的解决方案，也包括了Github上一些开源的解决方案。我觉得最接近的答案是部分解决方案至少能很好的处理英语（也许也能包括整个拉丁语系）文档，但对于汉字文档并没有什么特别好的办法。

于是，抱着花小钱办大事的思路，我尝试了包括OpenAI在内的各种我（截止到现在时刻）能接触到的多模态大模型的解决方案，最终选择了Google Cloud中相当具有专业性的Vision API。

我调试整个整个程序（大约花了一整天的时间反复在调用Vision API）外加OCR大约100页日语PDF文档，花费的金额是66日元（大约3人民币）。并且，因为我是新开的Google Cloud账户，这些点数还是Google赠送的，花不完～完全花不完～～

当然我也没有忘记免费的解决方案：我保留了一个脚本（img2md_ollama.py），用于调用兼容 OpenAI 接口的本地多模态模型，只需在命令行或环境变量中指定 `--api-url`、`--model` 等参数即可接入你的私有部署服务。


# English

Convert scanned document images to markdown format. With AI powered, you will get the bast output ever.
The tool now focuses purely on OCR and Markdown formatting without bundled translation.

- Use **Google Cloud Vision API** for OCR to achieve excellent recognition results.  
- Use **Google Gemini AI** to reformat the OCR output for the best Markdown results.

**See [docs from google](https://cloud.google.com/iam/docs/service-accounts-create) to create JSON file for Google Cloud Auth.**

It also handles **Japanese, Chinese, and other non-English languages** extremely well. If you prefer local inference, the helper script `img2md_ollama.py` now targets any **OpenAI-compatible** multimodal endpoint—just provide your own `--api-url` or environment variables.

If you have a PDF-file that you want to convert perfectly into Markdown, see another tool of mine:  
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

The program processes each image file in alphabetical order and saves the output to a single Markdown file.  
The generated Markdown file has the **same name** as input folder name.
