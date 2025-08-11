# Скрипт для пересохранения README.md в UTF-8

input_file = 'README.md'

with open(input_file, 'rb') as f:
    content = f.read()

# Попытаемся декодировать и заменить "битые" символы
text = content.decode('utf-8', errors='replace')

with open(input_file, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"{input_file} пересохранён в UTF-8")
