"""
analyze_oov.py - Out-of-Vocabulary (OOV) Word Analysis

This script analyzes OOV words from MFA validation logs and provides
detailed statistics and recommendations for improving dictionary coverage.

Usage:
    python3 analyze_oov.py <validation_log>
"""

import os
import sys
import re
from collections import Counter
from typing import List, Dict, Tuple


def extract_oov_words_from_log(log_file: str) -> List[str]:
    """
    Extract OOV words from MFA validation log.
    
    Args:
        log_file: Path to validation log file
    
    Returns:
        List of OOV words found
    """
    oov_words = []
    
    if not os.path.exists(log_file):
        return oov_words
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # Look for patterns like "word not in dictionary" or similar
            # This is a heuristic - actual format depends on MFA version
            patterns = [
                r'OOV:\s*(\w+)',
                r'out of vocabulary:\s*(\w+)',
                r'not found in dictionary:\s*(\w+)',
                r'unknown word:\s*(\w+)',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                oov_words.extend(matches)
    
    except Exception as e:
        print(f"Warning: Error parsing log file: {e}")
    
    return oov_words


def read_oov_files(mfa_corpus_dir: str) -> Tuple[List[str], Dict[str, int]]:
    """
    Read OOV words from MFA's generated OOV files.
    
    Args:
        mfa_corpus_dir: Path to MFA corpus directory (~/Documents/MFA/corpus)
    
    Returns:
        Tuple of (list of unique OOV words, dict of word frequencies)
    """
    oov_words = []
    word_frequencies = {}
    
    # Try to read oovs_found.txt (unique words)
    oovs_file = os.path.join(mfa_corpus_dir, 'oovs_found.txt')
    if os.path.exists(oovs_file):
        try:
            with open(oovs_file, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        oov_words.append(word)
        except Exception as e:
            print(f"Warning: Error reading {oovs_file}: {e}")
    
    # Try to read utterance_oovs.txt (per-utterance breakdown)
    utterance_oovs = os.path.join(mfa_corpus_dir, 'utterance_oovs.txt')
    if os.path.exists(utterance_oovs):
        try:
            with open(utterance_oovs, 'r', encoding='utf-8') as f:
                for line in f:
                    # Parse format like "filename.wav: word1 word2 word3"
                    if ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            words = parts[1].strip().split()
                            for word in words:
                                word = word.strip()
                                if word:
                                    word_frequencies[word] = word_frequencies.get(word, 0) + 1
        except Exception as e:
            print(f"Warning: Error reading {utterance_oovs}: {e}")
    
    return oov_words, word_frequencies


def analyze_oov_patterns(oov_words: List[str]) -> Dict[str, List[str]]:
    """
    Analyze patterns in OOV words.
    
    Args:
        oov_words: List of OOV words
    
    Returns:
        Dictionary of patterns found
    """
    patterns = {
        'numbers': [],
        'hyphenated': [],
        'contractions': [],
        'uppercase': [],
        'special_chars': [],
        'short': [],
        'long': []
    }
    
    for word in oov_words:
        # Numbers
        if any(c.isdigit() for c in word):
            patterns['numbers'].append(word)
        
        # Hyphenated
        if '-' in word:
            patterns['hyphenated'].append(word)
        
        # Contractions
        if "'" in word:
            patterns['contractions'].append(word)
        
        # All uppercase (potential acronyms)
        if word.isupper() and len(word) > 1:
            patterns['uppercase'].append(word)
        
        # Special characters
        if any(not c.isalnum() and c not in ['-', "'"] for c in word):
            patterns['special_chars'].append(word)
        
        # Very short
        if len(word) <= 2:
            patterns['short'].append(word)
        
        # Very long
        if len(word) >= 15:
            patterns['long'].append(word)
    
    return patterns


def print_oov_report(oov_words: List[str], word_frequencies: Dict[str, int]):
    """
    Print comprehensive OOV analysis report.
    
    Args:
        oov_words: List of unique OOV words
        word_frequencies: Dictionary of word frequencies
    """
    print("=" * 80)
    print("  OUT-OF-VOCABULARY (OOV) WORDS ANALYSIS")
    print("=" * 80)
    print()
    
    if not oov_words and not word_frequencies:
        print("No OOV words found - all words are in the dictionary!")
        print()
        print("=" * 80)
        return
    
    # Basic statistics
    print("STATISTICS")
    print("-" * 80)
    print(f"  Unique OOV words:        {len(oov_words):6d}")
    print(f"  Total OOV occurrences:   {sum(word_frequencies.values()) if word_frequencies else 'N/A':6}")
    print()
    
    # Most frequent OOVs
    if word_frequencies:
        print("MOST FREQUENT OOV WORDS")
        print("-" * 80)
        sorted_freqs = sorted(word_frequencies.items(), 
                             key=lambda x: x[1], 
                             reverse=True)[:20]
        
        for word, count in sorted_freqs:
            print(f"  {word:<30} {count:>4} occurrences")
        print()
    
    # List all unique OOVs
    if oov_words:
        print("ALL UNIQUE OOV WORDS")
        print("-" * 80)
        for i, word in enumerate(sorted(oov_words), 1):
            print(f"  {i:3d}. {word}")
            if i >= 50:
                print(f"  ... and {len(oov_words) - 50} more")
                break
        print()
    
    # Pattern analysis
    if oov_words:
        patterns = analyze_oov_patterns(oov_words)
        
        print("PATTERN ANALYSIS")
        print("-" * 80)
        
        if patterns['numbers']:
            print(f"  Numbers/Digits:          {len(patterns['numbers']):4d}")
            print(f"    Examples: {', '.join(patterns['numbers'][:5])}")
        
        if patterns['contractions']:
            print(f"  Contractions:            {len(patterns['contractions']):4d}")
            print(f"    Examples: {', '.join(patterns['contractions'][:5])}")
        
        if patterns['hyphenated']:
            print(f"  Hyphenated words:        {len(patterns['hyphenated']):4d}")
            print(f"    Examples: {', '.join(patterns['hyphenated'][:5])}")
        
        if patterns['uppercase']:
            print(f"  Potential acronyms:      {len(patterns['uppercase']):4d}")
            print(f"    Examples: {', '.join(patterns['uppercase'][:5])}")
        
        print()
    
    # Recommendations
    print("💡 RECOMMENDATIONS")
    print("-" * 80)
    print("  1. Use MFA's G2P (grapheme-to-phoneme) to add OOV words:")
    print("     mfa g2p english_us_arpa oov_words.txt output_pronunciations.txt")
    print()
    print("  2. Create a custom dictionary file with pronunciations:")
    print("     - Add words manually to english_us_arpa dictionary")
    print("     - Or create a custom dictionary file")
    print()
    print("  3. Consider using MFA's train_dictionary command:")
    print("     mfa train_dictionary corpus/ dictionary.txt output_dict.txt")
    print()
    print("  4. Check for transcription errors:")
    print("     - Verify spelling in .lab files")
    print("     - Normalize text (lowercase, remove punctuation)")
    print()
    print("=" * 80)
    print()


def main():
    """Main entry point."""
    
    # Default MFA corpus directory
    mfa_corpus_dir = os.path.expanduser('~/Documents/MFA/corpus')
    
    print()
    print("Searching for OOV words...")
    print()
    
    # Try to read OOV files from MFA's default location
    oov_words, word_frequencies = read_oov_files(mfa_corpus_dir)
    
    if not oov_words and not word_frequencies:
        print(f"No OOV files found in {mfa_corpus_dir}")
        print("   This is normal if validation found no OOV words.")
        print()
    
    # If validation log is provided, also extract from there
    if len(sys.argv) >= 2:
        log_file = sys.argv[1]
        log_oovs = extract_oov_words_from_log(log_file)
        if log_oovs:
            oov_words.extend(log_oovs)
            oov_words = list(set(oov_words))  # Remove duplicates
    
    # Print report
    print_oov_report(oov_words, word_frequencies)


if __name__ == '__main__':
    main()
