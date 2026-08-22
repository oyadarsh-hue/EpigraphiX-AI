"""
EpigraphiX-AI: Automated Test Suite for Dynamic Palm-Leaf Inscription Edit Operations
Verifies that palm-leaf character sequences produce authentic, dynamic, and non-static:
- Levenshtein Edit Distance (distance >= 0)
- Character Substitutions (substitutions >= 0)
- Weathered Character Insertions (insertions > 0 across eroded candidates)
- Spurious Artifact Deletions (deletions > 0 across noisy candidates)
- Match Confidence (%)
"""

import sys
import os
import json
import numpy as np

# Ensure UTF-8 output encoding across Windows terminals safely
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def split_malayalam_graphemes(word):
    vowel_signs = set(['ാ', 'ി', 'ീ', 'ു', 'ൂ', 'ൃ', 'െ', 'േ', 'ൈ', 'ൊ', 'ോ', 'ൌ', 'ൗ', '്', 'ം', 'ഃ'])
    graphemes = []
    curr = ''
    for ch in word:
        if ch in vowel_signs and curr:
            curr += ch
        else:
            if curr:
                graphemes.append(curr)
            curr = ch
    if curr:
        graphemes.append(curr)
    return graphemes

def generate_epigraphical_raw_sequence(word, feature_seed):
    confusion_map = {
        'ത': 'ദ', 'ദ': 'ത', 'ണ': 'ന', 'ന': 'ണ', 'പ': 'വ', 'വ': 'പ',
        'ഭ': 'ബ', 'ബ': 'ഭ', 'ര': 'റ', 'റ': 'ര', 'ല': 'ള', 'ള': 'ല',
        'ശ': 'ഷ', 'ഷ': 'ശ', 'ധ': 'ഥ', 'ഥ': 'ധ', 'ഘ': 'ഗ', 'ഗ': 'ഘ',
        'ക': 'ഖ', 'ഖ': 'ക', 'മ': 'പ'
    }
    spurious_artifacts = ['ം', '്', 'ി', 'ര', 'ത', 'പ', 'ല']
    graphemes = split_malayalam_graphemes(word)
    if len(graphemes) == 0:
        return word

    seed = abs(int(feature_seed))
    mode = seed % 6

    out_chars = list(graphemes)

    if mode == 0:
        pass
    elif mode == 1:
        idx = (seed * 3) % len(out_chars)
        orig = out_chars[idx]
        base_char = orig[0]
        out_chars[idx] = confusion_map.get(base_char, 'ദ') + orig[1:]
    elif mode == 2:
        if len(out_chars) >= 2:
            drop_idx = (seed * 7) % len(out_chars)
            out_chars.pop(drop_idx)
    elif mode == 3:
        ins_idx = (seed * 5) % (len(out_chars) + 1)
        artifact = spurious_artifacts[(seed * 11) % len(spurious_artifacts)]
        out_chars.insert(ins_idx, artifact)
    elif mode == 4:
        if len(out_chars) >= 2:
            out_chars.pop((seed * 7) % len(out_chars))
        idx = (seed * 3) % len(out_chars)
        base_char = out_chars[idx][0]
        out_chars[idx] = confusion_map.get(base_char, 'ത') + out_chars[idx][1:]
    elif mode == 5:
        artifact = spurious_artifacts[(seed * 13) % len(spurious_artifacts)]
        out_chars.insert((seed * 5) % (len(out_chars) + 1), artifact)
        idx = (seed * 3) % len(out_chars)
        base_char = out_chars[idx][0]
        out_chars[idx] = confusion_map.get(base_char, 'ത') + out_chars[idx][1:]

    return '-'.join(out_chars)

def compute_edit_operations(raw_input, candidate_input):
    a = raw_input.replace('-', '')
    b = candidate_input
    m, n = len(a), len(b)

    if m == 0 and n == 0:
        return {'distance': 0, 'substitutions': 0, 'insertions': 0, 'deletions': 0, 'confidence': '100.0%'}

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j])

    i, j = m, n
    subs, ins, dels = 0, 0, 0
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            i -= 1; j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            subs += 1; i -= 1; j -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            ins += 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            dels += 1; i -= 1
        else:
            break

    distance = dp[m][n]
    max_len = max(m, n, 1)
    sim = max(0.0, 1.0 - distance / max_len)
    confidence = f"{sim * 100:.1f}%"

    return {
        'distance': distance,
        'substitutions': subs,
        'insertions': ins,
        'deletions': dels,
        'confidence': confidence
    }

def test_dynamic_edit_operations_across_lexicon():
    test_words = ['ഗുണമേന്മ', 'അറിവ്', 'കരുണ', 'അത്ഭുതം', 'മലയാളം', 'കൃത്രിമബുദ്ധി', 'താളിയോല']

    observed_insertions = 0
    observed_deletions = 0
    observed_substitutions = 0
    observed_exact_matches = 0

    print("=" * 70)
    print("Testing Dynamic Edit Operations (Insertions, Deletions, Substitutions)")
    print("=" * 70)

    for word in test_words:
        print(f"\n[EVALUATING WORD] '{word}':")
        for seed in range(6):
            raw = generate_epigraphical_raw_sequence(word, seed)
            ops = compute_edit_operations(raw, word)

            if ops['insertions'] > 0: observed_insertions += 1
            if ops['deletions'] > 0: observed_deletions += 1
            if ops['substitutions'] > 0: observed_substitutions += 1
            if ops['distance'] == 0: observed_exact_matches += 1

            print(f"  Seed {seed} (Mode {seed%6}): Raw='{raw}' -> Dist: {ops['distance']}, Subs: {ops['substitutions']}, Ins: {ops['insertions']}, Dels: {ops['deletions']}, Conf: {ops['confidence']}")

    print("\n" + "=" * 70)
    print("Aggregate Edit Operations Distribution:")
    print(f"  Total Exact Matches (Dist=0) : {observed_exact_matches}")
    print(f"  Total Insertions Observed    : {observed_insertions}")
    print(f"  Total Deletions Observed     : {observed_deletions}")
    print(f"  Total Substitutions Observed : {observed_substitutions}")
    print("=" * 70)

    # Asserts that insertions and deletions are genuinely dynamic (not static 0!)
    assert observed_insertions > 0, "Insertions are stuck at 0!"
    assert observed_deletions > 0, "Deletions are stuck at 0!"
    assert observed_substitutions > 0, "Substitutions are stuck at 0!"
    assert observed_exact_matches > 0, "Exact matches missing!"

if __name__ == "__main__":
    test_dynamic_edit_operations_across_lexicon()
    print("\n🎉 ALL DYNAMIC EDIT OPERATIONS TESTS PASSED (100% Non-Static & Responsive)!")
