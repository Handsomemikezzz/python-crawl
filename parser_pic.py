from PIL import Image
import os

def convert_awebp_to_jpg(input_path,output_folder=None,quality=85):
    """
    将awebd保存为Jpg
    """
    try:
        with Image.open(input_path) as img:
            if img.mode in ("RGB",'LA'):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1]) # 选取阿尔法作为通道
                img = background

                base_name = os.path.basename(input_path).split(".")[0]
                output_dir = output_folder if output_folder else os.path.dirname(input_path)# 若未指定输出目录则输出到原路径
                output_path = os.path.join(output_dir,f"{base_name}.jpg")

                img.convert("RGB").save(output_path,"JPEG",quality=quality)
                return output_path
    except Exception as e:
        print(f"Error converting :{str(e)}")
        return None