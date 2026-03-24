# BBC 6 Minute English 学习技能

## 流程总结

### 刚才的字幕提取流程

```
YouTube URL → yt-dlp获取视频信息 → 提取BBC页面链接 → curl访问BBC页面 → Python解析HTML → 提取字幕内容
```

#### 关键步骤：

1. **从YouTube获取BBC页面链接**
   ```bash
   yt-dlp --get-description "https://www.youtube.com/watch?v=GPbPAC0xS1s"
   ```
   - 从视频描述中提取BBC Learning English页面URL

2. **获取视频上传日期**
   ```bash
   yt-dlp --get-filename -o "%(upload_date)s" "https://www.youtube.com/watch?v=GPbPAC0xS1s"
   ```
   - 返回格式：20260319（YYMMDD）

3. **访问BBC页面提取字幕**
   ```bash
   curl -s -L "BBC页面URL" > /tmp/bbc_page.html
   ```
   - BBC页面包含完整的文字稿（TRANSCRIPT部分）

4. **Python解析HTML提取字幕**
   - 查找 `<p class="p2">Note:` 或 `<strong>TRANSCRIPT</strong>`
   - 清理HTML标签，保留纯文本
   - 处理特殊字符（&amp;, &nbsp;等）

### 为什么PDF方式失败？

- BBC的PDF下载链接经常返回404
- PDF URL格式虽然固定，但文件不一定存在
- 网页方式更可靠，因为BBC页面始终保持更新

## Skill文件结构

```
bbc-6-minute-learn/
├── SKILL.md                    # 技能说明文档
├── README.md                   # 本文档
└── references/
    ├── get_transcript.sh       # 字幕获取脚本
    ├── analyze_transcript.py   # 字幕分析脚本（增强版）
    └── example_analysis.md      # 分析结果示例
```

## 使用方法

### 1. 获取字幕

```bash
# 方式1：使用YouTube URL
bash references/get_transcript.sh -u "YouTube视频URL" -o transcript.txt

# 方式2：使用BBC页面URL
bash references/get_transcript.sh -b "BBC页面URL" -o transcript.txt

# 方式3：提供日期（可选）
bash references/get_transcript.sh -u "YouTube URL" -d 260319 -o transcript.txt
```

### 2. 分析字幕

```bash
# 生成学习笔记
python3 references/analyze_transcript.py transcript.txt learning_notes.md
```

### 3. 完整工作流

```bash
# 一站式获取+分析
bash get_transcript.sh -u "YouTube URL" -o transcript.txt
python3 analyze_transcript.py transcript.txt learning_notes.md
```

## 分析脚本特性（增强版）

### 新增功能

1. **词汇音标**
   - 内置常用词汇音标
   - 支持自定义扩展

2. **词汇级别标注**
   - CET4（大学英语4级）
   - CET6（大学英语6级）
   - IELTS（雅思）
   - TOEFL（托福）

3. **详细解析**
   - 重点句子分析
   - 关键词提取
   - 学习建议

4. **框架结构**
   - 节目时间线
   - 各部分内容概要
   - 核心主题总结

### 词汇级别说明

| 级别 | 标记 | 含义 |
|------|------|------|
| CET4 | 🟢 | 大学英语4级词汇 |
| CET6 | 🟠 | 大学英语6级词汇 |
| IELTS | 🔴 | 雅思/托福高阶词汇 |

## 依赖项

- `curl` - 网页内容获取
- `yt-dlp` - YouTube视频信息提取
- `python3` - 脚本运行环境

安装依赖：
```bash
# Ubuntu/Debian
sudo apt-get install curl python3

# yt-dlp (推荐使用pip安装)
pip3 install yt-dlp
```

## 故障排除

### 问题1：无法获取BBC链接
**解决方案**：手动从YouTube视频描述中复制BBC页面链接

### 问题2：BBC页面访问失败
**解决方案**：
- 检查网络连接
- 尝试使用VPN
- 直接提供BBC完整URL

### 问题3：字幕内容为空
**解决方案**：
- 确认BBC页面包含TRANSCRIPT部分
- 可能是页面结构变化，需要更新解析脚本

## 示例输出

详见 `references/example_analysis.md`

## 后续优化方向

1. ✅ 增加词汇音标
2. ✅ 增加词汇级别标注
3. 🔲 自动从YouTube URL推断BBC页面URL
4. 🔲 支持批量处理多个视频
5. 🔲 集成音频下载功能
6. 🔲 生成Anki闪卡格式
