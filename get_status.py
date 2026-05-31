import subprocess

def get_git_status():
    result = subprocess.run(['git', 'status'], capture_output=True, text=True)
    print(result.stdout)

if __name__ == '__main__':
    get_git_status()
