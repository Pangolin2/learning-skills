# Learning Skills Collection

A collection of learning-related skills for OpenClaw.

## Available Skills

### [learn-six-minutes-english](./learn-six-minutes-english/)
**Description**: Quickly fetch and analyze BBC 6 Minute English video transcripts for English learning.

**Features**:
- Fetch official BBC transcripts from PDF files
- Analyze transcripts for key vocabulary and phrases
- Generate structured learning summaries
- Extract classic sentences for grammar analysis

**Usage**:
```bash
# Get transcript
./get_transcript.sh -t "Video Title" -d YYMMDD

# Analyze transcript
python3 analyze_transcript.py transcript.txt analysis.md
```

## How to Install

1. Clone this repository:
```bash
git clone https://github.com/Pangolin2/learning-skills.git
```

2. Copy the skill folder to your OpenClaw skills directory:
```bash
cp -r learning-skills/learn-six-minutes-english ~/.nvm/versions/node/v22.22.1/lib/node_modules/openclaw/skills/
```

3. Make scripts executable:
```bash
chmod +x ~/.nvm/versions/node/v22.22.1/lib/node_modules/openclaw/skills/learn-six-minutes-english/references/*.sh
```

## Contributing

1. Fork this repository
2. Create a new skill folder
3. Add a SKILL.md file with proper documentation
4. Submit a pull request

## License

MIT License

## Author

Boxi (波西) - Your AI Learning Assistant