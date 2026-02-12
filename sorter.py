import os
import shutil

# ==============================
# CONFIG
# ==============================
SIZE_LIMIT_MB = 95
ROOT = os.getcwd()   # always current directory
LARGE_DIR = "largerfile"

CATEGORIES = {
    "cybersecurity": ["security", "cyber", "defense"],
    "ethical-hacking": ["ethical", "hack", "hacking", "exploit"],
    "network": ["network", "tcp", "udp", "routing", "wireless"],
    "darknet": ["darkweb", "dark", "tor", "onion", "market"],
    "linux": ["linux", "unix", "bash", "kernel"],
    "blackhat": ["blackhat", "malware", "offensive", "redteam"],
    "ceh": ["ceh"],
    "comptia": ["comptia", "security+", "network+"],
    "cryptography": ["crypto", "cryptography", "encryption", "cipher"],
    "forensics": ["forensic", "investigation", "evidence"],
    "python": ["python", "automation", "script"],
    "pentesting": ["pentest", "penetration", "testing"],
    "web": ["web", "http", "xss", "csrf", "browser"]
}
# ==============================


def create_dirs():
    for cat in CATEGORIES:
        os.makedirs(os.path.join(ROOT, cat), exist_ok=True)
    os.makedirs(os.path.join(ROOT, LARGE_DIR), exist_ok=True)


def get_category(filename):
    name = filename.lower()
    for cat, words in CATEGORIES.items():
        for w in words:
            if w in name:
                return cat
    return "cybersecurity"


def move_file(src, dst_folder):
    dst = os.path.join(ROOT, dst_folder, os.path.basename(src))

    # avoid overwrite
    if os.path.exists(dst):
        base, ext = os.path.splitext(dst)
        i = 1
        while os.path.exists(f"{base}_{i}{ext}"):
            i += 1
        dst = f"{base}_{i}{ext}"

    shutil.move(src, dst)


def main():
    print(f"\nScanning: {ROOT}\n")
    create_dirs()

    moved = 0

    for file in os.listdir(ROOT):
        path = os.path.join(ROOT, file)

        if not os.path.isfile(path):
            continue

        if not file.lower().endswith(".pdf"):
            continue

        size_mb = os.path.getsize(path) / (1024 * 1024)

        if size_mb > SIZE_LIMIT_MB:
            move_file(path, LARGE_DIR)
            print(f"[LARGE >95MB] {file}")
        else:
            category = get_category(file)
            move_file(path, category)
            print(f"[{category}] {file}")

        moved += 1

    print(f"\nDone. Moved {moved} files.\n")


if __name__ == "__main__":
    main()
