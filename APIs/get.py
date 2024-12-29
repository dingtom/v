# 导入requests库，用于发送网络请求
import requests
# 从datetime模块导入datetime和timedelta类，用于处理日期和时间
from datetime import datetime, timedelta
# 导入yaml库，用于处理YAML格式的数据
import yaml
import logging
import base64
import os
import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
log_path = 'get.log'
if os.path.exists('get.log'):
    os.remove('get.log')
file_handler_new = logging.FileHandler(log_path, mode='w')
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

#import os
#os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
#os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'

urls = [
    "https://raw.githubusercontent.com/SamanGho/v2ray_collector/refs/heads/main/base64",
    "https://bulinkbulink.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://proxy.v2gh.com/https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    f"https://shareclash.github.io/uploads/{year}/{month}/0-{day}.txt",
    f"https://shareclash.github.io/uploads/{year}/{month}/1-{day}.txt",
    f"https://shareclash.github.io/uploads/{year}/{month}/2-{day}.txt",
    f"https://shareclash.github.io/uploads/{year}/{month}/3-{day}.txt",
    f"https://shareclash.github.io/uploads/{year}/{month}/4-{day}.txt", 
    f"https://shareclash.github.io/uploads/{year}/{month}/0-{int(day)-1}.txt",
    f"https://shareclash.github.io/uploads/{year}/{month}/1-{int(day)-1}.txt",
    f"https://shareclash.github.io/uploads/{year}/{month}/2-{int(day)-1}.txt",
    f"https://shareclash.github.io/uploads/{year}/{month}/3-{int(day)-1}.txt",
    f"https://shareclash.github.io/uploads/{year}/{month}/4-{int(day)-1}.txt", 
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://fs.v2rayse.com/share/20241229/veowliarr5.txt",
    "https://testingcf.jsdelivr.net/gh/chengaopan/AutoMergePublicNodes@master/list.txt",
    
    "https://raw.githubusercontent.com/snakem982/proxypool/main/source/v2ray.txt",
    "https://raw.githubusercontent.com/a2470982985/getNode/main/v2ray.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/yudou66.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/clashmeta.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/ndnode.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodev2ray.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodefree.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/v2rayshare.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/wenode.txt",
]


# 2. 从订阅内容中提取服务器地址
def extract_servers(decoded_data):
    servers = []
    lines = decoded_data.splitlines()
    for line in lines:
        # 每个服务器地址可能以 'ss://' 开头 (这是ss协议的标识)
        if line.startswith("ss://") or line.startswith("vmess://"):
            servers.append(line)
    return servers

# 3. 测试服务器是否可用
def test_server(server):
    try:
        # 假设V2Ray服务器的端口通常是 443 或其他常见端口
        # 这里只是测试HTTP连接的有效性，通常你需要更复杂的连接验证
        url = f"https://{server.split('@')[1].split(':')[0]}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False
    return False



def gets():
    # 遍历urls列表中的每个URL
    available_servers = []
    for url in urls:
        logger.info(f"Processing URL: {url}")
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                # decoded_text = response.content.decode('gbk')  # 将响应内容解码为gbk格式的字符串
                # # 将解码后的文本写入文件
                # with open(file_name, 'w', encoding='gbk') as file:
                #     file.write(decoded_text)
                # response_string = response.content.decode('utf-8')
                content_data = response.content
                try:
                    decoded_data = base64.b64decode(content_data).decode('utf-8')
                except:
                    decoded_data = content_data.decode('utf-8')

                if decoded_data:
                    available_servers.extend(extract_servers(decoded_data))
            # 如果响应状态码不是200，打印失败信息
            else:
                logger.info(f"Failed to fetch content from URL: {url}")
        # 捕获并打印任何异常信息
        except Exception as e:
            logger.error(f"Error URL: {url}, Error: {e}")
            return
        available_servers = set(available_servers)
        with open('1.txt', "w") as file:
            for server in available_servers:
                file.write(server + "\n")
gets()
