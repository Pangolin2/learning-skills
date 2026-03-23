#!/bin/bash
# get_transcript.sh - 获取BBC 6 Minute English视频字幕

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 帮助信息
show_help() {
    echo -e "${BLUE}BBC 6 Minute English 字幕获取工具${NC}"
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -u, --url URL          YouTube视频URL"
    echo "  -t, --title TITLE      视频标题（用于搜索）"
    echo "  -d, --date DATE        日期（格式：YYMMDD，如260312）"
    echo "  -o, --output FILE      输出文件（默认：transcript.txt）"
    echo "  -k, --keep             保留PDF文件（默认删除）"
    echo "  -h, --help             显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 -u \"https://www.youtube.com/watch?v=fi3uJy8KsUU\""
    echo "  $0 -t \"Should we pay more for chocolate\" -d 260312"
    echo ""
}

# 检查依赖
check_dependencies() {
    local missing=()
    
    for cmd in curl pdftotext; do
        if ! command -v $cmd &> /dev/null; then
            missing+=("$cmd")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${RED}错误：缺少必要的依赖：${missing[*]}${NC}"
        echo "请安装："
        for cmd in "${missing[@]}"; do
            case $cmd in
                curl) echo "  sudo apt-get install curl" ;;
                pdftotext) echo "  sudo apt-get install poppler-utils" ;;
            esac
        done
        exit 1
    fi
}

# 从YouTube URL提取标题
extract_title_from_url() {
    local url="$1"
    echo -e "${YELLOW}正在从YouTube获取视频信息...${NC}"
    
    # 尝试获取页面标题
    local title=$(curl -s "$url" | grep -o '"title":"[^"]*"' | head -1 | sed 's/"title":"//' | sed 's/"//')
    
    if [ -z "$title" ]; then
        echo -e "${RED}无法从URL提取标题${NC}"
        return 1
    fi
    
    echo -e "${GREEN}找到标题：$title${NC}"
    echo "$title"
}

# 构建PDF URL
build_pdf_url() {
    local title="$1"
    local date="$2"
    
    # 清理标题：小写、替换空格为下划线、移除特殊字符
    local clean_title=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/ /_/g' | sed 's/[^a-z0-9_]//g')
    
    # 构建PDF URL
    local pdf_url="https://downloads.bbc.co.uk/learningenglish/features/6min/${date}_${clean_title}_transcript_.pdf"
    
    echo "$pdf_url"
}

# 下载并转换PDF
download_and_convert() {
    local pdf_url="$1"
    local output_file="$2"
    local keep_pdf="$3"
    
    local pdf_file="/tmp/bbc_transcript_$$.pdf"
    local temp_txt_file="/tmp/bbc_transcript_$$.txt"
    
    echo -e "${YELLOW}正在下载PDF...${NC}"
    echo -e "URL: $pdf_url"
    
    # 下载PDF
    if ! curl -s -o "$pdf_file" "$pdf_url"; then
        echo -e "${RED}下载PDF失败${NC}"
        return 1
    fi
    
    # 检查文件大小
    local file_size=$(stat -c%s "$pdf_file" 2>/dev/null || stat -f%z "$pdf_file")
    if [ "$file_size" -lt 1000 ]; then
        echo -e "${RED}下载的文件可能无效（大小：${file_size}字节）${NC}"
        return 1
    fi
    
    echo -e "${GREEN}PDF下载成功（${file_size}字节）${NC}"
    
    # 转换为文本
    echo -e "${YELLOW}正在转换为文本...${NC}"
    if ! pdftotext "$pdf_file" "$temp_txt_file"; then
        echo -e "${RED}PDF转换失败${NC}"
        return 1
    fi
    
    # 复制到输出文件
    cp "$temp_txt_file" "$output_file"
    echo -e "${GREEN}字幕已保存到：$output_file${NC}"
    
    # 显示前10行
    echo -e "\n${BLUE}=== 字幕预览 ===${NC}"
    head -20 "$output_file"
    echo -e "${BLUE}================${NC}\n"
    
    # 清理临时文件
    rm -f "$temp_txt_file"
    if [ "$keep_pdf" != "true" ]; then
        rm -f "$pdf_file"
    else
        echo -e "${YELLOW}PDF文件保留在：$pdf_file${NC}"
    fi
    
    return 0
}

# 主函数
main() {
    local youtube_url=""
    local video_title=""
    local video_date=""
    local output_file="transcript.txt"
    local keep_pdf="false"
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -u|--url)
                youtube_url="$2"
                shift 2
                ;;
            -t|--title)
                video_title="$2"
                shift 2
                ;;
            -d|--date)
                video_date="$2"
                shift 2
                ;;
            -o|--output)
                output_file="$2"
                shift 2
                ;;
            -k|--keep)
                keep_pdf="true"
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}未知选项：$1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 检查依赖
    check_dependencies
    
    # 如果没有提供标题，尝试从URL提取
    if [ -z "$video_title" ] && [ -n "$youtube_url" ]; then
        video_title=$(extract_title_from_url "$youtube_url")
        if [ $? -ne 0 ]; then
            echo -e "${RED}请使用 -t 参数提供视频标题${NC}"
            exit 1
        fi
    fi
    
    # 检查必要参数
    if [ -z "$video_title" ]; then
        echo -e "${RED}错误：必须提供视频标题${NC}"
        show_help
        exit 1
    fi
    
    if [ -z "$video_date" ]; then
        echo -e "${YELLOW}警告：未提供日期，尝试自动检测...${NC}"
        # 这里可以添加自动检测日期的逻辑
        echo -e "${RED}请使用 -d 参数提供日期（格式：YYMMDD）${NC}"
        show_help
        exit 1
    fi
    
    # 构建PDF URL
    local pdf_url=$(build_pdf_url "$video_title" "$video_date")
    
    # 下载并转换
    download_and_convert "$pdf_url" "$output_file" "$keep_pdf"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 字幕获取完成！${NC}"
        echo -e "文件：$output_file"
        echo -e "大小：$(wc -l < "$output_file") 行"
    else
        echo -e "${RED}❌ 字幕获取失败${NC}"
        exit 1
    fi
}

# 运行主函数
main "$@"