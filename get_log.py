import subprocess

def get_git_log():
    result = subprocess.run(['git', 'log', '-n', '20', '--pretty=format:%h %s'], capture_output=True, text=True)
    print(result.stdout)

if __name__ == '__main__':
    get_git_log()
