import re

files_to_fix = [
    'lab/exp5/intro.md',
    'lab/exp9/experiment-09-ansible.md'
]

for filepath in files_to_fix:
    with open(filepath, 'r') as f:
        content = f.read()
    
    def replacer(match):
        block = match.group(0)
        if "{{" in block:
            return "{% raw %}\n" + block + "\n{% endraw %}"
        return block

    new_content = re.sub(r'```.*?```', replacer, content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(new_content)

print("Fixed.")
