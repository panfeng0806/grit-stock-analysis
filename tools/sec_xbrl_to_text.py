#!/usr/bin/env python3
"""
sec-xbrl-to-text — Convert SEC iXBRL HTML filings to clean readable text.

Usage:
    python3 sec_xbrl_to_text.py <input.html> [output.txt]

If output is omitted, prints to stdout.
"""
import re
import html as html_mod
import sys


def sec_xbrl_to_text(content):
    """Convert SEC iXBRL HTML content to readable plain text."""
    # Step 1: Remove XBRL-specific inline tags
    content = re.sub(r'<ix:[^>]+/?>', '', content)
    content = re.sub(r'</ix:[^>]+>', '', content)
    
    # Step 1b: ⚠️ CRITICAL - Remove <ix:hidden>...</ix:hidden> blocks ENTIRELY
    # These contain XBRL context definitions, unit references, and schema data
    # that have no human-readable value. Must remove content between tags too.
    content = re.sub(r'<ix:hidden[^>]*>.*?</ix:hidden>', '', content, flags=re.DOTALL)
    
    # Step 1c: Also remove <div style="display:none"> blocks (SEC inline XBRL wrapper)
    content = re.sub(r'<div[^>]*display\s*:\s*none[^>]*>.*?</div>', '', content, flags=re.DOTALL)

    # Step 2: Replace structural breaks with newlines
    content = re.sub(r'<br\s*/?>', '\n', content)
    content = re.sub(r'<hr[^>]*/?>', '\n---\n', content)

    # Step 3: Replace block-level closing tags with newlines
    for tag in ['</div>', '</p>', '</tr>', '</h1>', '</h2>', '</h3>', '</h4>',
                '</h5>', '</li>', '</table>', '</section>']:
        content = content.replace(tag, '\n')

    # Step 4: Remove all remaining HTML/XML tags
    content = re.sub(r'<[^>]+>', '', content)

    # Step 5: Remove CSS and JS blocks
    content = re.sub(r'\{[^}]*\}', '', content)
    content = re.sub(r'(?s)/\*.*?\*/', '', content)

    # Step 6: Decode HTML entities (&amp; → &, &#160; → space, etc.)
    content = html_mod.unescape(content)

    # Step 7: Collapse whitespace per line, remove empty lines
    lines = [line.strip() for line in content.split('\n')]
    lines = [line for line in lines if line]

    # Step 8: Filter residual XBRL data noise
    filtered = []
    for line in lines:
        # Skip single characters / symbols
        if len(line) <= 1:
            continue
        # Skip XBRL context ID lines (c-123, c-456...)
        if re.match(r'^c-\d+$', line):
            continue
        # Skip pure number lines (XBRL data fragments)
        if re.match(r'^[\d.,\s\-]+$', line) and len(line) < 50:
            continue
        # Skip hash-like strings
        if re.match(r'^[a-f0-9]{32,}$', line):
            continue
        # ⚠️ KEY FIX: Skip XBRL <ix:hidden> data dump lines
        # These are very long lines (>200 chars) with concatenated context IDs,
        # URLs, dates and no readable English words
        if len(line) > 200:
            # Count readable words (alphabetic sequences >= 3 chars)
            words = re.findall(r'[A-Za-z]{3,}', line)
            # If >80% of line is non-alphabetic (URLs, IDs, numbers), it's XBRL noise
            alpha_chars = sum(len(w) for w in words)
            if alpha_chars < len(line) * 0.15:
                continue
        filtered.append(line)

    return '\n\n'.join(filtered)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 sec_xbrl_to_text.py <input.html> [output.txt]")
        sys.exit(1)

    infile = sys.argv[1]
    with open(infile, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    text = sec_xbrl_to_text(content)

    if len(sys.argv) >= 3:
        outfile = sys.argv[2]
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Converted: {len(content):,} → {len(text):,} chars → {outfile}")
    else:
        print(text)


if __name__ == '__main__':
    main()
