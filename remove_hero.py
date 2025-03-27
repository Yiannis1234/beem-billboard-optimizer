#!/usr/bin/env python
# Simple script to remove the hero container from app_code.py

with open('app_code.py', 'r') as file:
    content = file.read()

# Find the else section that contains the homepage content
if 'else:' in content:
    # Split content at the else
    parts = content.split('else:')
    if len(parts) > 1:
        # Find the Features section part
        features_index = parts[1].find('# Features section')
        if features_index > -1:
            # Replace the content between 'else:' and '# Features section'
            # with just a newline + 4 spaces
            parts[1] = '\n    ' + parts[1][features_index:]
            
            # Join the content back together
            new_content = 'else:'.join(parts)
            
            # Write the result back to the file
            with open('app_code.py', 'w') as file:
                file.write(new_content)
            
            print("Hero container removed successfully!")
        else:
            print("Features section not found in the code.")
    else:
        print("Could not parse the 'else:' section properly.")
else:
    print("'else:' section not found in the code.") 