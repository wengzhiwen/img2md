import argparse
import base64
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

import requests
from dotenv import load_dotenv
from natsort import natsorted

@dataclass
class OpenAIClientConfig:
    model: str
    api_url: str
    timeout: float
    api_key: Optional[str] = None


def image_to_base64(image_path: Path) -> str:
    with image_path.open("rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def collect_images(folder: Path) -> List[Path]:
    patterns = ("*.png", "*.jpg", "*.jpeg")
    candidates: List[Path] = []
    for pattern in patterns:
        candidates.extend(folder.glob(pattern))
    # Ensure natural order to keep consistent with original script behavior.
    return [Path(p) for p in natsorted(candidates, key=lambda p: p.name)]


def call_openai(*, config: OpenAIClientConfig, images: Optional[Iterable[str]] = None) -> str:
    headers = {"Content-Type": "application/json"}
    if config.api_key:
        headers["Authorization"] = f"Bearer {config.api_key}"

    user_content = []
    user_content.append({
        "type": "text",
        "text": "请严格按照系统提示进行OCR识别，不要添加任何解释或说明",
    })
    for image_data in images or []:
        user_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{image_data}",
            },
        })

    system_prompt = """你是一个专业的OCR文本识别专家。
请仔细观察图像中的文本内容，并尽可能准确地提取所有文本和表格。
输出应该保持原始文本的格式和结构，包括格式（加粗、斜体、下划线、表格）、段落和标题。
针对表格的提取，可以采用markdown的语法来表示，特别注意表格的列数（有些表格首行有空单元格，也要算作一列）

请注意：
1. 仅提取图像中的实际文本，不要添加任何解释或说明
2. 保持原始语言文本，不要翻译
3. 尽可能保持原始格式结构，特别是表格，要准确的提取表格中的所有文字
4. 忽略所有的纯图形内容（比如：logo，地图等，包括页面上的水印）
5. 忽略所有的页眉和页脚，但保留原文中每页的页码（如果原文中有），严格按照原文中标注的页码来提取（不论原文是否有错）
6. 如果遇到空白页或整页都是没有意义的内容，请返回：EMPTY_PAGE"""

    payload = {
        "model": config.model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_content,
            },
        ],
        "stream": False,
    }

    try:
        response = requests.post(config.api_url, headers=headers, json=payload, timeout=config.timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"OpenAI兼容接口请求失败: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("无法解码OpenAI兼容接口的JSON响应") from exc

    try:
        message = data["choices"][0]["message"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError("OpenAI兼容接口响应格式异常") from exc

    content = message.get("content", "")
    if isinstance(content, list):
        texts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") in ("text", "output_text"):
                texts.append(part.get("text", ""))
        return "".join(texts).strip()
    if isinstance(content, str):
        return content.strip()

    raise RuntimeError("OpenAI兼容接口不支持的消息内容格式")


def ocr_with_openai(image_path: Path, *, config: OpenAIClientConfig) -> str:
    image_base64 = image_to_base64(image_path)
    return call_openai(config=config, images=[image_base64])


def build_output_path(folder: Path, timestamp: int, suffix: Optional[str] = None) -> Path:
    suffix_part = f"_{suffix}" if suffix else ""
    filename = f"{folder.name}_{timestamp}{suffix_part}.md"
    return folder.parent / filename


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="使用兼容 OpenAI 接口的本地多模态模型，将图片（PNG 或 JPG）识别为 Markdown 文本。")
    parser.add_argument("img_folder", help="包含图片的文件夹。")
    return parser.parse_args()


def run_ocr(img_folder: Path, *, config: OpenAIClientConfig) -> None:
    images = collect_images(img_folder)
    if not images:
        print(f"在 {img_folder} 中未找到图片。支持的格式：png, jpg, jpeg。")
        sys.exit(0)
    print(f"共 {len(images)} 张图片待处理...")

    timestamp = int(time.time())
    output_path = build_output_path(img_folder, timestamp)

    print(f"使用模型 '{config.model}' 通过 {config.api_url}")
    print(f"将OCR结果写入Markdown文件：{output_path}")

    failures = []
    try:
        with output_path.open("w", encoding="utf-8") as ocr_file:
            for idx, image_path in enumerate(images, start=1):
                print(f"正在处理 {idx} / {len(images)}: {image_path.name}")
                try:
                    text_content = ocr_with_openai(image_path, config=config)
                except RuntimeError as exc:
                    print(f"  处理失败 {image_path.name}: {exc}")
                    failures.append(image_path.name)
                    continue
                if text_content:
                    ocr_file.write(text_content)
                    ocr_file.write("\n\n")
    except OSError as exc:
        print(f"保存Markdown文件时发生错误: {exc}")
        sys.exit(1)

    print("处理完成。")
    if failures:
        print(f"处理完成，有 {len(failures)} 个失败: {', '.join(failures)}")
    print(f"OCR Markdown已保存到 {output_path}")


def main() -> None:
    load_dotenv()
    args = parse_args()

    img_folder = Path(args.img_folder).expanduser().resolve()
    if not img_folder.exists() or not img_folder.is_dir():
        print(f"指定的文件夹不存在或不是目录: {img_folder}")
        print("用法: python img2md.py <img_folder>")
        print('例如: "python img2md.py ." 处理当前文件夹')
        sys.exit(1)

    api_url = os.getenv("BASE_URL")
    model = os.getenv("MODEL_FOR_OCR")
    api_key = os.getenv("API_KEY_FOR_OCR")
    timeout = float(os.getenv("TIMEOUT_FOR_OCR", "120"))

    client_config = OpenAIClientConfig(model=model, api_url=api_url, timeout=timeout, api_key=api_key)

    run_ocr(img_folder, config=client_config)


if __name__ == "__main__":
    main()
