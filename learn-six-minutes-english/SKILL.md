---
name: learn-six-minutes-english
description: |
  快速获取BBC 6 Minute English视频的官方字幕，并进行学习总结。
  包括：获取字幕、经典例句解析、关键词汇提取、学习建议。
emoji: 🇬🇧
requires:
  bins: ["curl", "pdftotext"]
---

# Learn Six Minutes English Skill

快速获取BBC 6 Minute English视频字幕并进行英语学习分析。

## 使用场景

当用户需要：
- 获取BBC 6 Minute English视频的官方字幕
- 学习英语词汇和表达
- 分析英语对话结构
- 获取学习建议

## 工作流程

### 1. 获取视频信息
- 从YouTube链接提取视频标题
- 确认是BBC 6 Minute English节目

### 2. 搜索官方字幕
```bash
# 搜索官方页面
web_search('"视频标题" 6 Minute English transcript')

# 提取PDF链接（模式）
https://downloads.bbc.co.uk/learningenglish/features/6min/日期_标题_transcript_.pdf
```

### 3. 下载并转换字幕
```bash
curl -s -o /tmp/transcript.pdf "PDF链接"
pdftotext /tmp/transcript.pdf /tmp/transcript.txt
cat /tmp/transcript.txt
```

### 4. 分析总结
#### 4.1 节目概述
- 标题、日期、主持人
- 主题和主要内容

#### 4.2 经典例句解析
- 提取3-5个典型句子
- 分析语法结构和词汇用法
- 提供学习要点

#### 4.3 关键词汇总结
- 提取6-8个核心词汇
- 提供原文例句和中文解释
- 标注音标和词性

#### 4.4 学习建议
- 听力训练建议
- 口语练习方法
- 词汇记忆技巧

### 5. 输出格式
```
## 📝 学习总结

### 1. 节目基本信息
[标题、日期、主持人]

### 2. 经典例句解析
[例句1] - 解析
[例句2] - 解析

### 3. 关键词汇
1. 单词 - 解释 (原文例句)

### 4. 学习建议
[具体建议]

### 5. 完整文稿
[可折叠的完整英文文稿]
```

## 示例命令

```bash
# 获取字幕
curl -s -o /tmp/transcript.pdf "https://downloads.bbc.co.uk/learningenglish/features/6min/260312_should_we_pay_more_for_chocolate__transcript_.pdf"
pdftotext /tmp/transcript.pdf /tmp/transcript.txt

# 分析内容
cat /tmp/transcript.txt | grep -A2 -B2 "典型句子"
```

## 注意事项

1. **PDF链接格式**：BBC使用固定格式的PDF链接
2. **日期格式**：260312 表示2026年3月12日
3. **标题格式**：下划线连接，全部小写
4. **文件清理**：处理完成后删除临时文件

## 扩展功能

可考虑添加：
1. 音频下载功能
2. 词汇测试生成
3. 对话角色扮演脚本
4. 学习进度跟踪

## 依赖工具

- `curl`: 下载PDF文件
- `pdftotext`: 转换PDF为文本
- `grep`: 文本搜索
- `web_search`: 搜索官方页面

## 错误处理

1. 如果PDF链接失效，尝试搜索替代链接
2. 如果pdftotext不可用，使用其他PDF解析方法
3. 如果找不到官方字幕，提供替代学习资源

---

**技能作者**: Boxi (波西)
**创建日期**: 2026年3月23日
**版本**: 1.0