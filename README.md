# MFA Forced Alignment Pipeline

A complete automated pipeline for forced alignment of audio and transcripts using the Montreal Forced Aligner (MFA).

## Quick Start

**Clone the repository:**
```bash
git clone https://github.com/Satyamkumarnavneet/mfa-aligner.git
cd mfa-aligner
```

**Install and run:**

*macOS/Linux:*
```bash
# 1. Setup environment
./scripts/setup_mfa.sh

# 2. Activate environment  
conda activate mfa

# 3. Run pipeline
./run_all.sh
```

*Windows (PowerShell):*
```powershell
# 1. Setup environment
conda create -n mfa python=3.10 -y
conda activate mfa
conda install -c conda-forge montreal-forced-aligner -y

# 2. Run alignment manually (shell scripts require WSL or Git Bash on Windows)
mfa validate corpus/ english_us_arpa english_us_arpa
mfa align corpus/ english_us_arpa english_us_arpa aligned_output/
```
That's it! Your TextGrids will be in `aligned_output/`

## Overview

This pipeline automates the entire process of:
1. Installing and setting up the MFA environment
2. Preparing audio and transcript datasets
3. Validating corpus data
4. Running forced alignment
5. Generating TextGrid outputs for phonetic analysis
6. Computing alignment metrics and statistics

## Features

- **Automated Setup**: One-command environment configuration
- **Audio Preprocessing**: Optional audio conversion to MFA requirements
- **Validation**: Pre-alignment corpus validation with OOV detection
- **Parallel Processing**: Multi-core alignment support
- **Comprehensive Metrics**: Detailed statistics and coverage reports
- **Logging**: Complete pipeline logging for debugging
- **Clean Output**: No emojis in code output for better compatibility

## Project Structure

```
mfa-aligner/
├── README.md                     # This documentation
├── QUICKSTART.md                 # Quick start guide
├── QUICK_REFERENCE.md            # Quick reference for common tasks
├── COMMANDS.md                   # Detailed command reference
├── LICENSE                       # License information
├── Assignment1.pdf               # Assignment description
│
├── run_all.sh                    # Main pipeline script (START HERE)
│
├── scripts/                      # Utility shell scripts
│   ├── setup_mfa.sh             # MFA environment setup
│   ├── prepare_audio.sh         # Audio preprocessing
│   ├── validate_corpus.sh       # Corpus validation only
│   └── clean_workspace.sh       # Cleanup generated files
│
├── tools/                        # Analysis Python scripts
│   ├── metrics.py               # Alignment metrics collection
│   ├── analyze_textgrids.py     # TextGrid statistics
│   └── analyze_oov.py           # OOV word analysis
│
├── wav/                          # INPUT: Audio files (*.wav)
├── transcripts/                  # INPUT: Transcript files (*.txt, *.TXT, *.lab)
│
├── corpus/                       # Auto-generated: Prepared corpus
├── aligned_output/               # Auto-generated: TextGrid outputs
└── logs/                         # Auto-generated: Pipeline logs
```

## Installation Steps

### Step 1: Install Prerequisites

**1.1 Install Conda (if not already installed)**

macOS:
```bash
# Using Homebrew
brew install miniconda

# Or download from
# https://docs.conda.io/en/latest/miniconda.html
```

Linux:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Windows:
```powershell
# Download and install Miniconda from:
# https://docs.conda.io/en/latest/miniconda.html

# Or use winget (Windows Package Manager)
winget install Anaconda.Miniconda3
```

**1.2 Install FFmpeg (optional, for audio preprocessing)**

macOS:
```bash
brew install ffmpeg
```

Linux:
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

Windows:
```powershell
# Using chocolatey
choco install ffmpeg

# Or using winget
winget install Gyan.FFmpeg

# Or download from https://ffmpeg.org/download.html
```

### Step 2: Install MFA Environment

Navigate to the project directory and run the setup script:

**macOS/Linux:**
```bash
cd mfa-aligner
./scripts/setup_mfa.sh
```

**Windows (PowerShell):**
```powershell
cd mfa-aligner
# Run the commands manually since shell scripts don't run natively on Windows
conda create -n mfa python=3.10 -y
conda activate mfa
conda install -c conda-forge montreal-forced-aligner -y
```

This script will:
- Create a new conda environment named `mfa`
- Install Python 3.10
- Install Montreal Forced Aligner from conda-forge
- Install all required dependencies

**Verify installation:**
```bash
conda activate mfa
mfa version
```

Expected output:
```
montreal-forced-aligner 3.x.x
```

## Dataset Preparation

### Step 3: Prepare Your Audio Files

Place your audio files in the `wav/` directory.

