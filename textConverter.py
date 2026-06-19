import subprocess

def escape_string(text: str) -> str:
    escaped = text.encode('unicode_escape').decode('utf-8')
    escaped = escaped.replace('"', '\\"')
    return escaped


if __name__ == "__main__":
    input_file = "text.txt"

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found.")
        input("Press Enter to exit...")
        exit(1)

    escaped = escape_string(content)

    # ✅ Copy to clipboard (Windows)
    subprocess.run("clip", input=escaped, text=True)

    print("✅ Escaped text copied to clipboard!")

    input("Press Enter to exit...")