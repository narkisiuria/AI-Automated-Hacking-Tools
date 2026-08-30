import re

def filter_high_severity_lines(raw_output):
    """
    Extracts lines flagged as high-severity by linpeas'/winpeas' ANSI coloring.
    Red / bold-red ANSI codes typically indicate 'likely exploitable' findings.
    """
    red_pattern = re.compile(r'\x1b\[(?:1;)?(?:31|91)m')

    high_severity_lines = []
    for line in raw_output.split('\n'):
        if red_pattern.search(line):
            clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line).strip()
            if clean_line:
                high_severity_lines.append(clean_line)

    return high_severity_lines