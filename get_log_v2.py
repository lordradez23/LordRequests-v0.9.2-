import subprocess

def get_git_log():
    result = subprocess.run(['git', 'log', '-n', '30', '--pretty=format:%s'], capture_output=True, text=True)
    with open('git_subjects.txt', 'w', encoding='utf-8') as f:
        f.write(result.stdout)
    print("Done")

if __name__ == '__main__':
    get_git_log()
