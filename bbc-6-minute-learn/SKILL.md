---
name: bbc-6-minute-learn
description: 获取BBC 6 Minute English视频字幕并生成详细的学习笔记，包含词汇音标、解析和学习建议。适用于英语学习者辅助学习。
author: Boxi
version: 1.0.0
triggers:
  - "BBC 6 Minute English"
  - "bbc learning english 字幕"
  - "6分钟英语 学习"
  - "BBC英语学习"
metadata:
  priority: high
---

# BBC 6 Minute English 学习助手

专门用于处理BBC 6 Minute English视频，提取字幕并生成详细的学习笔记。

## 功能特性

- ✅ 自动获取视频信息和上传日期
- ✅ 从BBC Learning English官网获取完整字幕
- ✅ 生成包含音标的学习笔记
- ✅ 解析重点词汇和句子
- ✅ 提供学习建议

## 使用方式

### 方式1：提供YouTube URL
```
获取 https://www.youtube.com/watch?v=GPbPAC0xS1s 的字幕并分析
```

### 方式2：提供标题和日期
```
获取 BBC 6 Minute English "How do we adapt to the cold?" 260319 的学习笔记
```

## 执行流程

### 1. 获取字幕
运行脚本获取字幕：
```bash
bash ~/.openclaw/workspace/skills/bbc-6-minute-learn/references/get_transcript.sh -u "<youtube_url>"
```

### 2. 分析字幕
运行分析脚本生成学习笔记：
```bash
python3 ~/.openclaw/workspace/skills/bbc-6-minute-learn/references/analyze_transcript.py transcript.txt
```

### 3. 查看结果
分析结果保存在：
- `transcript.txt` - 原始字幕
- `analysis.md` - 学习笔记

## 输出格式

学习笔记包含：
1. **节目概述** - 标题、日期、主持人、内容摘要
2. **框架分析** - 节目结构、各部分要点
3. **词汇表** - 包含音标、释义、例句
4. **重点句子** - 详细解析
5. **学习建议** - 听、说、读、写、词汇学习建议
6. **完整原文** - 可用于跟读练习

## 示例输出

详见 `references/example_analysis.md`

## 依赖

- `curl` - 网页内容获取
- `yt-dlp` - YouTube视频信息提取
- `python3` - 脚本运行

## 故障排除

- **无法获取日期**：使用 `yt-dlp --get-filename -o "%(upload_date)s" <url>`
- **BBC页面访问失败**：检查网络连接，或直接提供BBC页面URL
- **脚本错误**：查看错误信息，通常是缺少依赖或URL格式问题
