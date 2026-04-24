import re

files_to_fix = [
    'lab/exp5/intro.md',
    'lab/exp9/experiment-09-ansible.md'
]

for filepath in files_to_fix:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # We want to replace {{ ... }} with {% raw %}{{ ... }}{% endraw %}
    # But wait, maybe the user has multiple {{ }} on the same line.
    
    # Let's just wrap the entire codeblock that contains {{ with raw tags
    def replacer(match):
        block = match.group(0)
        if "{{" in block:
            # check if it already has raw
            if "{% raw %}" not in block:
                return "{% raw %}\n" + block + "\n{% endraw %}"
        return block

    # match markdown code blocks
    new_content = re.sub(r'```.*?```', replacer, content, flags=re.DOTALL)
    
    # also handle inline code `...` that might contain {{
    def inline_replacer(match):
        block = match.group(0)
        if "{{" in block:
            if "{% raw %}" not in block:
                return "{% raw %}" + block + "{% endraw %}"
        return block
    
    new_content = re.sub(r'`[^`]*`', inline_replacer, new_content)
    
    with open(filepath, 'w') as f:
        f.write(new_content)

print("Fixed.")
