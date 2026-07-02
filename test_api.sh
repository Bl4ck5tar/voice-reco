#!/bin/bash

# 'EOF' 
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

API_URL="http://localhost:5000"

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}=====================================${NC}"echo -e "${BLUE}
echo ""

## 

#echo -e "${YELLOW}1
  Testing Health Check...${NC}"
HEALTH=$(curl -s "$API_URL/health")
echo "Response: $HEALTH"
echo ""


#echo -e "${YELLOW}2
  Testing Language List...${NC}"
LANGS=$(curl -s "$API_URL/languages" | head -50)
echo "Response: $LANGS"
echo ""

            {                 echo ___BEGIN___COMMAND_OUTPUT_MARKER___;                 PS1="";PS2="";unset HISTFILE;                 EC=$?;                 echo "___BEGIN___COMMAND_DONE_MARKER___$
#echo -e "${YELLOW}3
  Testing Transcription...${NC}"
echo -e "${YELLOW}Note: Upload an audio file at http://localhost:8080${NC}"
echo ""

echo -e "${ API is running and ready!${NC}"GREEN}
echo ""
echo -e "${BLUE}API Endpoints:${NC}"
echo "  Health:      GET  $API_URL/health"
echo "  Languages:   GET  $API_URL/languages"
echo "  Transcribe:  POST $API_URL/transcribe"
echo ""
echo -e "${BLUE}Web Demo:${NC}"
echo "  http://localhost:8080"
