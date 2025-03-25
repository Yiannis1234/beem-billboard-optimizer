import re
import sys

def fix_indentation(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split into lines and fix indentation
    lines = content.split('\n')
    
    # Special case for try-except block
    try_block_start = 0
    needs_except = False
    
    # First pass: locate and fix try-except
    for i, line in enumerate(lines):
        if line.strip() == "try:":
            try_block_start = i
            needs_except = True
        elif needs_except and (line.strip().startswith("except") or line.strip().startswith("finally")):
            needs_except = False
    
    # If we found a try without except, add except block
    if needs_except and try_block_start > 0:
        # Find the end of the try block (next line with same indent as try)
        try_line = lines[try_block_start]
        try_indent = len(try_line) - len(try_line.lstrip())
        
        # Look for a line that has the same indentation
        for i in range(try_block_start + 1, len(lines)):
            line = lines[i]
            if line.strip() and (len(line) - len(line.lstrip())) <= try_indent:
                # Insert except block before this line
                indent_str = ' ' * try_indent
                lines.insert(i, f"{indent_str}except Exception as e:")
                lines.insert(i+1, f"{indent_str}    st.error(f\"An error occurred: {{e}}\")")
                break
    
    # Track specific indentation issues
    # Format: (start_line, end_line, current_indent, target_indent)
    patterns = [
        # Weather icon section fix
        (574, 596, 12, 8),  # Fix lines with extra indent
        (576, 577, 8, 12),  # Fix if statements that need deeper indent
        (578, 580, 0, 12),  # Fix lines inside if that need deeper indent
        (579, 580, 8, 12),  # Fix elif statements
        (581, 582, 0, 12),  # Fix lines inside elif
        (582, 584, 8, 12),  # Fix more conditionals
        
        # Traffic conditions
        (630, 650, 12, 8),
        # Other sections with indentation issues
        (805, 815, 12, 8),
        (840, 860, 12, 8),
        (906, 950, 12, 8),
        (950, 965, 16, 8),
        (965, 990, 16, 8),
        (1183, 1200, 12, 8),  # Try block
        (1185, 1186, 8, 12),  # Try block first line
        (1186, 1190, 8, 12),  # Lines inside try
        (1271, 1290, 16, 8),  # Exception block 
        (1273, 1285, 16, 12),  # Lines inside except
        (1288, 1300, 12, 8),  # After try/except
        (1348, 1400, 12, 8),  # Time display section
        (1442, 1500, 12, 8),  # Visualization section
        (1554, 1560, 12, 4)  # Main try-except end
    ]
    
    # Second pass: fix all other indentation issues
    fixed_lines = []
    for i, line in enumerate(lines):
        line_num = i + 1
        if not line.strip():  # Empty line, keep as is
            fixed_lines.append(line)
            continue
            
        spaces = len(line) - len(line.lstrip(' '))
        
        # Default: keep line as is
        fixed_line = line
        
        # Check if this line falls into any pattern to fix
        for start, end, current, target in patterns:
            if start <= line_num <= end and spaces == current:
                # Replace indentation
                fixed_line = ' ' * target + line[spaces:]
                break
        
        fixed_lines.append(fixed_line)
    
    # Write fixed content back to file
    with open(file_path, 'w') as file:
        file.write('\n'.join(fixed_lines))
    
    return "File indentation fixed successfully!"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "app.py"  # Default
    
    print(fix_indentation(file_path)) 