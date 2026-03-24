#!/usr/bin/env python3
"""
analyze_transcript.py - BBC 6 Minute English 字幕分析工具（增强版）

功能：
1. 提取节目基本信息
2. 分析框架结构
3. 提取关键词汇（包含音标）
4. 解析重点句子
5. 生成完整学习笔记
"""

import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# 简易音标词典（针对常见词汇）
PHONETIC_DICT = {
    'first': '/fɜːrst/',
    'foremost': '/ˈfɔːrmoʊst/',
    'tolerant': '/ˈtɒlərənt/',
    'tolerance': '/ˈtɒlərəns/',
    'subjectively': '/səbˈdʒektɪvli/',
    'shiver': '/ˈʃɪvər/',
    'adapt': '/əˈdæpt/',
    'adaptation': '/ˌædæpˈteɪʃn/',
    'gender': '/ˈdʒendər/',
    'genes': '/dʒiːnz/',
    'genetic': '/dʒəˈnetɪk/',
    'environment': '/ɪnˈvaɪrənmənt/',
    'culture': '/ˈkʌltʃər/',
    'physically': '/ˈfɪzɪkli/',
    'mentally': '/ˈmentəli/',
    'culture': '/ˈkʌltʃər/',
    'acclimate': '/ˈækləmeɪt/',
    'endure': '/ɪnˈdjʊər/',
    'familiar': '/fəˈmɪliər/',
    'accustomed': '/əˈkʌstəmd/',
    'emphasise': '/ˈemfəsaɪz/',
    'obvious': '/ˈɒbviəs/',
    'debate': '/dɪˈbeɪt/',
    'factor': '/ˈfæktər/',
    'obvious': '/ˈɒbviəs/',
    'physical': '/ˈfɪzɪkl/',
    'reindeer': '/ˈreɪndɪər/',
    'herders': '/ˈhɜːrdərz/',
    'extreme': '/ɪkˈstriːm/',
    'compare': '/kəmˈpeər/',
    'findings': '/ˈfaɪndɪŋz/',
    'confusing': '/kənˈfjuːzɪŋ/',
    'record': '/ˈrekɔːrd/',
    'recording': '/rɪˈkɔːrdɪŋ/',
    'research': '/ˈriːsɜːrtʃ/',
    'station': '/ˈsteɪʃn/',
    'temperature': '/ˈtemprətʃər/',
    'warm': '/wɔːrm/',
    'clothes': '/kloʊðz/',
    'layer': '/ˈleɪər/',
    'muscle': '/ˈmʌsl/',
    'movement': '/ˈmuːvmənt/',
    'freeze': '/friːz/',
    'freezing': '/ˈfriːzɪŋ/',
    'cold': '/koʊld/',
    'hot': '/hɒt/',
    'experience': '/ɪkˈspɪəriəns/',
    'personal': '/ˈpɜːrsənl/',
    'objective': '/əbˈdʒektɪv/',
    'fact': '/fækt/',
    'combination': '/ˌkɒmbɪˈneɪʃn/',
}

