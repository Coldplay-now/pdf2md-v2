#!/bin/bash
# PDF to Markdown Converter - 停止脚本

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

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  $APP_NAME - 停止服务${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 检查PID文件是否存在
if [ ! -f "$PID_FILE" ]; then
    echo -e "${YELLOW}⚠️  未找到PID文件，服务可能未运行${NC}"
    
    # 尝试查找进程
    echo -e "${BLUE}🔍 搜索相关进程...${NC}"
    PIDS=$(ps aux | grep "[p]ython.*app.py" | awk '{print $2}')
    
    if [ -z "$PIDS" ]; then
        echo -e "${GREEN}✓ 未发现运行中的服务${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  发现运行中的进程:${NC}"
        ps aux | grep "[p]ython.*app.py"
        echo ""
        read -p "是否要停止这些进程? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            for pid in $PIDS; do
                echo -e "${BLUE}🛑 停止进程 $pid...${NC}"
                kill $pid 2>/dev/null || true
            done
            sleep 2
            # 强制停止
            for pid in $PIDS; do
                if ps -p $pid > /dev/null 2>&1; then
                    echo -e "${YELLOW}⚠️  强制停止进程 $pid${NC}"
                    kill -9 $pid 2>/dev/null || true
                fi
            done
            echo -e "${GREEN}✓ 进程已停止${NC}"
        fi
        exit 0
    fi
fi

# 读取PID
PID=$(cat "$PID_FILE")
echo -e "${BLUE}📋 PID: $PID${NC}"

# 检查进程是否存在
if ! ps -p $PID > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  进程不存在（可能已停止）${NC}"
    rm -f "$PID_FILE"
    echo -e "${GREEN}✓ 已清理PID文件${NC}"
    exit 0
fi

# 显示进程信息
echo -e "${BLUE}📊 进程信息:${NC}"
ps -p $PID -o pid,ppid,cmd,%cpu,%mem,etime

echo ""
echo -e "${BLUE}🛑 正在停止服务...${NC}"

# 优雅停止（SIGTERM）
kill $PID 2>/dev/null || true

# 等待进程结束
WAIT_TIME=0
MAX_WAIT=10

while ps -p $PID > /dev/null 2>&1 && [ $WAIT_TIME -lt $MAX_WAIT ]; do
    echo -e "${YELLOW}⏳ 等待进程结束... ($WAIT_TIME/$MAX_WAIT)${NC}"
    sleep 1
    WAIT_TIME=$((WAIT_TIME + 1))
done

# 如果进程还在运行，强制停止
if ps -p $PID > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  进程未响应，强制停止...${NC}"
    kill -9 $PID 2>/dev/null || true
    sleep 1
fi

# 最终检查
if ps -p $PID > /dev/null 2>&1; then
    echo -e "${RED}✗ 停止失败，进程仍在运行${NC}"
    exit 1
else
    rm -f "$PID_FILE"
    echo -e "${GREEN}✓ 服务已停止${NC}"
    echo ""
    
    # 显示日志最后几行
    if [ -f "$LOG_FILE" ] && [ -s "$LOG_FILE" ]; then
        echo -e "${BLUE}📄 最后日志:${NC}"
        echo -e "${YELLOW}---${NC}"
        tail -n 5 "$LOG_FILE"
        echo -e "${YELLOW}---${NC}"
        echo ""
        echo -e "${BLUE}💡 查看完整日志: tail -f $LOG_FILE${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 停止完成！${NC}"
fi

