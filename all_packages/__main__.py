import os
import re
import shutil
import subprocess
import sys
import urllib.request
import venv


class ExtendedEnvBuilder(venv.EnvBuilder):
    """Virtual environment builder for installing a single package."""

    def __init__(self, package_name: str):
        """Intialize with a given package name to install."""
        super().__init__(with_pip=True)
        self.package_name = package_name

    def post_setup(self, context):
        """Install the package."""
        args = [context.env_exe, '-m', 'pip', 'install', self.package_name, '--disable-pip-version-check']
        subprocess.run(args, check=True)


def rmtree(path: str):
    """Like shutil.rmtree but ignores error if path does not exist."""
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


def main():
    """Install each package from PyPI in its own virtual environment."""
    # validate arguments
    if (len(sys.argv) != 2 and len(sys.argv) != 4 or
        len(sys.argv) > 1 and sys.argv[1] != 'install' or
        len(sys.argv) == 4 and sys.argv[2] != '-d'):
        print('Usage: all_packages install [-d DIRECTORY]')
        return

    # determine installation location
    if len(sys.argv) == 4:
        root_dir = sys.argv[3]
    else:
        root_dir = os.path.expanduser(f'~{os.sep}all_packages')
    if os.path.exists(root_dir):
        answer = input(f'{root_dir} exists, and continuing will delete all its contents. Continue? (y/n): ')
        if answer.startswith('y') or answer.startswith('Y'):
            print(f'Deleting {root_dir} ... ', end='', flush=True)
            rmtree(root_dir)
            print('Done')
        else:
            print('Installation has been cancelled.')
            return

    # get list of all PyPI packages
    print('Getting list of all PyPI packages ... ', end='', flush=True)
    html = urllib.request.urlopen('https://pypi.org/simple/').read().decode('utf-8')
    pattern = re.compile(r'>([^<]+)</a>')
    all_packages = [match[1] for match in re.finditer(pattern, html)]
    print(f'Found {len(all_packages):,} packages\n')

    # install packages
    successful_count = 0
    fail_count = 0
    for package_name in all_packages:
        builder = ExtendedEnvBuilder(package_name)
        venv_dir = os.path.join(root_dir, package_name)
        print(f'===> Start installing {package_name!r} <===')
        try:
            builder.create(venv_dir)
            successful_count += 1
        except KeyboardInterrupt:
            fail_count += 1
            rmtree(venv_dir)
            print('Installation cancelled.')
            break
        except:
            fail_count += 1
            print(f'===> Error installing {package_name!r} <===\n')
            rmtree(venv_dir)
        else:
            print(f'===> Successfully installed {package_name!r} <===\n')
    print(f'Successfully installed {successful_count} package{"" if successful_count == 1 else "s"}.')
    print(f'Failed to install {fail_count} package{"" if fail_count == 1 else "s"}.')


if __name__ == '__main__':
    main()
