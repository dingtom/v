# 导入requests库，用于发送网络请求
import requests
# 从datetime模块导入datetime和timedelta类，用于处理日期和时间
from datetime import datetime, timedelta
# 导入yaml库，用于处理YAML格式的数据
import yaml
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
if os.path.exists('get.log'):
    os.remove('get.log')
file_handler_new = logging.FileHandler('get.log')
file_handler_new.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # 使用同样的格式化字符串
file_handler_new.setFormatter(formatter)
logger.addHandler(file_handler_new)

current_date = datetime.now()
year = current_date.strftime('%Y')
month = current_date.strftime('%m')
day = current_date.strftime('%Y%m%d')
yesterday_date = current_date - timedelta(days=1)
y_day = yesterday_date.strftime('%Y%m%d')

# 定义一个包含URLs的列表，这些URLs用于访问网络上的YAML和TXT文件
urls = [
    # 使用f-string格式化字符串，插入年、月、日的值，构建URL
    f"https://clashgithub.github.io/uploads/{year}/{month}/0-{day}.txt", 
    f"https://clashgithub.github.io/uploads/{year}/{month}/1-{day}.txt", 
    f"https://clashgithub.github.io/uploads/{year}/{month}/2-{day}.txt", 
    f"https://clashgithub.github.io/uploads/{year}/{month}/3-{day}.txt", 
    f"https://clashgithub.github.io/uploads/{year}/{month}/4-{day}.txt" 
]

# 定义一个名为gets的函数，用于从URLs获取数据并保存
def gets():
    # 遍历urls列表中的每个URL
    for i, url in enumerate(urls):
        logger.info(f"Processing URL: {url}")
        try:
            # 发送GET请求到URL，verify=False表示不验证SSL证书
            response = requests.get(url, verify=False)
            # 检查响应的状态码是否为200（成功）
            if response.status_code == 200:
                # 如果URL包含"shareclash"，则处理YAML文件
                if "shareclash" in url:
                    file_name = f"sc{i}.yaml"  # 定义文件名
                    decoded_text = response.content.decode('utf-8')  # 将响应内容解码为utf-8格式的字符串
                    data = yaml.safe_load(decoded_text)  # 使用yaml库解析YAML内容
                    # 将解析后的数据写入文件
                    with open(file_name, 'w', encoding='utf-8') as file:
                        yaml.dump(data, file, allow_unicode=True)
                    logger.debug(f"YAML content from {url} saved to {file_name}")  # 打印保存成功的信息
                # 否则，处理TXT文件
                else:
                    file_name = f"cg{i-5}.txt"  # 定义文件名
                    decoded_text = response.content.decode('gbk')  # 将响应内容解码为gbk格式的字符串
                    # 将解码后的文本写入文件
                    with open(file_name, 'w', encoding='gbk') as file:
                        file.write(decoded_text)
                    logger.debug(f"Text content from {url} saved to {file_name}")  # 打印保存成功的信息
            # 如果响应状态码不是200，打印失败信息
            else:
                logger.info(f"Failed to fetch content from URL: {url}")
        # 捕获并打印任何异常信息
        except Exception as e:
            logger.error("An error occurred:", e)

# 调用gets函数执行
gets()