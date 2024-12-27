import base64
import glob
import os
import sys
import argparse
import time
from dotenv import load_dotenv
from ollama import chat
from ollama import ChatResponse
from typing import Dict, List
from PIL import Image
from natsort import natsorted
import requests

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
    
def ocr_by_ollama(image_path):
    OLLAMA_MODEL =  "llama3.2-vision:11b-instruct-q4_K_M"
    
    # Ollama API endpoint
    url = "http://localhost:11434/api/generate"
    
    # 将图片转换为base64
    image_base64 = image_to_base64(image_path)
    
    # 构建请求数据
    data = {
        "model": OLLAMA_MODEL, 
        "prompt": "请OCR图片中的文字，注意识别文字中混排的emoji或其他日语常用的符号，表格中的文字也需要识别。不需要总结图片内容，只需要返回OCR的结果",
        "stream": False,
        "images": [image_base64]
    }

    try:
        # 发送POST请求到Ollama
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        return result['response']
        
    except requests.exceptions.RequestException as e:
        return f"Error occurred: {str(e)}"
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert images(PNG or JPG) to ONE markdown file.')
    parser.add_argument('img_folder', help='Folder for images.')
    parser.add_argument('--trans_to', help='Translate the content to the specified language.')
    args = parser.parse_args()

    img_folder = args.img_folder
    trans_to = args.trans_to
    
    if not os.path.exists(img_folder):
        print(f'The specified folder does not exist: {img_folder}')
        print('Usage: python img2md.py <img_folder>')
        print('e.g.: "python img2md.py ." for current folder')
        sys.exit(1)
    
    images = natsorted(glob.glob(f'{img_folder}/*.png') + 
        glob.glob(f'{img_folder}/*.jpg') + 
        glob.glob(f'{img_folder}/*.jpeg'))
    print(f'{len(images)} images to process...')
    
    output_file = f'{img_folder}_{int(time.time())}.md'
    
    try:
        with open(output_file, 'w') as f:
            for img in images:
                print(f'Processing {images.index(img) + 1} / {len(images)}')
                text_content = ocr_by_ollama(img)
                #markdown_output = format_to_markdown_ref_image(text_content, img)
                if text_content:
                    f.write(text_content)
                    f.write('\n\n')
    except Exception as e:
        print(f"Error occurred while saving the Markdown file: {e}")
        sys.exit(1)

    print(f'Processing complete, saved to {output_file}')
    
    if trans_to:
        print(f'Translated doc saved to {output_file_trans}')
