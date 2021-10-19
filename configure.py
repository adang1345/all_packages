"""Generate setup.cfg and README_pypi.md, the files needed to build all_packages."""

import urllib.request
import urllib.error
import re
import threading
import datetime


THREAD_COUNT = 1000
MAX_RETRIES = 100

count = 0
count_lock = threading.Lock()
valid_packages = []


def check_validity() -> None:
    """Repeatedly consume a value from all_packages and add it to valid_packages if it is valid.
    Terminate when all_packages is empty."""
    global count
    while True:
        increment = False
        try:
            package_name = all_packages.pop()
        except IndexError:
            break
        while True:
            retry_count = 0
            try:
                urllib.request.urlopen(f'https://pypi.org/project/{package_name}/')
                increment = True
                break
            except urllib.error.HTTPError as ex:
                if ex.code == 404:
                    increment = True
                    break
                raise
            except:
                if (retry_count := retry_count + 1) == MAX_RETRIES:
                    with count_lock:
                        print(f'WARNING: Failed to access {package_name}', flush=True)
                    break
        if increment:
            with count_lock:
                if (count := count + 1) % 1000 == 0:
                    print(f'{count}; {count/all_packages_len:.2f}', flush=True)
            valid_packages.append(package_name)


# Create setup.cfg
html = urllib.request.urlopen('https://pypi.org/simple/').read().decode('utf-8')
pattern = re.compile(r'>([^<]+)</a>')
all_packages = [match[1] for match in re.finditer(pattern, html) if match[1] != 'all_packages']
all_packages_len = len(all_packages)

threads = []
for _ in range(THREAD_COUNT):
    threads.append(thread := threading.Thread(target=check_validity))
    thread.start()
for thread in threads:
    thread.join()
print('Scan of PyPI is complete')

print('Creating setup.cfg ... ', end='', flush=True)
now = datetime.datetime.utcnow()
version = f'{now.year}.{now.month}.{now.day}.{now.hour}.{now.minute}.{now.second}'
valid_packages.sort(key=str.lower)
with open('setup.cfg', 'w') as file, open('setup.cfg.txt') as file2:
    file.write(file2.read().format(version))
    for package_name in valid_packages:
        file.write(f'    {package_name}\n')
print('Done')

# Create README.md
print('Creating README.md ... ', end='', flush=True)
with open('README_pypi.md', 'w') as file, open('README_pypi.md.txt') as file2:
    s = file2.read()
    file.write(s.format(len(valid_packages), now.strftime('%d %b %Y %H:%M:%S UTC')))
print('Done')
