#!/usr/bin/env python3
"""
analyze_textgrids.py - TextGrid Analysis Script

This script analyzes generated TextGrid files to provide detailed statistics
about the alignment quality and content.

Usage:
    python3 analyze_textgrids.py <textgrid_directory>
"""

import os
import sys
import glob
from typing import List, Dict


def read_textgrid(filepath: str) -> Dict:
    """
    Parse a TextGrid file and extract basic statistics.
    
    Args:
        filepath: Path to TextGrid file
    
    Returns:
        Dictionary with TextGrid statistics
    """
    stats = {
        'filename': os.path.basename(filepath),
        'total_duration': 0.0,
        'interval_count': 0,
        'word_count': 0,
        'phone_count': 0,
        'empty_intervals': 0,
        'has_errors': False
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.splitlines()
            
            # Find xmax (total duration)
            for line in lines:
                if 'xmax' in line and '=' in line:
                    try:
                        stats['total_duration'] = float(line.split('=')[1].strip())
                        break
                    except (ValueError, IndexError):
                        pass
            
            # Track current tier to distinguish words from phones
            current_tier = None
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Detect tier type by name
                if 'name =' in line:
                    if '"words"' in line or "'words'" in line:
                        current_tier = 'words'
                    elif '"phones"' in line or "'phones'" in line:
                        current_tier = 'phones'
                    else:
                        current_tier = 'unknown'
                
                # Count intervals based on tier type
                if 'text =' in line:
                    try:
                        text = line.split('=', 1)[1].strip().strip('"').strip()
                        
                        stats['interval_count'] += 1
                        
                        if not text or text == '':
                            stats['empty_intervals'] += 1
                        else:
                            # Count based on tier type
                            if current_tier == 'words':
                                stats['word_count'] += 1
                            elif current_tier == 'phones':
                                stats['phone_count'] += 1
                    except IndexError:
                        pass
    
    except Exception as e:
        stats['has_errors'] = True
        print(f"  Error reading {stats['filename']}: {e}")
    
    return stats


def analyze_directory(directory: str) -> List[Dict]:
    """
    Analyze all TextGrid files in a directory.
    
    Args:
        directory: Path to directory containing TextGrid files
    
    Returns:
        List of statistics dictionaries for each file
    """
    pattern = os.path.join(directory, '*.TextGrid')
    textgrid_files = glob.glob(pattern)
    
    if not textgrid_files:
        return []
    
    print(f"Found {len(textgrid_files)} TextGrid file(s)")
    print("Analyzing...")
    print()
    
    all_stats = []
    for filepath in sorted(textgrid_files):
        stats = read_textgrid(filepath)
        all_stats.append(stats)
    
    return all_stats


def print_summary(all_stats: List[Dict]):
    """
    Print summary statistics for all analyzed TextGrids.
    
    Args:
        all_stats: List of statistics dictionaries
    """
    if not all_stats:
        print("No TextGrid files to analyze.")
        return
    
    print("=" * 80)
    print("  TEXTGRID ANALYSIS SUMMARY")
    print("=" * 80)
    print()
    
    # Aggregate statistics
    total_files = len(all_stats)
    total_duration = sum(s['total_duration'] for s in all_stats)
    total_intervals = sum(s['interval_count'] for s in all_stats)
    total_words = sum(s['word_count'] for s in all_stats)
    total_phones = sum(s['phone_count'] for s in all_stats)
    total_empty = sum(s['empty_intervals'] for s in all_stats)
    files_with_errors = sum(1 for s in all_stats if s['has_errors'])
    
    print("OVERALL STATISTICS")
    print("-" * 80)
    print(f"  Total files analyzed:     {total_files:6d}")
    print(f"  Total duration:           {total_duration:6.1f} seconds ({total_duration/60:.1f} minutes)")
    print(f"  Average duration:         {total_duration/total_files:6.1f} seconds per file")
    print(f"  Total intervals:          {total_intervals:6d}")
    print(f"  Total words detected:     {total_words:6d}")
    print(f"  Total phones detected:    {total_phones:6d}")
    print(f"  Empty intervals:          {total_empty:6d}")
    
    if files_with_errors > 0:
        print(f"  Files with errors:        {files_with_errors:6d}")
    print()
    
    # Per-file details
    print("PER-FILE DETAILS")
    print("-" * 80)
    print(f"{'Filename':<40} {'Duration':>10} {'Words':>8} {'Phones':>8}")
    print("-" * 80)
    
    for stats in all_stats:
        print(f"{stats['filename']:<40} "
              f"{stats['total_duration']:>9.1f}s "
              f"{stats['word_count']:>8d} "
              f"{stats['phone_count']:>8d}")
    
    print()
    print("=" * 80)
    print()


def main():
    """Main entry point."""
    
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_textgrids.py <textgrid_directory>")
        print()
        print("Example:")
        print("  python3 analyze_textgrids.py ./aligned_output")
        sys.exit(1)
    
    textgrid_dir = sys.argv[1]
    
    if not os.path.isdir(textgrid_dir):
        print(f"ERROR: Directory not found: {textgrid_dir}")
        sys.exit(1)
    
    print()
    all_stats = analyze_directory(textgrid_dir)
    
    if all_stats:
        print()
        print_summary(all_stats)
    else:
        print("No TextGrid files found in directory.")
        print()


if __name__ == '__main__':
    main()
