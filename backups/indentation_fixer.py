import re

# Open and read the file
with open('app.py', 'r') as file:
    content = file.read()

# Fix indentation issues
lines = content.split('\n')
fixed_lines = []

# Fix indentation throughout the file
for i, line in enumerate(lines):
    # Fix specific line ranges with known issues (from linter errors)
    if 574 <= i+1 <= 596:  # Lines 574-596 have incorrect indentation
        if i+1 in [578, 579, 580]:  # These lines need a deeper indent (after if/elif)
            if line.strip().startswith(('weather_icon', 'elif')):
                fixed_lines.append('            ' + line.strip())  # 12 spaces for indented block
            else:
                fixed_lines.append(line)
        elif re.match(r'^            ', line):  # If line has 12 spaces (3 indents)
            fixed_lines.append(re.sub(r'^            ', '        ', line))  # Replace with 8 spaces (2 indents)
        else:
            fixed_lines.append(line)
    elif 630 <= i+1 <= 650:  # Lines 630-650 have incorrect indentation
        if re.match(r'^            ', line):  # If line has 12 spaces (3 indents)
            fixed_lines.append(re.sub(r'^            ', '        ', line))  # Replace with 8 spaces (2 indents)
        else:
            fixed_lines.append(line)
    elif 655 <= i+1 <= 665:  # Lines 655-665 have incorrect indentation (traffic conditions)
        if i+1 == 659:  # Line 659 is showing the error
            # This line should be indented at the same level as the previous line
            prev_spaces = len(lines[i-1]) - len(lines[i-1].lstrip())
            this_spaces = len(line) - len(line.lstrip())
            if this_spaces > prev_spaces:
                fixed_lines.append(' ' * prev_spaces + line.lstrip())
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    elif 840 <= i+1 <= 860:  # Lines 840-860 have incorrect indentation
        if re.match(r'^            ', line):  # If line has 12 spaces (3 indents)
            fixed_lines.append(re.sub(r'^            ', '        ', line))  # Replace with 8 spaces (2 indents)
        else:
            fixed_lines.append(line)
    elif 908 <= i+1 <= 1000:  # Lines 908-1000 range with incorrect indentation
        if re.match(r'^            ', line) or re.match(r'^                ', line):  # If line has 12 or 16 spaces
            fixed_line = re.sub(r'^            ', '        ', line)  # Replace with 8 spaces (2 indents)
            fixed_line = re.sub(r'^                ', '            ', fixed_line)  # And deeper indent levels 
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
    elif 1185 <= i+1 <= 1300:  # Lines 1185-1300 range with incorrect indentation in historical data
        if re.match(r'^                ', line):  # If line has 16 spaces (4 indents)
            fixed_lines.append(re.sub(r'^                ', '            ', line))  # Replace with 12 spaces (3 indents)
        else:
            fixed_lines.append(line)
    elif 1350 <= i+1 <= 1450:  # Lines 1350-1450 range with incorrect indentation
        if re.match(r'^            ', line):  # If line has 12 spaces (3 indents)
            fixed_lines.append(re.sub(r'^            ', '        ', line))  # Replace with 8 spaces (2 indents)
        else:
            fixed_lines.append(line)
    elif 1445 <= i+1 <= 1500:  # Lines 1445-1500 range with incorrect indentation
        if re.match(r'^            ', line):  # If line has 12 spaces (3 indents)
            fixed_lines.append(re.sub(r'^            ', '        ', line))  # Replace with 8 spaces (2 indents)
        else:
            fixed_lines.append(line)
    elif 1555 <= i+1 <= 1560:  # Lines 1555-1560 range with incorrect indentation
        if re.match(r'^            ', line):  # If line has 12 spaces (3 indents)
            fixed_lines.append(re.sub(r'^            ', '    ', line))  # Replace with 4 spaces (1 indent)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

# Write the fixed content back to the file
with open('app.py', 'w') as file:
    file.write('\n'.join(fixed_lines))

print('Indentation fixed successfully!') 