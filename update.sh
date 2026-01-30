#!/bin/bash

# 1. 确保进入项目目录
cd ~/write_bot || exit

# 2. 拉取最新代码
echo "--- [1/5] Pulling Code ---"
git pull

# 3. 虚拟环境管理 (核心变更)
# 如果 venv 文件夹不存在，就创建一个
if [ ! -d "venv" ]; then
    echo "--- [2/5] Creating Virtual Environment ---"
    python3 -m venv venv
fi

# 4. 激活环境
# 这一步之后，所有的 pip 和 python 命令都会自动指向 venv 内部
source venv/bin/activate

# 5. 安装依赖 (安装进 venv，不污染系统)
echo "--- [3/5] Installing Dependencies ---"
pip install -r requirements.txt

# 6. 重启服务
echo "--- [4/5] Restarting Service ---"
pkill -f streamlit

# 7. 启动新进程 (使用 venv 里的 python)
nohup streamlit run app.py > app.log 2>&1 &

echo "========================================"
echo " Update Success! (Running in venv) "
echo " Use 'tail -f app.log' to see logs."
echo "========================================"