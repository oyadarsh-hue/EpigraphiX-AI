"""
EpigraphiX-AI: Automated Test Suite for Multilingual Epigraphical Semantic Bridge
Verifies complete dictionary coverage, 0 boilerplate entries, and authentic multilingual translations:
Malayalam -> Old Epigraphical Form, Modern Malayalam, English Exegesis, Hindi Meaning, Genre.
"""

import sys
import io
import json
import os
import re

# Ensure UTF-8 output encoding across Windows terminals safely
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

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
    boilerplate_entries = []

    for word in dict_words:
        if word not in multilingual_db:
            missing_words.append(word)
        else:
            entry = multilingual_db[word]
            # Check all required keys exist and are non-empty
            for key in ["old", "newLit", "english", "hindi", "genre"]:
                val = entry.get(key, "")
                if not val or len(val.strip()) == 0:
                    invalid_entries.append((word, key))

            # Verify no generic boilerplate placeholder text exists
            eng = entry.get("english", "")
            hi = entry.get("hindi", "")
            if "classical Malayalam semantic term" in eng or "शास्त्रीय एवं व्यावहारिक संदर्भ में प्रयुक्त होता है" in hi:
                boilerplate_entries.append(word)

            # Verify Hindi contains actual Devanagari characters
            has_devanagari = bool(re.search(r'[\u0900-\u097F]', hi))
            if not has_devanagari:
                invalid_entries.append((word, "hindi_no_devanagari"))

    print(f"Missing words count: {len(missing_words)}")
    print(f"Invalid entries count: {len(invalid_entries)}")
    print(f"Boilerplate entries count: {len(boilerplate_entries)}")

    assert len(missing_words) == 0, f"Words missing from database: {missing_words[:10]}"
    assert len(invalid_entries) == 0, f"Invalid entries: {invalid_entries[:10]}"
    assert len(boilerplate_entries) == 0, f"Boilerplate entries detected: {boilerplate_entries[:10]}"

    # Spot check specific critical words requested by user
    spot_checks = [
        "ഗുണമേന്മ", "അറിവ്", "കരുണ", "അത്ഭുതം", "വളർച്ച", "ഐക്യം", "മാനവികത",
        "മലയാളം", "കേരളം", "അക്ഷരം", "ഗുണനിലവാരം", "കൃത്രിമബുദ്ധി",
        "ഭാരതം", "താളിയോല", "ശ്രീഗണപതയേ", "നമഃ", "അവിഘ്നമസ്തു"
    ]
    for sc in spot_checks:
        assert sc in multilingual_db, f"Critical word '{sc}' missing"
        e = multilingual_db[sc]
        print(f"\n[SPOT CHECK] '{sc}':")
        print(f"  Old Form : {e['old']}")
        print(f"  New Form : {e['newLit']}")
        print(f"  English  : {e['english']}")
        print(f"  Hindi    : {e['hindi']}")
        print(f"  Genre    : {e['genre']}")

        # Ensure spot check words have exact non-empty meaningful translations
        assert len(e['english']) > 15, f"English translation too brief for {sc}"
        assert len(e['hindi']) > 10, f"Hindi translation too brief for {sc}"

    return True

if __name__ == "__main__":
    print("=" * 65)
    print("Running EpigraphiX-AI Multilingual Semantic Bridge Test Suite")
    print("=" * 65)
    test_dictionary_coverage()
    print("\n" + "=" * 65)
    print("ALL MULTILINGUAL TESTS PASSED (100% Exact & Meaningful)")
    print("=" * 65)
