# QUICKSTART GUIDE - MFA Forced Alignment Pipeline

This guide will get you up and running in 5 minutes!

## 🚀 Super Quick Start (3 Commands)

```bash
# 1. Setup environment
./setup_mfa.sh

# 2. Activate environment  
conda activate mfa

# 3. Run pipeline
./run_all.sh
```

That's it! Your TextGrids will be in `aligned_output/`

---

## 📋 Step-by-Step Guide

### Step 1: Prerequisites Check

**Do you have Conda?**
```bash
conda --version
```

- ✅ If you see a version number → Continue to Step 2
- ❌ If you get "command not found" → Install Miniconda:
  ```bash
  # macOS
  brew install miniconda
  
  # Or download from:
  # https://docs.conda.io/en/latest/miniconda.html
  ```

### Step 2: Setup MFA Environment

```bash
# Make sure you're in the project directory
cd /path/to/mfa-aligner

# Run setup script
chmod +x setup_mfa.sh
./setup_mfa.sh
```

**What this does:**
- Creates a conda environment named `mfa`
- Installs Python 3.10
- Installs Montreal Forced Aligner
- Takes about 2-3 minutes

**Expected output:**
```
✅ SUCCESS! MFA installed successfully
```

### Step 3: Activate Environment

```bash
conda activate mfa
```

You should see `(mfa)` appear in your terminal prompt.

### Step 4: Verify Your Data

Your data is already in place:

**Audio files** (in `wav/`):
```
F2BJRLP1.wav
F2BJRLP2.wav
F2BJRLP3.wav
ISLE_SESS0131_BLOCKD02_01_sprt1.wav
ISLE_SESS0131_BLOCKD02_02_sprt1.wav
ISLE_SESS0131_BLOCKD02_03_sprt1.wav
```

**Transcripts** (in `transcripts/`):
```
F2BJRLP1.TXT
F2BJRLP2.TXT
F2BJRLP3.TXT
ISLE_SESS0131_BLOCKD02_01_sprt1.txt
ISLE_SESS0131_BLOCKD02_02_sprt1.txt
ISLE_SESS0131_BLOCKD02_03_sprt1.txt
```

✅ File names match between audio and transcripts!

### Step 5: Run the Pipeline

```bash
chmod +x run_all.sh
./run_all.sh
```

**What happens:**
1. Creates `corpus/` directory
2. Copies audio and transcripts
3. Normalizes transcript extensions to `.lab`
4. Downloads MFA models (first time only)
5. Validates corpus
6. Runs forced alignment (this may take a few minutes)
7. Generates metrics
8. Creates output ZIP file

**Progress indicators:**
```
✓ Audio files copied
✓ Transcripts normalized
✓ Models ready
✓ Validation complete
✓ Alignment complete
```

### Step 6: Check Your Results

**TextGrid files:**
```bash
ls -lh aligned_output/
```

You should see `.TextGrid` files for each audio file.

**View metrics:**
The metrics are printed at the end of the pipeline run, showing:
- Number of files processed
- Alignment coverage
- OOV (out-of-vocabulary) statistics

**Logs:**
```bash
ls -lh logs/
```

Contains detailed logs of validation and alignment.

---

## 🎯 What to Do Next

### Option 1: Inspect Alignments in Praat

1. **Install Praat:**
   - macOS: Download from https://www.fon.hum.uva.nl/praat/
   - Or: `brew install --cask praat`

2. **Open a TextGrid:**
   ```
   File → Open → Read from file → Select a .TextGrid file
   ```

3. **View alignment:**
   - You'll see word and phone boundaries
   - Play audio to hear each segment

### Option 2: Analyze All TextGrids

```bash
python3 python/analyze_textgrids.py ./aligned_output
```

This shows:
- Total duration of all alignments
- Number of intervals, words, phones
- Per-file statistics

### Option 3: Re-run with Different Settings

Edit `run_all.sh` and change:
```bash
# Use different MFA models
MFA_DICT="english_mfa"
MFA_ACOUSTIC="english_mfa"

# Use more CPU cores (faster)
mfa align ... -j 8  # Use 8 cores instead of 4
```

Then run again:
```bash
./run_all.sh
```

---

## 🔧 Optional: Audio Preprocessing

If you have different audio files with varying formats:

```bash
chmod +x prepare_audio.sh
./prepare_audio.sh
```

