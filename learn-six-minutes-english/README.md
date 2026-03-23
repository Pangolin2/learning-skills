# Learn Six Minutes English Skill

快速获取BBC 6 Minute English视频字幕并进行英语学习分析的技能。

## 🎯 功能特点

1. **快速获取字幕**：从BBC官网获取官方PDF字幕
2. **智能分析**：自动提取节目信息、经典例句、关键词汇
3. **学习总结**：生成结构化的学习总结报告
4. **多种格式**：支持文本、Markdown格式输出

## 📁 文件结构

```
learn-six-minutes-english/
├── SKILL.md                    # 技能主文件
├── README.md                   # 使用说明
└── references/                 # 参考脚本
    ├── get_transcript.sh      # 字幕获取脚本
    └── analyze_transcript.py  # 字幕分析脚本
```

## 🚀 快速开始

### 方法1：使用脚本（推荐）

```bash
# 1. 获取字幕
chmod +x references/get_transcript.sh
./references/get_transcript.sh -t "Should we pay more for chocolate" -d 260312

# 2. 分析字幕
python3 references/analyze_transcript.py transcript.txt analysis.md
```

### 方法2：手动流程

```bash
# 1. 下载PDF字幕
curl -s -o transcript.pdf "https://downloads.bbc.co.uk/learningenglish/features/6min/260312_should_we_pay_more_for_chocolate__transcript_.pdf"

# 2. 转换为文本
pdftotext transcript.pdf transcript.txt

# 3. 分析内容
python3 references/analyze_transcript.py transcript.txt
```

## 📋 使用示例

### 示例1：完整流程
```bash
# 获取字幕
./references/get_transcript.sh \
  -t "Should we pay more for chocolate" \
  -d 260312 \
  -o chocolate_transcript.txt

# 分析字幕
python3 references/analyze_transcript.py \
  chocolate_transcript.txt \
  chocolate_analysis.md
```

### 示例2：从YouTube链接开始
```bash
# 自动提取标题（需要YouTube页面可访问）
./references/get_transcript.sh \
  -u "https://www.youtube.com/watch?v=fi3uJy8KsUU" \
  -d 260312
```

## 🔧 参数说明

### get_transcript.sh 参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `-u, --url` | YouTube视频URL | `-u "https://www.youtube.com/watch?v=..."` |
| `-t, --title` | 视频标题 | `-t "Should we pay more for chocolate"` |
| `-d, --date` | 日期（YYMMDD） | `-d 260312` |
| `-o, --output` | 输出文件 | `-o my_transcript.txt` |
| `-k, --keep` | 保留PDF文件 | `-k` |

### analyze_transcript.py 参数
| 参数 | 说明 | 示例 |
|------|------|------|
| 字幕文件 | 要分析的字幕文件 | `transcript.txt` |
| 输出文件 | 分析结果文件（可选） | `analysis.md` |

## 📊 输出内容

### 1. 字幕文件（transcript.txt）
- 完整的英文对话内容
- 词汇表（VOCABULARY部分）
- 节目元数据

### 2. 分析报告（analysis.md）
```
# 📝 BBC 6 Minute English 学习总结

## 1. 节目基本信息
- 标题、主持人、日期

## 2. 经典例句解析
- 3-5个典型句子及分析

## 3. 关键词汇学习
- 6-8个核心词汇及例句

## 4. 学习建议
- 听力、口语、词汇学习建议

## 5. 学习资源
- 相关学习链接
```

## 🎓 学习建议

### 听力训练
1. **盲听**：先不看文稿听音频
2. **跟读**：对照文稿模仿发音
3. **精听**：逐句理解语法和词汇

### 词汇学习
1. **分类记忆**：按主题分类词汇
2. **语境学习**：在句子中理解词汇
3. **定期复习**：使用间隔重复法

### 口语练习
1. **角色扮演**：模仿主持人对话
2. **主题讨论**：围绕节目话题讨论
3. **造句练习**：使用新词汇造句

## ⚙️ 系统要求

### 必需工具
- `curl` - 下载文件
- `pdftotext` - PDF转文本
- `python3` - 运行分析脚本

### 安装依赖
```bash
# Ubuntu/Debian
sudo apt-get install curl poppler-utils python3

# macOS
brew install curl poppler python3
```

## 🔍 故障排除

### 问题1：PDF下载失败
**可能原因**：
- 日期格式错误
- 标题格式不正确
- BBC链接已失效

**解决方案**：
1. 确认日期格式为YYMMDD
2. 确保标题与BBC官网一致
3. 手动访问BBC页面查找正确链接

### 问题2：pdftotext转换失败
**解决方案**：
```bash
# 安装poppler-utils
sudo apt-get install poppler-utils

# 或使用其他PDF工具
sudo apt-get install pdftk
```

### 问题3：分析脚本错误
**解决方案**：
```bash
# 确保使用Python3
python3 --version

# 安装必要模块（如果需要）
pip3 install -r requirements.txt
```

## 📚 学习资源

### BBC官方资源
- [BBC Learning English](https://www.bbc.co.uk/learningenglish)
- [6 Minute English](https://www.bbc.co.uk/learningenglish/english/features/6-minute-english)
- [PDF字幕目录](https://downloads.bbc.co.uk/learningenglish/features/6min/)

### 相关工具
- [YouTube字幕下载工具](https://github.com/ytdl-org/youtube-dl)
- [PDF处理工具](https://poppler.freedesktop.org/)

## 🤝 贡献指南

欢迎提交问题和改进建议！

1. Fork本仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 📄 许可证

MIT License

## 👨‍💻 作者

Boxi (波西) - 你的AI学习助手

---

**最后更新**: 2026年3月23日
**版本**: 1.0.0