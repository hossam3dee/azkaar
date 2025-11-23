import re
import json
import os

def parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by the major divider '*'
    sections = content.split('*')
    prayers = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        lines = section.split('\n')
        # Filter out empty lines
        lines = [line.strip() for line in lines if line.strip()]

        if not lines:
            continue

        # Format assumption:
        # Line 0: Title (Ignore)
        # ... Prayer text ...
        # Line with ----[number]
        # ... Source ...

        # Find the divider line index
        divider_index = -1
        count = 1
        
        for i, line in enumerate(lines):
            if line.startswith('----'):
                divider_index = i
                # Extract number if present
                match = re.search(r'----(\d+)', line)
                if match:
                    count = int(match.group(1))
                break
        
        if divider_index == -1:
            # Fallback if no divider found (shouldn't happen based on file review but good for safety)
            # Maybe it's just text?
            continue

        # Prayer text is everything between title (index 0) and divider
        # Wait, the prompt says "first a title, ignore that".
        # So index 0 is title.
        # Prayer is index 1 to divider_index - 1
        
        prayer_lines = lines[1:divider_index]
        prayer_text = ' '.join(prayer_lines)

        # Source is everything after divider
        source_lines = lines[divider_index+1:]
        source_text = ' '.join(source_lines)

        prayers.append({
            "content": prayer_text,
            "count": count,
            "source": source_text,
            "length": len(prayer_text.split()) # Word count for sorting
        })

    # Sort: Least number of saying -> Highest number.
    # If same number -> Sort by length (how many words)
    prayers.sort(key=lambda x: (x['count'], x['length']))

    return prayers

morning_prayers = parse_file('d:/Azkar+/morning.txt')
night_prayers = parse_file('d:/Azkar+/night.txt')

data = {
    "morning": morning_prayers,
    "night": night_prayers
}

with open('data_utf8.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