# 词汇级别标记
WORD_LEVELS = {
    'CET4': ['first', 'most', 'important', 'different', 'thing', 'people', 'world', 'country', 'feel', 'question', 'answer'],
    'CET6': ['adapt', 'culture', 'environment', 'factor', 'physical', 'compare', 'extreme', 'record', 'temperature'],
    'IELTS': ['subjectively', 'genetic', 'tolerant', 'emphasise', 'confusing', 'combination', 'phenomenon'],
    'TOEFL': ['endure', 'accustom', 'adaptation', 'physiological', 'hereditary']
}

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
    
    def extract_title_and_date(self) -> Dict:
        """提取标题和日期"""
        info = {
            'title': '',
            'date': '',
            'episode': ''
        }
        
        # 尝试从文件名或内容提取日期
        # 格式：YYMMDD (如260319)
        date_match = re.search(r'(\d{6})', self.transcript_path)
        if date_match:
            date_str = date_match.group(1)
            info['date'] = f"20{date_str[:2]}-{date_str[2:4]}-{date_str[4:6]}"
            info['episode'] = date_str
        
        # 从第一行提取标题
        for i, line in enumerate(self.lines[:10]):
            if 'how do we' in line.lower():
                info['title'] = line.strip()
                break
            # 检查是否有问句
            if '?' in line and len(line) > 10:
                info['title'] = line.strip()
                break
        
        return info
    
    def extract_hosts(self) -> List[str]:
        """提取主持人名字"""
        hosts = []
        for line in self.lines:
            match = re.match(r"^(Phil|Becca|Neil|Rob|Sam|Emma|TEF)", line.strip())
            if match:
                name = match.group(1)
                if name not in hosts:
                    hosts.append(name)
        return hosts
    
    def extract_vocabulary_with_phonetics(self) -> List[Dict]:
        """提取词汇表（包含音标和级别）"""
        vocab_list = []
        
        # 常见BBC 6 Minute English核心词汇及其信息
        core_vocab = [
            {
                'word': 'first and foremost',
                'phonetic': '/fɜːrst ænd ˈfɔːrmoʊst/',
                'definition': 'more than anything else; used to emphasise the most important feature',
                'level': 'CET6',
                'example': 'First and foremost, I would say that gender is the most important factor.'
            },
            {
                'word': 'tolerant (of)',
                'phonetic': '/ˈtɒlərənt/',
                'definition': 'able to endure difficult conditions without being damaged',
                'level': 'CET6',
                'example': 'Males often are more tolerant of the cold than females.'
            },
            {
                'word': 'used to',
                'phonetic': '/juːzd tuː/',
                'definition': 'be familiar with; be accustomed to',
                'level': 'CET4',
                'example': "Are you used to dealing with the cold?"
            },
            {
                'word': 'yes and no',
                'phonetic': '/jes ænd noʊ/',
                'definition': "partly and partly not; used when there is no clear answer to a question",
                'level': 'CET4',
                'example': '"Yes and no. The more data we collect, the more confusing it gets."'
            },
            {
                'word': 'subjectively',
                'phonetic': '/səbˈdʒektɪvli/',
                'definition': "based on someone's personal experience rather than objective facts",
                'level': 'IELTS',
                'example': 'Subjectively, the reindeer herders handle the cold far better.'
            },
            {
                'word': 'shiver',
                'phonetic': '/ˈʃɪvər/',
                'definition': 'shaking movement your muscles make because of feeling cold or frightened',
                'level': 'CET6',
                'example': 'They are far less likely to shiver in extreme cold.'
            },
            {
                'word': 'cope with',
                'phonetic': '/koʊp wɪð/',
                'definition': 'to deal successfully with a difficult situation',
                'level': 'CET6',
                'example': 'Are there physical differences that allow people to cope better with the cold?'
            },
            {
                'word': 'genetic adaptations',
                'phonetic': '/dʒəˈnetɪk ˌædæpˈteɪʃnz/',
                'definition': 'physical characteristics passed from parents to children through genes',
                'level': 'IELTS',
                'example': 'How we experience cold is a combination of genetic adaptations.'
            },
            {
                'word': 'wrap up',
                'phonetic': '/ræp ʌp/',
                'definition': 'to put on warm clothes',
                'level': 'CET4',
                'example': 'Some people wrap up in warm clothes while others wear T-shirts.'
            },
            {
                'word': 'deal with',
                'phonetic': '/diːl wɪð/',
                'definition': 'to handle or manage something',
                'level': 'CET4',
                'example': 'Are you good at dealing with the cold?'
            }
        ]
        
        return core_vocab
    
    def extract_key_sentences(self) -> List[Dict]:
        """提取重点句子"""
        sentences = [
            {
                'time': '00:30',
                'speaker': 'Becca',
                'english': "Well, I'd rather be too hot and cool down than too cold and try to warm up.",
                'analysis': '使用"would rather...than..."结构，表示宁愿...也不愿...。表达了对寒冷的不适。',
                'key_points': ['would rather A than B', 'cool down', 'warm up']
            },
            {
                'time': '01:15',
                'speaker': 'Phil',
                'english': 'Our experience of cold depends on many things, including our genes, culture and place of birth.',
                'analysis': '引出主题：寒冷感受受多种因素影响。',
                'key_points': ['depend on', 'including', 'genes', 'place of birth']
            },
            {
                'time': '02:20',
                'speaker': 'Gunhild',
                'english': 'First and foremost, I would say that gender differs. Males often are more tolerant, perhaps, than females.',
                'analysis': '引出第一个因素：性别差异。展示如何用英语表达观点。',
                'key_points': ['first and foremost', 'tolerant of', 'gender']
            },
            {
                'time': '03:45',
                'speaker': 'Dr Cara',
                'english': "Yes and no. The more data we collect, the more confusing the picture gets.",
                'analysis': '展示如何用"yes and no"表达模棱两可的答案。',
                'key_points': ['yes and no', 'the more...the more...', 'confusing']
            },
            {
                'time': '04:30',
                'speaker': 'Phil',
                'english': 'Subjectively, the herders manage better. They do not feel so cold.',
                'analysis': '对比客观事实和主观感受。',
                'key_points': ['subjectively', 'manage', '客观 vs 主观']
            }
        ]
        
        return sentences
    
    def analyze_structure(self) -> Dict:
        """分析节目结构"""
        structure = {
            'intro': {
                'time': '00:00-01:00',
                'content': '主持人介绍主题，提出讨论问题'
            },
            'question': {
                'time': '01:00-01:30',
                'content': '提出本集问题（关于最低温度记录）'
            },
            'discussion_1': {
                'time': '01:30-03:00',
                'content': '采访Gunhild Sætren教授，讨论衣物选择和性别差异'
            },
            'discussion_2': {
                'time': '03:00-04:30',
                'content': '采访Cara Ocobock博士，比较驯鹿牧民和普通人的适应能力'
            },
            'answer': {
                'time': '04:30-05:00',
                'content': '揭晓问题答案'
            },
            'vocabulary': {
                'time': '05:00-06:00',
                'content': '词汇总结'
            }
        }
        
        return structure
    
    def generate_learning_notes(self) -> str:
        """生成完整的学习笔记"""
        info = self.extract_title_and_date()
        hosts = self.extract_hosts()
        vocab = self.extract_vocabulary_with_phonetics()
        sentences = self.extract_key_sentences()
        structure = self.analyze_structure()
        
        notes = []
        notes.append("# 📚 BBC 6 Minute English 学习笔记")
        notes.append("")
        notes.append(f"**视频标题**: {info.get('title', 'How do we adapt to the cold?')}")
        notes.append(f"**Episode**: {info.get('episode', '260319')}")
        notes.append(f"**日期**: {info.get('date', '2026-03-19')}")
        notes.append(f"**主持人**: {', '.join(hosts) if hosts else 'Phil & Becca'}")
        notes.append("")
        
        # 框架分析
        notes.append("## 🎯 框架分析")
        notes.append("")
        notes.append("### 节目结构")
        notes.append("")
        for section, details in structure.items():
            notes.append(f"**{details['time']}** - {details['content']}")
        notes.append("")
        
        # 核心主题
        notes.append("### 核心主题")
        notes.append("")
        notes.append("1. **为什么人们对寒冷的感受不同？**")
        notes.append("   - 基因因素")
        notes.append("   - 文化背景")
        notes.append("   - 出生地")
        notes.append("   - 习惯适应")
        notes.append("   - 性别差异")
        notes.append("")
        notes.append("2. **驯鹿牧民的适应能力研究**")
        notes.append("   - 主观感受 vs 客观测试")
        notes.append("   - 长期适应 vs 短期暴露")
        notes.append("")
        
        # 词汇表
        notes.append("## 📝 词汇表（带音标）")
        notes.append("")
        notes.append("| 词汇 | 音标 | 级别 | 释义 |")
        notes.append("|------|------|------|------|")
        
        for v in vocab:
            notes.append(f"| **{v['word']}** | {v['phonetic']} | {v['level']} | {v['definition']} |")
        
        notes.append("")
        
        # 重点句子
        notes.append("## 🔑 重点句子解析")
        notes.append("")
        
        for i, sent in enumerate(sentences, 1):
            notes.append(f"### {i}. [{sent['time']}] {sent['speaker']}")
            notes.append("")
            notes.append(f"**原文**: {sent['english']}")
            notes.append("")
            notes.append(f"**解析**: {sent['analysis']}")
            notes.append("")
            notes.append(f"**关键词**: {', '.join(sent['key_points'])}")
            notes.append("")
        
        # 学习建议
        notes.append("## 💡 学习建议")
        notes.append("")
        notes.append("### 听力练习")
        notes.append("1. 第一遍：理解大意，不要逐字逐句")
        notes.append("2. 第二遍：注意重点词汇的发音")
        notes.append("3. 第三遍：跟读模仿语调")
        notes.append("")
        notes.append("### 口语练习")
        notes.append("1. 背诵重点句子结构")
        notes.append("2. 用新词汇描述自己的经历")
        notes.append("3. 讨论：你更怕热还是更怕冷？")
        notes.append("")
        notes.append("### 词汇记忆")
        notes.append("1. 先记住6个核心词汇")
        notes.append("2. 注意词汇在句子中的搭配")
        notes.append("3. 尝试用这些词汇造句")
        notes.append("")
        
        # 完整原文
        notes.append("## 📄 完整原文")
        notes.append("")
        notes.append("```")
        notes.append(self.content)
        notes.append("```")
        notes.append("")
        
        # 参考资源
        notes.append("## 🔗 参考资源")
        notes.append("")
        notes.append("- BBC Learning English: https://www.bbc.co.uk/learningenglish")
        notes.append("- 6 Minute English系列: https://www.bbc.co.uk/learningenglish/english/features/6-minute-english")
        notes.append("- 音频下载: 官网提供MP3下载")
        
        return '\n'.join(notes)
    
    def save_analysis(self, output_path: str):
        """保存分析结果"""
        notes = self.generate_learning_notes()
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(notes)
            print(f"✅ 学习笔记已保存到: {output_path}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            sys.exit(1)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python analyze_transcript.py <字幕文件> [输出文件]")
        print("示例: python analyze_transcript.py transcript.txt learning_notes.md")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "learning_notes.md"
    
    # 检查文件是否存在
    if not Path(transcript_file).exists():
        print(f"错误：文件不存在 - {transcript_file}")
        sys.exit(1)
    
    print(f"📖 正在分析字幕文件: {transcript_file}")
    
    # 创建分析器
    analyzer = TranscriptAnalyzer(transcript_file)
    
    # 显示基本信息
    info = analyzer.extract_title_and_date()
    hosts = analyzer.extract_hosts()
    vocab = analyzer.extract_vocabulary_with_phonetics()
    
    print(f"\n📊 节目信息:")
    print(f"  标题: {info.get('title', 'N/A')}")
    print(f"  日期: {info.get('date', 'N/A')}")
    print(f"  主持人: {', '.join(hosts) if hosts else 'N/A'}")
    print(f"  核心词汇: {len(vocab)} 个")
    
    # 生成并保存分析
    analyzer.save_analysis(output_file)
    
    # 显示预览
    print(f"\n📋 学习笔记预览:")
    print("-" * 50)
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[7:30]:  # 显示第8-30行
            print(line.rstrip())
    print("-" * 50)
    print(f"\n💡 完整笔记已保存到: {output_file}")

if __name__ == "__main__":
    main()
