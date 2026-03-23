#!/usr/bin/env python3
"""
analyze_transcript.py - BBC 6 Minute English 字幕分析工具

功能：
1. 提取节目基本信息
2. 分析经典例句
3. 提取关键词汇
4. 生成学习总结
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class TranscriptAnalyzer:
    def __init__(self, transcript_path: str):
        self.transcript_path = transcript_path
        self.content = ""
        self.lines = []
        self.load_transcript()
        
    def load_transcript(self):
        """加载字幕文件"""
        try:
            with open(self.transcript_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.lines = self.content.split('\n')
        except FileNotFoundError:
            print(f"错误：文件不存在 - {self.transcript_path}")
            sys.exit(1)
        except Exception as e:
            print(f"错误：读取文件失败 - {e}")
            sys.exit(1)
    
    def extract_basic_info(self) -> Dict:
        """提取节目基本信息"""
        info = {
            'title': '',
            'date': '',
            'hosts': [],
            'vocabulary': []
        }
        
        # 提取标题（通常是第二行）
        for i, line in enumerate(self.lines):
            if '6 Minute English' in line and i + 1 < len(self.lines):
                # 下一行通常是标题
                next_line = self.lines[i + 1].strip()
                if next_line and not next_line.startswith('This is'):
                    info['title'] = next_line
                    break
        
        # 提取主持人
        host_patterns = [r'^I\'m (\w+)\.$', r'^And I\'m (\w+)\.$']
        for line in self.lines:
            for pattern in host_patterns:
                match = re.match(pattern, line.strip())
                if match:
                    host = match.group(1)
                    if host not in info['hosts']:
                        info['hosts'].append(host)
        
        # 提取词汇表
        vocab_section = False
        for line in self.lines:
            if 'VOCABULARY' in line:
                vocab_section = True
                continue
            if vocab_section and line.strip():
                # 假设词汇格式：单词 - 解释
                if '-' in line:
                    parts = line.split('-', 1)
                    if len(parts) == 2:
                        word = parts[0].strip()
                        definition = parts[1].strip()
                        info['vocabulary'].append((word, definition))
        
        return info
    
    def find_classic_sentences(self, count: int = 5) -> List[Tuple[str, str]]:
        """查找经典例句"""
        sentences = []
        
        # 寻找包含关键词的句子
        keywords = ['because', 'that means', 'which is', 'in other words', 'for example']
        
        for i, line in enumerate(self.lines):
            line = line.strip()
            if not line or line.startswith('BBC LEARNING ENGLISH') or line.startswith('6 Minute English'):
                continue
            
            # 跳过主持人名字行
            if line in ['Neil', 'Becca'] or re.match(r'^[A-Z][a-z]+$', line):
                continue
            
            # 检查是否包含关键词
            for keyword in keywords:
                if keyword in line.lower() and len(line) > 20:
                    # 获取上下文（前一行和后一行）
                    context = ""
                    if i > 0:
                        prev_line = self.lines[i-1].strip()
                        if prev_line and not prev_line.startswith('BBC'):
                            context += f"前文: {prev_line}\n"
                    
                    context += f"例句: {line}\n"
                    
                    if i + 1 < len(self.lines):
                        next_line = self.lines[i+1].strip()
                        if next_line and not next_line.startswith('BBC'):
                            context += f"后文: {next_line}"
                    
                    sentences.append((line, context))
                    break
            
            if len(sentences) >= count:
                break
        
        return sentences
    
    def extract_key_words(self, count: int = 8) -> List[Dict]:
        """提取关键词汇"""
        words = []
        
        # 从词汇表获取
        info = self.extract_basic_info()
        for word, definition in info['vocabulary'][:count]:
            # 在文本中查找例句
            example = self.find_word_example(word)
            words.append({
                'word': word,
                'definition': definition,
                'example': example
            })
        
        return words
    
    def find_word_example(self, word: str) -> str:
        """在文本中查找单词的例句"""
        word_lower = word.lower()
        
        for line in self.lines:
            line_lower = line.lower()
            if word_lower in line_lower and len(line) > 10:
                # 确保不是词汇表行
                if 'VOCABULARY' not in line and not line.startswith(word):
                    return line.strip()
        
        return ""
    
    def generate_summary(self) -> str:
        """生成学习总结"""
        info = self.extract_basic_info()
        sentences = self.find_classic_sentences(3)
        words = self.extract_key_words(6)
        
        summary = []
        summary.append("# 📝 BBC 6 Minute English 学习总结")
        summary.append("")
        
        # 基本信息
        summary.append("## 1. 节目基本信息")
        summary.append(f"- **标题**: {info['title']}")
        summary.append(f"- **主持人**: {', '.join(info['hosts'])}")
        summary.append(f"- **核心词汇**: {len(info['vocabulary'])} 个")
        summary.append("")
        
        # 经典例句
        summary.append("## 2. 经典例句解析")
        for i, (sentence, context) in enumerate(sentences, 1):
            summary.append(f"### 例句{i}:")
            summary.append(f"```")
            summary.append(context)
            summary.append("```")
            summary.append("**学习要点**:")
            summary.append("- 分析句子结构")
            summary.append("- 学习地道表达")
            summary.append("")
        
        # 关键词汇
        summary.append("## 3. 关键词汇学习")
        for word_info in words:
            summary.append(f"### {word_info['word']}")
            summary.append(f"- **解释**: {word_info['definition']}")
            if word_info['example']:
                summary.append(f"- **例句**: {word_info['example']}")
            summary.append("")
        
        # 学习建议
        summary.append("## 4. 学习建议")
        summary.append("1. **听力训练**: 先听音频，再对照文稿")
        summary.append("2. **跟读练习**: 模仿主持人的发音和语调")
        summary.append("3. **词汇记忆**: 重点记忆6个核心词汇")
        summary.append("4. **口语应用**: 使用新词汇造句")
        summary.append("5. **主题讨论**: 围绕节目主题进行对话练习")
        summary.append("")
        
        # 资源链接
        summary.append("## 5. 学习资源")
        summary.append("- BBC Learning English官网: https://www.bbc.co.uk/learningenglish")
        summary.append("- 6 Minute English页面: https://www.bbc.co.uk/learningenglish/english/features/6-minute-english")
        summary.append("- 音频下载: 官网提供MP3下载")
        
        return '\n'.join(summary)
    
    def save_analysis(self, output_path: str):
        """保存分析结果"""
        summary = self.generate_summary()
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"✅ 分析结果已保存到: {output_path}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python analyze_transcript.py <字幕文件> [输出文件]")
        print("示例: python analyze_transcript.py transcript.txt analysis.md")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "analysis.md"
    
    # 检查文件是否存在
    if not Path(transcript_file).exists():
        print(f"错误：文件不存在 - {transcript_file}")
        sys.exit(1)
    
    print(f"📖 正在分析字幕文件: {transcript_file}")
    
    # 创建分析器
    analyzer = TranscriptAnalyzer(transcript_file)
    
    # 显示基本信息
    info = analyzer.extract_basic_info()
    print(f"\n📊 节目信息:")
    print(f"  标题: {info['title']}")
    print(f"  主持人: {', '.join(info['hosts'])}")
    print(f"  词汇数量: {len(info['vocabulary'])}")
    
    # 生成并保存分析
    analyzer.save_analysis(output_file)
    
    # 显示预览
    print(f"\n📋 分析预览:")
    with open(output_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < 15:  # 显示前15行
                print(line.rstrip())
            else:
                print("...")
                break

if __name__ == "__main__":
    main()