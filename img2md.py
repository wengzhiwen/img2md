import glob
import os
import sys
import argparse
import time
from dotenv import load_dotenv
from google.cloud import vision
from google.auth.transport.requests import Request
import google.generativeai as genai
from PIL import Image

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GOOGLE_CLOUD_API_KEY = os.getenv('GOOGLE_CLOUD_API_KEY')

def format_to_markdown_ref_image(text_content, image_path):
    genai.configure(api_key=GEMINI_API_KEY)
    GEMINI_MODEL = os.getenv('GEMINI_MODEL_FOR_FORMAT_MD', 'gemini-1.5-flash')
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
    except Exception as e:
        print(f"加载 Gemini 模型时发生错误: {e}")
        return None
    
    try:
        img = Image.open(image_path)
        contents = [
            "请参考以下图片的内容，将我提供的文本重新组织成 Markdown 格式。",
            img,
            f"文本内容：\n\n{text_content}",
            "请注意保持文本的含义，并根据图片内容调整格式和排版风格，例如：图片中有列表，你可以考虑将文本中的相关部分也组织成列表。",
            "如果文本中包含标题、段落等结构信息，请尽量在 Markdown 中保留。",
            "请输出完整的 Markdown 格式文本。"
        ]

        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        print(f"重新排版时发生错误: {e}")
        return None

def ocr_by_google_cloud(image_path):
    """Performs document text detection on the image file using API Key."""
    client_options = {'api_key': GOOGLE_CLOUD_API_KEY}
    client = vision.ImageAnnotatorClient(client_options=client_options)

    try:
        with open(image_path, 'rb') as image_path:
            content = image_path.read()
    except Exception as e:
        print(f"读取图片文件时发生错误: {e}")
        return None

    try:
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
    except Exception as e:
        print(f"调用 Google Cloud API 时发生错误: {e}")
        return None

    if response.error.message:
        raise Exception(
            'Google Cloud API 错误: {}'.format(
                response.error.message
            )
        )
    else:
        return response.full_text_annotation.text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert images(PNG or JPG) to ONE markdown file.')
    parser.add_argument('img_folder', help='Folder for images.')
    args = parser.parse_args()

    img_folder = args.img_folder
    
    # 检查文件夹是否存在
    if not os.path.exists(img_folder):
        print(f'指定的文件夹不存在： {img_folder}')
        print('Usage: python img2md.py <img_folder>')
        sys.exit(1)
    
    # 获取文件夹下所有图片文件, 支持 PNG, JPG, JPEG 格式, 并按文件名排序
    images = sorted(glob.glob(f'{img_folder}/*.png') + glob.glob(f'{img_folder}/*.jpg') + glob.glob(f'{img_folder}/*.jpeg'))
    
    # 总共要处理N个图片
    print(f'总共要处理 {len(images)} 张图片')
    
    # 创建一个img_folder_当前时间戳.md文件
    output_file = f'{img_folder}_{int(time.time())}.md'
    
    try:
        with open(output_file, 'w') as f:
            for img in images:
                print(f'正在处理 {images.index(img) + 1} / {len(images)}')
                text_content = ocr_by_google_cloud(img)
                markdown_output = format_to_markdown_ref_image(text_content, img)
                if markdown_output:
                    f.write(markdown_output)
                    f.write('\n\n')
    except Exception as e:
        print(f"保存 Markdown 文件时发生错误: {e}")
        sys.exit(1)

    print(f'处理完成，结果已保存到 {output_file}')
