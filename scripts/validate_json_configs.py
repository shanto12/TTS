#!/usr/bin/env python3
"""Validate JSON configuration files for invalid values.

This script checks JSON files to ensure they don't contain
invalid values like Infinity or NaN that are not compliant
with the JSON standard.

Usage:
    python scripts/validate_json_configs.py [path]
"""

import json
import sys
from pathlib import Path


def validate_json_file(filepath):
    """Validate a single JSON file for invalid values.
    
    Args:
        filepath: Path to the JSON file to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for invalid JSON values
        invalid_patterns = ['Infinity', 'NaN', '-Infinity']
        found_issues = []
        
        for pattern in invalid_patterns:
            if pattern in content:
                found_issues.append(pattern)
                
        if found_issues:
            return False, f"Found invalid JSON values: {', '.join(found_issues)}"
        
        # Try to parse the JSON to ensure it's valid
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            return False, f"JSON parse error: {e}"
            
        return True, None
        
    except Exception as e:
        return False, f"Error reading file: {e}"


def main():
    """Main function to validate JSON config files."""
    # Default to checking common config locations
    search_paths = [
        Path('TTS/tts/configs'),
        Path('TTS/vocoder/configs'),
        Path('TTS/encoder/configs'),
    ]
    
    # Allow custom path from command line
    if len(sys.argv) > 1:
        search_paths = [Path(sys.argv[1])]
    
    all_valid = True
    files_checked = 0
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
            
        # Find all .json files
        json_files = list(search_path.rglob('*.json'))
        
        for json_file in json_files:
            files_checked += 1
            is_valid, error_msg = validate_json_file(json_file)
            
            if not is_valid:
                print(f"❌ INVALID: {json_file}")
                print(f"   {error_msg}")
                all_valid = False
            else:
                print(f"✓ VALID: {json_file}")
    
    print(f"\nChecked {files_checked} JSON file(s)")
    
    if all_valid:
        print("✓ All JSON files are valid!")
        return 0
    else:
        print("❌ Some JSON files contain invalid values!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
