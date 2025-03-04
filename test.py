import os
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re
from urllib.parse import urljoin
import time
import random

def get_response(url, headers=None, timeout=5):
    """通用请求函数"""
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except RequestException as e:
        print(f"请求失败: {url} - {str(e)}")
        return None

def parse_links(soup, pattern=None):
    """解析页面链接"""
    return soup.find_all('a', href=re.compile(pattern))

def download_resource(url, save_path, headers=None):
    """通用资源下载函数"""
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb' if isinstance(response.content, bytes) else 'w') as f:
                f.write(response.content if isinstance(response.content, bytes) else response.text)
            return True
    except Exception as e:
        print(f"下载失败: {url} - {str(e)}")
    return False

def process_images(soup, base_url, save_dir):
    """图片处理专用函数"""
    image_dir = os.path.join(save_dir, "assets") # html/assets
    for img in soup.find_all('img'):
        img_url = urljoin(img_base_url, img['src'])
        # img_name = os.path.basename(img_url.split("?")[0]) #https://learn.lianglianglee.com/%E4%B8%93%E6%A0%8F/%E7%A8%8B%E5%BA%8F%E5%91%98%E7%9A%84%E4%B8%AA%E4%BA%BA%E8%B4%A2%E5%AF%8C%E8%AF%BE/assets/d1c51fa77e264189b823ab5d46b6f48b.jpg
        img_path = os.path.join(image_dir, os.path.basename(img_url))# html/assets/xxxxx.jpg
        
        if download_resource(img_url, img_path):
            img['src'] = os.path.relpath(img_path, save_dir)  # 计算img_path相对与save_dir的路径，不是replace，而是relpath

def crawl_article(link, base_url, save_dir, headers):
    """单篇文章爬取处理"""
    full_url = urljoin(base_url, link['href'])
    response = get_response(full_url, headers)
    if not response:
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    process_images(soup, base_url, save_dir)  # 处理图片
    
    file_name = os.path.basename(link['href'])
    file_name = file_name if file_name.endswith('.html') else f"{file_name}.html"
    file_path = os.path.join(save_dir, file_name)
    
    if download_resource(full_url, file_path, headers):
        print(f"已保存：{file_path}")

# 主流程
if __name__ == "__main__":
    # 初始化配置
    config = {
        'main_url': "https://learn.lianglianglee.com/专栏/程序员的个人财富课",
        'save_dir': "html_files",
        'base_url': "https://learn.lianglianglee.com",
        'match_pattern': r'^/专栏/程序员的个人财富课',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }

    img_base_url = "https://learn.lianglianglee.com/%E4%B8%93%E6%A0%8F/%E7%A8%8B%E5%BA%8F%E5%91%98%E7%9A%84%E4%B8%AA%E4%BA%BA%E8%B4%A2%E5%AF%8C%E8%AF%BE/"
    # 创建保存目录
    os.makedirs(config['save_dir'], exist_ok=True)

    # 获取主页面
    main_response = get_response(config['main_url'], config['headers'])
    if main_response.status_code==200:
        main_soup = BeautifulSoup(main_response.content, 'html.parser')
        article_links = parse_links(main_soup, config['match_pattern'])
        
        for link in article_links:
            crawl_article(link, config['base_url'], config['save_dir'], config['headers'])
            time.sleep(random.uniform(10, 12))