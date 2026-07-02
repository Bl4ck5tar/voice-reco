#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}🎤 AI语音识别与翻译系统${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker未安装，请先安装Docker${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 第一步: 构建Docker镜像...${NC}"
docker build -t voice-recognition:latest .

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Docker镜像构建失败${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker镜像构建完成${NC}"
echo ""

# 检查容器是否已存在
if docker ps -a --format '{{.Names}}' | grep -q '^voice-api$'; then
    echo -e "${YELLOW}🔄 检测到已存在的容器，正在移除...${NC}"
    docker rm -f voice-api
fi

echo -e "${YELLOW}🚀 第二步: 启动API服务容器...${NC}"
docker run -d \
  --name voice-api \
  -p 5000:5000 \
  --memory=6g \
  voice-recognition:latest

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 容器启动失败${NC}"
    exit 1
fi

echo -e "${GREEN}✅ API容器已启动${NC}"
echo ""

# 等待容器完全启动
echo -e "${YELLOW}⏳ 等待API服务就绪...${NC}"
sleep 3

# 检查API是否可达
for i in {1..10}; do
    if curl -s http://localhost:5000/health > /dev/null; then
        echo -e "${GREEN}✅ API服务已就绪${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "${RED}❌ API服务未能启动，请检查日志${NC}"
        docker logs voice-api
        exit 1
    fi
    echo -e "${YELLOW}⏳ 等待中... ($i/10)${NC}"
    sleep 2
done

echo ""
echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}✨ 系统启动成功！${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

echo -e "${YELLOW}📱 Web Demo 地址:${NC}"
echo -e "${GREEN}http://localhost:8080${NC}"
echo ""

echo -e "${YELLOW}🔌 API 地址:${NC}"
echo -e "${GREEN}http://localhost:5000${NC}"
echo ""

echo -e "${YELLOW}📚 常用命令:${NC}"
echo "  查看日志:        docker logs voice-api"
echo "  停止容器:        docker stop voice-api"
echo "  重启容器:        docker restart voice-api"
echo "  删除容器:        docker rm -f voice-api"
echo ""

echo -e "${YELLOW}🎯 接下来:${NC}"
echo "  1. 在另一个终端运行: python3 demo_server.py"
echo "  2. 打开浏览器访问: http://localhost:8080"
echo "  3. 上传音频文件进行测试"
echo ""

echo -e "${YELLOW}📖 API文档:${NC}"
echo "  POST /transcribe - 转录和翻译音频"
echo "  GET  /health     - 检查API状态"
echo "  GET  /languages  - 获取支持的语言列表"
echo ""

read -p "按Enter键打开Demo网页... " -t 5 || true
if command -v open &> /dev/null; then
    open "http://localhost:8080" 2>/dev/null || true
fi
