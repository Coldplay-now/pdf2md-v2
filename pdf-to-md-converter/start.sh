#!/bin/bash
# PDF to Markdown Converter - 启动脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
APP_NAME="PDF to Markdown Converter"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$APP_DIR/app.pid"
LOG_FILE="$APP_DIR/app.log"
HOST="0.0.0.0"
PORT=8000

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  $APP_NAME${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 检查是否已经在运行
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  服务已在运行中 (PID: $PID)${NC}"
        echo -e "${YELLOW}   如需重启，请先运行: ./stop.sh${NC}"
        echo ""
        echo -e "${GREEN}   访问地址: http://localhost:$PORT${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  发现旧的PID文件，正在清理...${NC}"
        rm -f "$PID_FILE"
    fi
fi

# 检查Python
echo -e "${BLUE}📦 检查环境...${NC}"
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ 未找到Python，请先安装Python 3.10+${NC}"
    exit 1
fi

# 使用python3或python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# 检查Python版本
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python版本: $PYTHON_VERSION${NC}"

# 检查是否在虚拟环境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠️  未检测到虚拟环境${NC}"
    echo -e "${YELLOW}   建议使用虚拟环境: python -m venv venv && source venv/bin/activate${NC}"
    echo ""
fi

# 检查依赖
echo -e "${BLUE}📦 检查依赖...${NC}"
if ! $PYTHON_CMD -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  未安装依赖，正在安装...${NC}"
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ 依赖安装失败${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ 依赖安装完成${NC}"
else
    echo -e "${GREEN}✓ 依赖已安装${NC}"
fi

# 检查模型
echo -e "${BLUE}🤖 检查模型...${NC}"
MODEL_PATH="/personal/1102case/models/paddleocr-vl"
if [ ! -d "$MODEL_PATH" ]; then
    echo -e "${RED}✗ 未找到模型: $MODEL_PATH${NC}"
    echo -e "${RED}   请确保模型已下载到正确位置${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 模型路径正确${NC}"

# 检查端口占用
echo -e "${BLUE}🔌 检查端口 $PORT...${NC}"
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${RED}✗ 端口 $PORT 已被占用${NC}"
    echo -e "${YELLOW}   占用进程:${NC}"
    lsof -Pi :$PORT -sTCP:LISTEN
    echo ""
    echo -e "${YELLOW}   您可以:${NC}"
    echo -e "${YELLOW}   1. 修改 app.py 中的端口号${NC}"
    echo -e "${YELLOW}   2. 或停止占用端口的进程: lsof -ti:$PORT | xargs kill -9${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 端口 $PORT 可用${NC}"

# 创建必要的目录
mkdir -p "$APP_DIR/uploads"
mkdir -p "$APP_DIR/outputs"

# 启动服务
echo ""
echo -e "${BLUE}🚀 启动服务...${NC}"
cd "$APP_DIR"

# 后台运行
nohup $PYTHON_CMD app.py > "$LOG_FILE" 2>&1 &
APP_PID=$!

# 保存PID
echo $APP_PID > "$PID_FILE"

# 等待服务启动
echo -e "${BLUE}⏳ 等待服务启动...${NC}"
sleep 3

# 检查服务是否成功启动
if ps -p $APP_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 服务启动成功！${NC}"
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}  服务信息${NC}"
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}PID:        ${NC}$APP_PID"
    echo -e "${GREEN}访问地址:   ${NC}http://localhost:$PORT"
    echo -e "${GREEN}API文档:    ${NC}http://localhost:$PORT/docs"
    echo -e "${GREEN}日志文件:   ${NC}$LOG_FILE"
    echo -e "${GREEN}PID文件:    ${NC}$PID_FILE"
    echo ""
    echo -e "${BLUE}💡 使用提示:${NC}"
    echo -e "   查看日志: tail -f $LOG_FILE"
    echo -e "   停止服务: ./stop.sh"
    echo -e "   重启服务: ./stop.sh && ./start.sh"
    echo ""
    
    # 尝试健康检查
    sleep 2
    if command -v curl &> /dev/null; then
        echo -e "${BLUE}🔍 健康检查...${NC}"
        if curl -s http://localhost:$PORT/api/health > /dev/null; then
            echo -e "${GREEN}✓ 服务响应正常${NC}"
        else
            echo -e "${YELLOW}⚠️  服务可能还在初始化中${NC}"
        fi
    fi
    
    echo ""
    echo -e "${GREEN}🎉 启动完成！打开浏览器访问 http://localhost:$PORT${NC}"
else
    echo -e "${RED}✗ 服务启动失败${NC}"
    echo -e "${RED}   请查看日志: tail -f $LOG_FILE${NC}"
    rm -f "$PID_FILE"
    exit 1
fi

