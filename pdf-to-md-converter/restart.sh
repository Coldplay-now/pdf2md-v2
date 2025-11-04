#!/bin/bash
# PDF to Markdown Converter - 重启脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  PDF to Markdown Converter${NC}"
echo -e "${BLUE}  重启服务${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 停止服务
echo -e "${BLUE}🛑 步骤 1/2: 停止现有服务...${NC}"
"$APP_DIR/stop.sh"

echo ""
echo -e "${BLUE}⏳ 等待 2 秒...${NC}"
sleep 2

echo ""
# 启动服务
echo -e "${BLUE}🚀 步骤 2/2: 启动服务...${NC}"
"$APP_DIR/start.sh"