**Audio Requirements:**
- Format: WAV (PCM)
- Sample Rate: 16kHz (recommended)
- Channels: Mono (recommended)
- Encoding: PCM 16-bit

**Example:**
```bash
wav/
├── F2BJRLP1.wav
├── F2BJRLP2.wav
└── F2BJRLP3.wav
```

**If your audio doesn't meet requirements, preprocess it:**
```bash
conda activate mfa
./scripts/prepare_audio.sh
```

This converts all WAV files to mono, 16kHz, PCM 16-bit format and saves to `wav_processed/`

### Step 4: Prepare Your Transcripts

Place transcript files in the `transcripts/` directory.

**Transcript Requirements:**
- Format: Plain text (`.txt`, `.TXT`, or `.lab`)
- Encoding: UTF-8
- Content: One transcript per file
- Naming: Must match audio filename (case-insensitive)

**Example:**
```bash
transcripts/
├── F2BJRLP1.TXT
├── F2BJRLP2.TXT
└── F2BJRLP3.TXT
```

**File naming convention:**
```
wav/F2BJRLP1.wav  <-->  transcripts/F2BJRLP1.TXT
wav/F2BJRLP2.wav  <-->  transcripts/F2BJRLP2.txt
wav/F2BJRLP3.wav  <-->  transcripts/F2BJRLP3.lab
```

## Running the Alignment

### Step 5: Run the Complete Pipeline

Activate the conda environment and run the main script:

```bash
conda activate mfa
./run_all.sh
```

**What happens during execution:**

1. **Environment Check** - Verifies MFA installation
2. **Directory Setup** - Creates `corpus/`, `aligned_output/`, `logs/`
3. **File Copying** - Copies audio and transcripts to `corpus/`
4. **Normalization** - Converts all transcripts to `.lab` extension
5. **Model Download** - Downloads acoustic model and dictionary (if needed)
6. **Validation** - Checks corpus for errors and OOV words
7. **Alignment** - Runs forced alignment (this may take several minutes)
8. **Metrics** - Displays alignment statistics
9. **Packaging** - Creates `aligned_output_<timestamp>.zip`

**Expected output:**
```
======================================================================
  MFA Forced Alignment Pipeline - START
======================================================================

Working Directory: /path/to/mfa-aligner
...
[Progress bars and status messages]
...

======================================================================
  MFA ALIGNMENT METRICS REPORT
======================================================================

INPUT FILES
--------------------------------------------------------------------------------
  WAV files (audio):           6
  LAB files (transcripts):     6

OUTPUT FILES
--------------------------------------------------------------------------------
  TextGrid files generated:    6
  Alignment coverage:       100.0%

VALIDATION RESULTS
--------------------------------------------------------------------------------
  Validation log:           logs/validate_20251105_170146.txt
  OOV occurrences:             4

======================================================================
  SUMMARY
======================================================================
  Alignment completed successfully!
     6 TextGrid file(s) generated
  All audio files were aligned
...
```

### Step 6: Review Results

**TextGrid files** (alignment outputs):
```bash
ls -lh aligned_output/
# F2BJRLP1.TextGrid
# F2BJRLP2.TextGrid
# F2BJRLP3.TextGrid
# ...
```

**Open in Praat** for visual inspection:
1. Download Praat: https://www.fon.hum.uva.nl/praat/
2. Open TextGrid file along with corresponding WAV file
3. Inspect word and phone-level alignments

**View detailed metrics:**
```bash
python3 tools/analyze_textgrids.py aligned_output/
```

**Analyze OOV words:**
```bash
python3 tools/analyze_oov.py logs/validate_*.txt
```

## Example Commands

### Complete Workflow Example

```bash
# 1. One-time setup
./scripts/setup_mfa.sh
conda activate mfa

# 2. Verify your data is ready
ls wav/          # Should show your .wav files
ls transcripts/  # Should show your .txt/.TXT/.lab files

# 3. (Optional) Preprocess audio if needed
./scripts/prepare_audio.sh

# 4. Run alignment
./run_all.sh

# 5. Analyze results
python3 tools/analyze_textgrids.py aligned_output/
python3 tools/analyze_oov.py logs/validate_*.txt

# 6. View in Praat
# Open Praat → Read → Read from file → aligned_output/F2BJRLP1.TextGrid
# Then: Read → Read from file → wav/F2BJRLP1.wav
```

### Individual Step Examples

**Validate corpus only:**
```bash
conda activate mfa
./scripts/validate_corpus.sh
```

**Analyze existing TextGrids:**
```bash
python3 tools/analyze_textgrids.py aligned_output/
```

**Clean workspace:**
```bash
./scripts/clean_workspace.sh
```

**Custom alignment with different models:**
```bash
conda activate mfa
mfa align corpus/ english_mfa english_mfa aligned_output/
```

