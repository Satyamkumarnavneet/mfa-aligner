#!/usr/bin/env python3
"""
metrics.py - Metrics Collection for MFA Alignment Pipeline
  - Counts of input files (WAV, LAB)
  - Counts of output files (TextGrid)
  - OOV (Out-of-Vocabulary) word statistics from validation
  - Alignment coverage statistics

Usage:
    python3 metrics.py <corpus_dir> <output_dir> <validate_log>
"""

import os
import sys
import glob
from typing import Dict


def count_files_by_extension(directory: str, extension: str) -> int:
    """
    Count files with a specific extension in a directory.
    
    Args:
        directory: Path to directory to search
        extension: File extension (e.g., '.wav', '.lab')
    
    Returns:
        Number of files found
    """
    if not os.path.isdir(directory):
        return 0
    
    pattern = os.path.join(directory, f'*{extension}')
    return len(glob.glob(pattern, recursive=False))


def parse_validation_log(log_file: str) -> Dict[str, any]:
    """
    Parse MFA validation log to extract OOV and error statistics.
    
    Args:
        log_file: Path to validation log file
    
    Returns:
        Dictionary with validation statistics
    """
    stats = {
        'oov_count': 0,
        'oov_words': set(),
        'total_utterances': 0,
        'error_count': 0
    }
    
    if not os.path.exists(log_file):
        return stats
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.splitlines()
            
            for line in lines:
                # Count OOV occurrences
                if 'OOV' in line or 'oov' in line.lower():
                    stats['oov_count'] += 1
                
                # Try to extract OOV words (format varies by MFA version)
                if 'not found in dictionary' in line.lower():
                    # Extract word before "not found"
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.lower() == 'not' and i > 0:
                            stats['oov_words'].add(parts[i-1])
                
                # Count actual errors (exclude normal messages like "no errors found")
                line_lower = line.lower()
                if 'error' in line_lower:
                    # Skip lines that indicate NO errors (false positives)
                    if any(phrase in line_lower for phrase in [
                        'no error', 'there were no', '0 error', 'without error',
                        'error read', 'read error', 'no issues'
                    ]):
                        continue
                    # Count only actual error indicators
                    if any(phrase in line_lower for phrase in [
                        ' error:', 'error occurred', 'failed', 'exception',
                        'traceback', 'error -'
                    ]):
                        stats['error_count'] += 1
    
    except Exception as e:
        print(f"Warning: Error parsing validation log: {e}")
    
    return stats


def get_textgrid_stats(output_dir: str) -> Dict[str, any]:
    """
    Get statistics about generated TextGrid files.
    
    Args:
        output_dir: Path to output directory
    
    Returns:
        Dictionary with TextGrid statistics
    """
    stats = {
        'textgrid_count': 0,
        'textgrid_files': []
    }
    
    if not os.path.isdir(output_dir):
        return stats
    
    pattern = os.path.join(output_dir, '*.TextGrid')
    textgrid_files = glob.glob(pattern, recursive=False)
    
    stats['textgrid_count'] = len(textgrid_files)
    stats['textgrid_files'] = [os.path.basename(f) for f in textgrid_files]
    
    return stats


def calculate_coverage(wav_count: int, textgrid_count: int) -> float:
    """
    Calculate alignment coverage percentage.
    
    Args:
        wav_count: Number of input WAV files
        textgrid_count: Number of output TextGrid files
    
    Returns:
        Coverage percentage (0-100)
    """
    if wav_count == 0:
        return 0.0
    return (textgrid_count / wav_count) * 100


def print_metrics_report(corpus_dir: str, output_dir: str, validate_log: str):
    """
    Generate and print comprehensive metrics report.
    
    Args:
        corpus_dir: Path to corpus directory
        output_dir: Path to output directory
        validate_log: Path to validation log file
    """
    print("=" * 80)
    print("  MFA ALIGNMENT METRICS REPORT")
    print("=" * 80)
    print()
    
    # Count input files
    print("INPUT FILES")
    print("-" * 80)
    wav_count = count_files_by_extension(corpus_dir, '.wav')
    lab_count = count_files_by_extension(corpus_dir, '.lab')
    print(f"  WAV files (audio):        {wav_count:4d}")
    print(f"  LAB files (transcripts):  {lab_count:4d}")
    
    if wav_count != lab_count:
        print(f"  WARNING: Mismatch between WAV and LAB file counts!")
    print()
    
    # Count output files
    print("OUTPUT FILES")
    print("-" * 80)
    tg_stats = get_textgrid_stats(output_dir)
    textgrid_count = tg_stats['textgrid_count']
    print(f"  TextGrid files generated: {textgrid_count:4d}")
    
    # Calculate coverage
    coverage = calculate_coverage(wav_count, textgrid_count)
    print(f"  Alignment coverage:       {coverage:5.1f}%")
    print()
    
    # Parse validation log
    print("VALIDATION RESULTS")
    print("-" * 80)
    val_stats = parse_validation_log(validate_log)
    
    if os.path.exists(validate_log):
        print(f"  Validation log:           {validate_log}")
        print(f"  OOV occurrences:          {val_stats['oov_count']:4d}")
        
        if val_stats['oov_words']:
            print(f"  Unique OOV words:         {len(val_stats['oov_words']):4d}")
            if len(val_stats['oov_words']) <= 20:
                print(f"\n  OOV words found:")
                for word in sorted(val_stats['oov_words']):
                    print(f"    - {word}")
        
        if val_stats['error_count'] > 0:
            print(f"  Errors found:              {val_stats['error_count']:4d}")
    else:
        print(f"  WARNING: Validation log not found: {validate_log}")
    print()
    
    # Summary
    print("=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    
    if textgrid_count > 0:
        print("  Alignment completed successfully!")
        print(f"     {textgrid_count} TextGrid file(s) generated")
        
        if coverage >= 100:
            print("  All audio files were aligned")
        elif coverage >= 90:
            print("  Most audio files were aligned")
        else:
            print("  Some audio files were not aligned")
    else:
        print("  No TextGrid files generated - alignment may have failed")
    
    print()
    print("Next steps:")
    print("   1. Review the alignment coverage and investigate any missing files")
    print("   2. Check validation log for OOV words and add them to dictionary if needed")
    print("   3. Open TextGrid files in Praat to visually inspect alignment quality")
    print("   4. If OOV rate is high, consider using MFA's G2P (grapheme-to-phoneme)")
    print()
    print("=" * 80)
    print()


def main():
    """Main entry point for metrics collection."""
    
    # Parse command line arguments
    if len(sys.argv) < 4:
        print("Usage: python3 metrics.py <corpus_dir> <output_dir> <validate_log>")
        print()
        print("Example:")
        print("  python3 metrics.py ./corpus ./aligned_output ./logs/validate.txt")
        sys.exit(1)
    
    corpus_dir = sys.argv[1]
    output_dir = sys.argv[2]
    validate_log = sys.argv[3]
    
    # Validate directories exist
    if not os.path.isdir(corpus_dir):
        print(f"ERROR: Corpus directory not found: {corpus_dir}")
        sys.exit(1)
    
    if not os.path.isdir(output_dir):
        print(f"WARNING: Output directory not found: {output_dir}")
        print("   (This is normal if alignment hasn't run yet)")
    
    # Generate report
    print_metrics_report(corpus_dir, output_dir, validate_log)


if __name__ == '__main__':
    main()
