
import sys
import os

file_path = "CLAUDE.md"
temp_output_path = os.path.join(sys.argv[1], "claude_md_content.txt")

encodings_to_try = ["utf-8", "big5", "cp950", "utf-8-sig"]

for encoding in encodings_to_try:
    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        
        with open(temp_output_path, "w", encoding="utf-8") as out_f:
            out_f.write(content)
        
        print(f"Successfully read CLAUDE.md with {encoding} and wrote to {temp_output_path}")
        sys.exit(0)
    except UnicodeDecodeError:
        print(f"Failed to decode with {encoding}", file=sys.stderr)
    except FileNotFoundError:
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

print("Could not decode CLAUDE.md with any of the tried encodings.", file=sys.stderr)
sys.exit(1)
