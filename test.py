import os
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re
from urllib.parse import urljoin
import time
import random
from parser_pic import convert_awebp_to_jpg

def get_response(url, headers=None, timeout=5):
    """通用请求函数
    
    """
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


def crawl_article(link, base_url, save_dir, headers):
    """单篇文章爬取处理"""
    full_url = urljoin(base_url, link['href']) # 每个子页面的完整url
    response = get_response(full_url, headers) # 每个子页面的返回值
    if not response:
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    image_dir  = os.path.join(save_dir, 'assets') # 图片的存储目录
    for img in soup.find_all('img'):
        img_url = urljoin(img_base_url,img['src']) # 拼接出图片的访问路径
        clean_url = img_url.split('?')[0]
        img_name = os.path.basename(clean_url) # 图片的名字： 如xxx.jpg
        original_path = os.path.join(image_dir, img_name) # 图片存储的最终路径   如 assets/img.jpg 

        if download_resource(img_url, original_path):
            if original_path.endswith('.awebp'):
                jpg_path = convert_awebp_to_jpg(original_path)
                if jpg_path and os.path.exists(jpg_path):
                  os.remove(original_path)
                  new_jpg_path  = jpg_path
            else:
                new_jpg_path = original_path
        else:
            new_jpg_path = original_path
        img['src'] = os.path.relpath(new_jpg_path, save_dir)# 更新soup中图片的引用位置

    modify_soup = str(soup)
    # 保存修改后的内容为html文件,而不是通过download_resource重新打开内容
    file_name = os.path.basename(link['href'])
    file_name = file_name if file_name.endswith('.html') else f"{file_name}.html"
    file_path = os.path.join(save_dir, file_name)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modify_soup)
        print(f"已保存：{file_path}")

# 主流程
if __name__ == "__main__":
    # 初始化配置
    config = {
        'main_url': "https://learn.lianglianglee.com/%E4%B8%93%E6%A0%8F/Java%20%E5%B9%B6%E5%8F%91%EF%BC%9AJUC%20%E5%85%A5%E9%97%A8%E4%B8%8E%E8%BF%9B%E9%98%B6",
        'save_dir': "html_files",
        'base_url': "https://learn.lianglianglee.com",
        'match_pattern': r'^/专栏',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }

    img_base_url = config['main_url']+"/" # 用于拼接图片访问链接
    # 创建保存目录
    os.makedirs(config['save_dir'], exist_ok=True) # 存在也OK

    # 获取主页面
    main_response = get_response(config['main_url'], config['headers'])
    if main_response.status_code==200:
        main_soup = BeautifulSoup(main_response.content, 'html.parser')
        article_links = parse_links(main_soup, config['match_pattern'])
        
        for link in article_links:
            crawl_article(link, config['base_url'], config['save_dir'], config['headers'])
            time.sleep(random.uniform(5, 8))