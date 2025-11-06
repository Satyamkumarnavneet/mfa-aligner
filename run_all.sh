#!/usr/bin/env bash
###############################################################################
# run_all.sh - Main Pipeline Script for MFA Forced Alignment
# Usage: ./run_all.sh
# Prerequisites: Run ./setup_mfa.sh first and activate the conda environment
###############################################################################

set -euo pipefail

# Configuration Variables
WORKDIR="$(pwd)"
WAV_DIR="${WORKDIR}/wav"
TRANS_DIR="${WORKDIR}/transcripts"
CORPUS_DIR="${WORKDIR}/corpus"
OUTPUT_DIR="${WORKDIR}/aligned_output"
MFA_DICT="english_us_arpa"
MFA_ACOUSTIC="english_us_arpa"

# Logging setup
LOG_DIR="${WORKDIR}/logs"
mkdir -p "${LOG_DIR}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${LOG_DIR}/pipeline_${TIMESTAMP}.log"

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "${LOG_FILE}"
}

log "======================================================================"
log "  MFA Forced Alignment Pipeline - START"
log "======================================================================"
log ""
log "Working Directory: ${WORKDIR}"
log "Corpus Directory: ${CORPUS_DIR}"
log "Output Directory: ${OUTPUT_DIR}"
log ""

# Check if MFA is available
if ! command -v mfa &> /dev/null; then
    log "ERROR: MFA not found. Please run ./setup_mfa.sh first"
    log "   Then activate the environment: conda activate mfa"
    exit 1
fi

log "MFA found: $(mfa version)"
log ""

# Create necessary directories
log "Creating directories..."
mkdir -p "${CORPUS_DIR}" "${OUTPUT_DIR}"

