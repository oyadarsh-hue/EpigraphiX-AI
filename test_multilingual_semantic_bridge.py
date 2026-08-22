"""
EpigraphiX-AI: Automated Test Suite for Multilingual Epigraphical Semantic Bridge
Verifies complete dictionary coverage and valid multilingual translations:
Malayalam -> Old Epigraphical Form, Modern Malayalam, English Exegesis, Hindi Meaning, Genre.
"""

import sys
import io
import json
import os

# Ensure UTF-8 output encoding across Windows terminals
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_dictionary_coverage():
    dict_txt_path = "malayalam_dictionary.txt"
    json_path = os.path.join("web_studio", "comprehensive_dictionary.json")

    assert os.path.exists(dict_txt_path), f"Missing {dict_txt_path}"
    assert os.path.exists(json_path), f"Missing {json_path}"

    with open(dict_txt_path, "r", encoding="utf-8") as f:
        dict_words = [line.strip() for line in f if line.strip()]

    with open(json_path, "r", encoding="utf-8") as f:
        multilingual_db = json.load(f)

    print(f"Total vocabulary words: {len(dict_words)}")
    print(f"Total multilingual database entries: {len(multilingual_db)}")

    missing_words = []
    invalid_entries = []

    for word in dict_words:
        if word not in multilingual_db:
            missing_words.append(word)
        else:
            entry = multilingual_db[word]
            # Check all required keys exist and are non-empty
            for key in ["old", "newLit", "english", "hindi", "genre"]:
                if not entry.get(key) or len(entry[key].strip()) == 0:
                    invalid_entries.append((word, key))

    print(f"Missing words count: {len(missing_words)}")
    print(f"Invalid entries count: {len(invalid_entries)}")

    assert len(missing_words) == 0, f"Words missing from database: {missing_words[:10]}"
    assert len(invalid_entries) == 0, f"Invalid entries: {invalid_entries[:10]}"

    # Spot check specific critical words
    spot_checks = [
        "മലയാളം", "കേരളം", "അക്ഷരം", "ഗുണനിലവാരം", "കൃത്രിമബുദ്ധി",
        "ഭാരതം", "താളിയോല", "ശ്രീഗണപതയേ", "നമഃ", "അവിഘ്നമസ്തു"
    ]
    for sc in spot_checks:
        assert sc in multilingual_db, f"Critical word '{sc}' missing"
        e = multilingual_db[sc]
        print(f"\n[SPOT CHECK] '{sc}':")
        print(f"  Old Form : {e['old']}")
        print(f"  English  : {e['english']}")
        print(f"  Hindi    : {e['hindi']}")
        print(f"  Genre    : {e['genre']}")

if __name__ == "__main__":
    print("=" * 65)
    print("Running EpigraphiX-AI Multilingual Semantic Bridge Test Suite")
    print("=" * 65)
    test_dictionary_coverage()
    print("\n" + "=" * 65)
    print("ALL MULTILINGUAL TESTS PASSED (100% Dictionary Coverage)")
    print("=" * 65)
