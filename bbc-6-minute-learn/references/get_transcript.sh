#!/bin/bash
# get_transcript.sh - 获取BBC 6 Minute English视频字幕

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

OUTPUT_FILE="transcript.txt"

show_help() {
    echo -e "${BLUE}BBC 6 Minute English 字幕获取工具${NC}"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -u, --url URL          YouTube视频URL"
    echo "  -b, --bbc URL          BBC Learning English页面URL"
    echo "  -d, --date DATE        日期（格式：YYMMDD）"
    echo "  -o, --output FILE      输出文件（默认：transcript.txt）"
    echo "  -h, --help             显示帮助"
}

check_dependencies() {
    for cmd in curl yt-dlp python3; do
        if ! command -v $cmd &> /dev/null; then
            echo -e "${RED}缺少依赖: $cmd${NC}"
            exit 1
        fi
    done
}

main() {
    local youtube_url=""
    local bbc_url=""
    local video_date=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -u|--url) youtube_url="$2"; shift 2 ;;
            -b|--bbc) bbc_url="$2"; shift 2 ;;
            -d|--date) video_date="$2"; shift 2 ;;
            -o|--output) OUTPUT_FILE="$2"; shift 2 ;;
            -h|--help) show_help; exit 0 ;;
            *) echo -e "${RED}未知选项: $1${NC}"; exit 1 ;;
        esac
    done
    
    check_dependencies
    
    # 从YouTube获取BBC链接
    if [ -z "$bbc_url" ] && [ -n "$youtube_url" ]; then
        echo -e "${YELLOW}从YouTube获取BBC页面链接...${NC}"
        bbc_url=$(yt-dlp --get-description "$youtube_url" 2>/dev/null | grep -o 'https://bbc\.in/[a-zA-Z0-9]*' | head -1)
        [ -z "$bbc_url" ] && bbc_url=$(yt-dlp --get-description "$youtube_url" 2>/dev/null | grep -o 'https://www\.bbc\.co\.uk/learningenglish[^ ]*' | head -1)
        
        if [ -z "$video_date" ]; then
            video_date=$(yt-dlp --get-filename -o "%(upload_date)s" "$youtube_url" 2>/dev/null | tail -1)
        fi
    fi
    
    if [ -z "$bbc_url" ]; then
        echo -e "${RED}错误：需要提供YouTube URL或BBC页面URL${NC}"
        show_help
        exit 1
    fi
    
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}  BBC 6 Minute English 字幕获取${NC}"
    echo -e "${CYAN}========================================${NC}\n"
    echo -e "${BLUE}来源: $bbc_url${NC}"
    [ -n "$video_date" ] && echo -e "${BLUE}日期: $video_date${NC}"
    echo -e "${BLUE}输出: $OUTPUT_FILE${NC}\n"
    
    # 获取BBC页面内容并提取字幕
    echo -e "${YELLOW}正在访问BBC页面...${NC}"
    
    # 创建临时Python脚本
    local temp_py="/tmp/get_transcript_$$.py"
    
    cat > "$temp_py" << 'PYTHON_EOF'
import re
import subprocess
import sys

bbc_url = sys.argv[1]
output_file = sys.argv[2]

try:
    result = subprocess.run(['curl', '-s', '-L', bbc_url], 
                          capture_output=True, text=True, timeout=30)
    html = result.stdout
except Exception as e:
    print(f"获取页面失败: {e}", file=sys.stderr)
    sys.exit(1)

if not html:
    print("页面内容为空", file=sys.stderr)
    sys.exit(1)

# 提取 TRANSCRIPT 部分
start = html.find('<p class="p2">Note:')
if start == -1:
    start = html.find('TRANSCRIPT</strong>')
    
end = html.find('<h3>', start)
if end == -1:
    end = html.find('Next', start)

if start != -1 and end != -1:
    content = html[start:end]
    
    # 清理HTML
    text = re.sub(r'<br\s*/?>', '\n', content)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&[a-z]+;', '', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = text.strip()
    
    # 保存到文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    line_count = len(text.splitlines())
    print(f"SUCCESS:{line_count}")
else:
    print("ERROR: 无法找到字幕内容", file=sys.stderr)
    sys.exit(1)
PYTHON_EOF
    
    # 运行Python脚本
    python3 "$temp_py" "$bbc_url" "$OUTPUT_FILE"
    local result=$?
    rm -f "$temp_py"
    
    if [ $result -eq 0 ]; then
        echo -e "${GREEN}✅ 字幕获取成功！${NC}"
        echo -e "文件: $OUTPUT_FILE"
        echo -e "行数: $(wc -l < "$OUTPUT_FILE")"
        
        echo -e "\n${BLUE}=== 预览（前20行）===${NC}"
        head -20 "$OUTPUT_FILE"
        echo -e "${BLUE}=========================${NC}\n"
        
        [ -n "$video_date" ] && echo "$video_date" > "${OUTPUT_FILE}.date"
    else
        echo -e "${RED}❌ 字幕获取失败${NC}"
        exit 1
    fi
}

main "$@"