This converts all audio to:
- Mono (1 channel)
- 16kHz sample rate
- PCM 16-bit encoding

Processed files go to `wav_processed/`

---

## 🧹 Cleanup (When You're Done)

To remove generated files and start fresh:

```bash
chmod +x scripts/clean_workspace.sh
./scripts/clean_workspace.sh
```

This removes:
- `corpus/`
- `aligned_output/`
- `logs/`
- `wav_processed/`
- `*.zip` files

Your original `wav/` and `transcripts/` folders are preserved!

---

## ❓ Troubleshooting

### Problem: "mfa: command not found"

**Solution:**
```bash
conda activate mfa
```

Make sure you see `(mfa)` in your terminal prompt.

### Problem: "No TextGrids generated"

**Solution:**
```bash
# Check validation log for errors
cat logs/validate_*.txt

# Look for OOV (out-of-vocabulary) words
grep -i "oov" logs/validate_*.txt
```

Common causes:
- Transcript doesn't match audio content
- Special characters in transcripts
- Audio quality issues

### Problem: High OOV rate

**Solution:**
```bash
# Generate pronunciations for OOV words
mfa g2p english_us_arpa corpus/ output_dict.txt

# Use the generated dictionary in next run
mfa align corpus/ output_dict.txt english_us_arpa aligned_output/
```

### Problem: "Permission denied"

**Solution:**
```bash
# Make all scripts executable
chmod +x *.sh scripts/*.sh
```

### Problem: "No module named '_kalpy'" Error

**Solution:**
```bash
# Quick fix - run the fix script
chmod +x FIX_KALPY_ERROR.sh
./FIX_KALPY_ERROR.sh

# Or manual fix
conda activate mfa
conda install -c conda-forge montreal-forced-aligner -y
```

**Why this happens:**
MFA requires kalpy which may not install properly via pip. Using conda-forge is more reliable.

---

## 📊 Expected Output Structure

After running the pipeline:

```
mfa-aligner/
├── corpus/                          # Prepared corpus
│   ├── F2BJRLP1.wav
│   ├── F2BJRLP1.lab
│   ├── F2BJRLP2.wav
│   ├── F2BJRLP2.lab
│   └── ...
│
├── aligned_output/                  # TextGrid outputs
│   ├── F2BJRLP1.TextGrid
│   ├── F2BJRLP2.TextGrid
│   └── ...
│
├── logs/                            # Pipeline logs
│   ├── pipeline_20251105_123456.log
│   ├── validate_20251105_123456.txt
│   └── align_20251105_123456.txt
│
└── aligned_output_20251105_123456.zip   # Complete archive
```

---

## 🎓 Understanding the Metrics

When the pipeline completes, you'll see a report like:

```
================================================================================
  MFA ALIGNMENT METRICS REPORT
================================================================================

📁 INPUT FILES
--------------------------------------------------------------------------------
  WAV files (audio):           6
  LAB files (transcripts):     6

📊 OUTPUT FILES
--------------------------------------------------------------------------------
  TextGrid files generated:    6
  Alignment coverage:      100.0%

🔍 VALIDATION RESULTS
--------------------------------------------------------------------------------
  Validation log:           ./logs/validate_20251105_123456.txt
  OOV occurrences:             12
  Unique OOV words:             3
  
  OOV words found:
    - hesitation
    - um
    - uh

================================================================================
  SUMMARY
================================================================================
  ✅ Alignment completed successfully!
     6 TextGrid file(s) generated
  ✅ All audio files were aligned
```

**What this means:**
- ✅ **100% coverage**: All audio files were successfully aligned
- ⚠️ **OOV words**: Some words weren't in the dictionary (common for disfluencies)
- 📊 **6 TextGrids**: One output file for each input audio file

---

## 🎉 Success!

You now have:
- ✅ Aligned TextGrid files ready for analysis
- ✅ Detailed logs for troubleshooting
- ✅ Metrics showing alignment quality
- ✅ Complete archive for sharing/submission

**Next Steps:**
1. Open TextGrids in Praat to inspect alignments
2. Use alignments for your research/analysis
3. Share the ZIP file if needed

---

## 📞 Need Help?

1. **Check logs**: `cat logs/pipeline_*.log`
2. **Re-run validation**: `./scripts/validate_corpus.sh`
3. **Read full README**: `README.md`
4. **MFA docs**: https://montreal-forced-aligner.readthedocs.io/

---
