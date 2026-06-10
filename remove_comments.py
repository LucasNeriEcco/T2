import os
import re
import tokenize
import io

def remove_python_comments(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # Using tokenize to safely remove comments
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    new_tokens = []
    for tok in tokens:
        if tok.type != tokenize.COMMENT:
            new_tokens.append(tok)
            
    out = tokenize.untokenize(new_tokens)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(out)

def remove_html_comments(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove HTML comments
    content = re.sub(r'<!--[\s\S]*?-->', '', content)
    # Remove Jinja comments
    content = re.sub(r'\{#[\s\S]*?#\}', '', content)
    # Clean up empty lines created by comment removal
    content = re.sub(r'\n\s*\n', '\n', content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def remove_css_comments(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def remove_sql_comments(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove inline -- comments
    content = re.sub(r'--.*', '', content)
    # Remove block /* */ comments
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    # Clean up empty lines
    content = re.sub(r'\n\s*\n', '\n', content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def process_dir(directory):
    for root, dirs, files in os.walk(directory):
        if 'venv' in root or '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            path = os.path.join(root, file)
            try:
                if file.endswith('.py'):
                    remove_python_comments(path)
                elif file.endswith('.html'):
                    remove_html_comments(path)
                elif file.endswith('.css'):
                    remove_css_comments(path)
                elif file.endswith('.sql'):
                    remove_sql_comments(path)
                print(f"Processed {file}")
            except Exception as e:
                print(f"Error on {path}: {e}")

process_dir(r'c:\Users\Usuario\Documents\T2\projeto')
