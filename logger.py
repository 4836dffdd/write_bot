# logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

# 确保日志目录存在 (防止报错)
if not os.path.exists("logs"):
    os.makedirs("logs")

# 幂等性检查：如果已经有 Logger 了，就不要重复添加 Handler，防止日志重复打印
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        handlers=[
            # 存文件：最多 5 个文件，每个 1MB，UTF-8 编码防止中文乱码
            RotatingFileHandler("logs/app.log", maxBytes=1024*1024, backupCount=5, encoding='utf-8'),
            # 输出到控制台：方便你在 Cursor 终端实时看
            logging.StreamHandler()
        ],
        level=logging.INFO,
        # 格式：时间 - 级别 - [文件名:行号] - 消息
        format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    )