### Troubleshooting Commands

**Check MFA installation:**
```bash
conda activate mfa
mfa version
```

**List available models:**
```bash
mfa model download dictionary --list
mfa model download acoustic --list
```

**Fix common installation issues:**
```bash
conda activate mfa
conda install -c conda-forge montreal-forced-aligner -y
```

## Advanced Usage

### Audio Preprocessing

If your audio doesn't meet MFA requirements (mono, 16kHz, PCM 16-bit):

```bash
conda activate mfa
./scripts/prepare_audio.sh
```

Processed files are saved to `wav_processed/`. To use them, update the `WAV_DIR` variable in `run_all.sh`:

```bash
WAV_DIR="${WORKDIR}/wav_processed"
```

### Corpus Validation Only

Validate your corpus without running alignment:

```bash
conda activate mfa
./scripts/validate_corpus.sh
```

### Analyze Existing TextGrids

Analyze statistics from already-generated TextGrid files:

```bash
python3 tools/analyze_textgrids.py aligned_output/
```

### Analyze OOV Words

Get detailed analysis of out-of-vocabulary words:

```bash
python3 tools/analyze_oov.py logs/validate_*.txt
```

### Clean Workspace

Remove all generated files and start fresh:

```bash
./scripts/clean_workspace.sh
```

### Custom MFA Configuration

Edit `run_all.sh` to customize alignment settings:

```bash
# Change MFA models
MFA_DICT="english_us_arpa"           # Dictionary model
MFA_ACOUSTIC="english_us_arpa"       # Acoustic model

# Change parallel processing
mfa align ... -j 4                   # Use 4 CPU cores

# Change input/output directories
WAV_DIR="${WORKDIR}/wav"             # Audio input directory
TRANS_DIR="${WORKDIR}/transcripts"   # Transcript input directory
OUTPUT_DIR="${WORKDIR}/aligned_output" # TextGrid output directory
```

## Understanding the Output

### TextGrid Files

- **Location:** `aligned_output/`
- **Format:** Praat TextGrid format
- **Contains:** Phone-level and word-level time alignments
- **Usage:** Open with Praat for phonetic analysis

**To view in Praat:**
1. Download Praat from https://www.fon.hum.uva.nl/praat/
2. Open Praat → Read → Read from file → Select TextGrid
3. Read → Read from file → Select corresponding WAV file
4. Select both → View & Edit

### Metrics Report

The pipeline displays comprehensive metrics:

- Input file counts (WAV, LAB)
- Output file count (TextGrid)
- Alignment coverage percentage
- OOV (Out-of-Vocabulary) statistics
- Validation errors/warnings

### Log Files

- `logs/pipeline_*.log` - Complete pipeline execution log
- `logs/validate_*.txt` - Corpus validation results
- `logs/align_*.txt` - Alignment process log

Check these files for detailed information and troubleshooting.

## Troubleshooting

### Common Issues and Solutions

**1. "mfa command not found"**

Solution:
```bash
conda activate mfa
mfa version
```

**2. "No TextGrid files generated"**

Possible causes:
- Audio and transcript files don't match
- Audio format issues
- High OOV rate

Solutions:
```bash
# Check validation log
cat logs/validate_*.txt

# Preprocess audio
./scripts/prepare_audio.sh

# Check file naming
ls wav/
ls transcripts/
```

**3. High OOV (Out-of-Vocabulary) rate**

Solution: Use MFA's G2P (grapheme-to-phoneme) to generate pronunciations:
```bash
conda activate mfa
mfa g2p english_us_arpa corpus/ output_dict.txt
# Review and add generated pronunciations to custom dictionary
```

**4. Audio format errors**

Solution:
```bash
./scripts/prepare_audio.sh
# Then update run_all.sh to use wav_processed/
```

**5. "No module named '_kalpy'" error**

Solution:
```bash
conda activate mfa
conda install -c conda-forge montreal-forced-aligner -y
```

**6. Permission denied on scripts**

Solution:
```bash
chmod +x run_all.sh
chmod +x scripts/*.sh
```

### Getting Help

1. Check the `logs/` directory for detailed error messages
2. Review MFA documentation: https://montreal-forced-aligner.readthedocs.io/
3. Verify your data format matches requirements
4. Check validation output for specific issues

### Diagnostic Commands

```bash
# Check MFA version
conda activate mfa
mfa version

# List available models
mfa model download dictionary --list
mfa model download acoustic --list

# Validate corpus manually
mfa validate corpus/ english_us_arpa

# Check Python environment
conda activate mfa
python --version
pip list | grep montreal
```

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review pipeline logs in `logs/` directory
3. Consult MFA documentation

---
