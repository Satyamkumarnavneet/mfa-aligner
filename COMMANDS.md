# MFA Pipeline - Quick Command Reference

## 🚀 Essential Commands

### Setup (One-time)
```bash
./setup_mfa.sh          # Create environment and install MFA
conda activate mfa      # Activate the environment
```

### Main Pipeline
```bash
./run_all.sh           # Run complete pipeline (setup → alignment → metrics)
```

---

## 📂 Individual Operations

### Environment
```bash
conda activate mfa                    # Activate MFA environment
conda deactivate                      # Deactivate environment
mfa version                          # Check MFA version
```

### Audio Preprocessing
```bash
./prepare_audio.sh                   # Convert audio to MFA format
./scripts/prepare_audio.sh           # Same (organized location)
```

### Validation
```bash
./scripts/validate_corpus.sh         # Validate corpus only (no alignment)
```

### Metrics & Analysis
```bash
# Basic metrics (run during pipeline)
python3 python/metrics.py ./corpus ./aligned_output ./logs/validate_*.txt

# Detailed TextGrid analysis
python3 python/analyze_textgrids.py ./aligned_output
```

### Cleanup
```bash
./scripts/clean_workspace.sh         # Remove generated files
```

---

## 🔧 Advanced MFA Commands

### Model Management
```bash
mfa model list                       # List available models
mfa model download dictionary english_us_arpa
mfa model download acoustic english_us_arpa
```

### Manual Alignment Steps
```bash
# Validate
mfa validate ./corpus english_us_arpa

# Align
mfa align ./corpus english_us_arpa english_us_arpa ./aligned_output -j 4 --clean
```

### G2P (Grapheme-to-Phoneme) for OOV words
```bash
mfa g2p english_us_arpa ./corpus ./output_dict.txt
```

---

## 📊 Checking Status

### View Files
```bash
ls -lh wav/                          # Input audio files
ls -lh transcripts/                  # Input transcripts
ls -lh corpus/                       # Prepared corpus
ls -lh aligned_output/               # TextGrid outputs
ls -lh logs/                         # Pipeline logs
```

### Check Logs
```bash
cat logs/pipeline_*.log              # Full pipeline log
cat logs/validate_*.txt              # Validation results
cat logs/align_*.txt                 # Alignment log
tail -f logs/pipeline_*.log          # Follow log in real-time
```

### File Counts
```bash
ls wav/*.wav | wc -l                 # Count audio files
ls transcripts/*.{txt,TXT} | wc -l   # Count transcripts
ls aligned_output/*.TextGrid | wc -l # Count TextGrids
```

---

## 🐍 Python Tools

### Metrics Collection
```bash
### Metrics Collection

Collect and display alignment metrics:

```bash
python3 tools/metrics.py <corpus_dir> <output_dir> <validate_log>

# Example
python3 tools/metrics.py corpus/ aligned_output/ logs/validate.txt
```
```

### TextGrid Analysis
```bash
### TextGrid Analysis

Analyze generated TextGrid files:

```bash
python3 tools/analyze_textgrids.py <textgrid_directory>

# Example
python3 tools/analyze_textgrids.py aligned_output/
```
```

---

## 🗑️ Cleanup Operations

### Clean Generated Files Only
```bash
./scripts/clean_workspace.sh         # Interactive cleanup
```

### Manual Cleanup
```bash
rm -rf corpus/                       # Remove prepared corpus
rm -rf aligned_output/               # Remove TextGrid outputs
rm -rf logs/                         # Remove logs
rm -rf wav_processed/                # Remove processed audio
rm -f aligned_output_*.zip           # Remove archives
```

### Start Fresh
```bash
./scripts/clean_workspace.sh         # Clean all generated files
./run_all.sh                         # Run pipeline again
```

---

## 📖 Documentation

### View Documentation
```bash
cat README.md                        # Full documentation
cat QUICKSTART.md                    # Quick start guide
cat STRUCTURE.md                     # Project structure
cat SETUP_COMPLETE.txt               # Setup summary
```

### Open in Editor
```bash
open README.md                       # macOS
code README.md                       # VS Code
```

---

## 🔍 Troubleshooting Commands

### Check MFA Installation
```bash
which mfa                            # Find MFA location
mfa version                          # Check version
mfa --help                           # View help

# If you see "No module named '_kalpy'" error:
./FIX_KALPY_ERROR.sh                # Run automatic fix
```

### Check Python Environment
```bash
which python3                        # Find Python
python3 --version                    # Check version
conda list | grep montreal           # Check MFA installation
```

### Check Permissions
```bash
ls -l *.sh scripts/*.sh              # Check if executable
chmod +x *.sh scripts/*.sh           # Make executable
```

### Check File Formats
```bash
file wav/*.wav                       # Check audio format
file transcripts/*                   # Check transcript format
```

---

## 📦 Packaging

### Create Archive
```bash
# Manual archive creation
zip -r my_alignment.zip aligned_output/ logs/

# Include everything
zip -r full_project.zip . -x ".*" -x "*/__pycache__/*"
```

### Extract Archive
```bash
unzip aligned_output_*.zip
```

---

## ⚙️ Configuration

### View Current Settings
```bash
grep "^MFA_" run_all.sh              # View MFA settings
grep "^WAV_DIR" run_all.sh           # View directory settings
```

### Edit Configuration
```bash
nano run_all.sh                      # Edit main script
code run_all.sh                      # Open in VS Code
```

---

## 🎯 Common Workflows

### First Run
```bash
./setup_mfa.sh
conda activate mfa
./run_all.sh
```

### Re-run After Changes
```bash
conda activate mfa
./scripts/clean_workspace.sh
./run_all.sh
```

### Validate Before Alignment
```bash
conda activate mfa
./scripts/validate_corpus.sh
# Review output, then:
./run_all.sh
```

### Preprocess + Align
```bash
conda activate mfa
./prepare_audio.sh
# Edit run_all.sh to use wav_processed/
./run_all.sh
```

---

## 📊 Performance Tuning

### Adjust CPU Cores
```bash
# Edit run_all.sh, change:
mfa align ... -j 8     # Use 8 cores instead of 4
```

### Check System Resources
```bash
top                    # View CPU/memory usage
htop                   # Better top (if installed)
```

---

## 🔗 Quick Links

| Command | Description |
|---------|-------------|
| `./setup_mfa.sh` | Setup environment |
| `./run_all.sh` | Run pipeline |
| `conda activate mfa` | Activate environment |
| `./scripts/validate_corpus.sh` | Validate only |
| `./scripts/clean_workspace.sh` | Cleanup |
| `python3 python/analyze_textgrids.py ./aligned_output` | Analyze results |

---

## 📞 Getting Help

```bash
mfa --help                           # MFA help
mfa align --help                     # Alignment help
mfa validate --help                  # Validation help
```

---
