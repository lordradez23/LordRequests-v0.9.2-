import subprocess

def get_git_status():
    result = subprocess.run(['git', 'status'], capture_output=True, text=True)
    with open('status_utf8.txt', 'w', encoding='utf-8') as f:
        f.write(result.stdout)

if __name__ == '__main__':
    get_git_status()
