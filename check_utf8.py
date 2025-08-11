import os

def check_encoding(path, exts):
    for root, dirs, files in os.walk(path):
        for file in files:
            if any(file.endswith(ext) for ext in exts):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, encoding='utf-8') as f:
                        f.read()
                except Exception as e:
                    print(f"Encoding error in {file_path}: {e}")

if __name__ == "__main__":
    extensions = ['.py', '.md', '.toml', '.lock', '.cfg', '.ini', '.txt']
    check_encoding(".", extensions)