# Step 1: Copy audio files
log "======================================================================"
log "STEP 1: Copying audio files to corpus"
log "======================================================================"
if [ -d "${WAV_DIR}" ]; then
    wav_count=$(find "${WAV_DIR}" -name "*.wav" | wc -l | tr -d ' ')
    log "Found ${wav_count} WAV files"
    cp -v "${WAV_DIR}"/*.wav "${CORPUS_DIR}"/ 2>&1 | tee -a "${LOG_FILE}" || true
    # Remove macOS extended attributes that can cause read timeouts
    xattr -cr "${CORPUS_DIR}"/*.wav 2>/dev/null || true
    log "Audio files copied"
else
    log "Warning: WAV directory not found: ${WAV_DIR}"
fi
log ""

# Step 2: Copy and normalize transcripts
log "======================================================================"
log "STEP 2: Copying and normalizing transcripts"
log "======================================================================"
if [ -d "${TRANS_DIR}" ]; then
    # Copy all transcript files (suppress error if .lab files don't exist)
    cp -v "${TRANS_DIR}"/*.lab "${CORPUS_DIR}"/ 2>/dev/null | tee -a "${LOG_FILE}" || true
    cp -v "${TRANS_DIR}"/*.txt "${CORPUS_DIR}"/ 2>&1 | tee -a "${LOG_FILE}" || true
    cp -v "${TRANS_DIR}"/*.TXT "${CORPUS_DIR}"/ 2>&1 | tee -a "${LOG_FILE}" || true
    
    # Remove macOS extended attributes that can cause read timeouts
    xattr -cr "${CORPUS_DIR}"/*.lab "${CORPUS_DIR}"/*.txt "${CORPUS_DIR}"/*.TXT 2>/dev/null || true
    
    # Normalize extensions to .lab
    log "Normalizing transcript extensions to .lab..."
    for t in "${CORPUS_DIR}"/*.TXT "${CORPUS_DIR}"/*.txt; do
        if [ -e "$t" ]; then
            base=$(basename "$t" | sed 's/\.[^.]*$//')
            mv -v "$t" "${CORPUS_DIR}/${base}.lab" 2>&1 | tee -a "${LOG_FILE}"
        fi
    done
    log "Transcripts normalized"
else
    log "Warning: Transcripts directory not found: ${TRANS_DIR}"
fi
log ""

# Verify corpus setup
log "======================================================================"
log "Corpus Summary:"
log "======================================================================"
wav_count=$(find "${CORPUS_DIR}" -name "*.wav" | wc -l | tr -d ' ')
lab_count=$(find "${CORPUS_DIR}" -name "*.lab" | wc -l | tr -d ' ')
log "WAV files: ${wav_count}"
log "LAB files: ${lab_count}"

if [ "${wav_count}" -eq 0 ] || [ "${lab_count}" -eq 0 ]; then
    log "ERROR: Corpus is incomplete (need both WAV and LAB files)"
    exit 1
fi
log ""

# Step 3: Download MFA models if needed
log "======================================================================"
log "STEP 3: Checking/Downloading MFA models"
log "======================================================================"
log "Dictionary: ${MFA_DICT}"
log "Acoustic Model: ${MFA_ACOUSTIC}"

# Download dictionary
log "Downloading dictionary..."
mfa model download dictionary ${MFA_DICT} 2>&1 | tee -a "${LOG_FILE}" || true

# Download acoustic model
log "Downloading acoustic model..."
mfa model download acoustic ${MFA_ACOUSTIC} 2>&1 | tee -a "${LOG_FILE}" || true
log "Models ready"
log ""

# Step 4: Validate corpus
log "======================================================================"
log "STEP 4: Validating corpus"
log "======================================================================"
VALIDATE_LOG="${LOG_DIR}/validate_${TIMESTAMP}.txt"
log "Running MFA validation..."
mfa validate "${CORPUS_DIR}" "${MFA_DICT}" 2>&1 | tee "${VALIDATE_LOG}" | tee -a "${LOG_FILE}" || {
    log "Validation completed with warnings (this is normal)"
}
log "Validation complete (see ${VALIDATE_LOG})"
log ""

# Step 5: Run alignment
log "======================================================================"
log "STEP 5: Running forced alignment"
log "======================================================================"
ALIGN_LOG="${LOG_DIR}/align_${TIMESTAMP}.txt"
log "This may take several minutes depending on corpus size..."
mfa align "${CORPUS_DIR}" "${MFA_DICT}" "${MFA_ACOUSTIC}" "${OUTPUT_DIR}" \
    -j 4 --clean 2>&1 | tee "${ALIGN_LOG}" | tee -a "${LOG_FILE}"

if [ $? -eq 0 ]; then
    log "Alignment complete"
else
    log "ERROR: Alignment failed. Check ${ALIGN_LOG} for details"
    exit 1
fi
log ""

# Step 6: Generate metrics
log "======================================================================"
log "STEP 6: Generating metrics"
log "======================================================================"
python3 tools/metrics.py "${CORPUS_DIR}" "${OUTPUT_DIR}" "${VALIDATE_LOG}" 2>&1 | tee -a "${LOG_FILE}"
log ""

# Step 7: Create output package
log "======================================================================"
log "STEP 7: Packaging outputs"
log "======================================================================"
OUTPUT_ZIP="${WORKDIR}/aligned_output_${TIMESTAMP}.zip"
if command -v zip &> /dev/null; then
    log "Creating ZIP archive..."
    zip -r "${OUTPUT_ZIP}" "${OUTPUT_DIR}" "${LOG_DIR}" 2>&1 | tee -a "${LOG_FILE}" || true
    log "Archive created: ${OUTPUT_ZIP}"
else
    log "zip command not found, skipping archive creation"
fi
log ""

# Final summary
log "======================================================================"
log "  MFA Forced Alignment Pipeline - COMPLETE"
log "======================================================================"
log ""
log "Results:"
log "   - TextGrids: ${OUTPUT_DIR}/"
log "   - Logs: ${LOG_DIR}/"
log "   - Archive: ${OUTPUT_ZIP}"
log ""
log "Next steps:"
log "   1. Review metrics output above"
log "   2. Open TextGrid files in Praat to inspect alignments"
log "   3. Check logs if any issues occurred"
log ""
log "Pipeline log saved to: ${LOG_FILE}"
log ""
