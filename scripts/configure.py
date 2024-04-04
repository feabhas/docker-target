#!/usr/bin/python3
import os
import shutil
import sys
import urllib.request
import urllib.error
from zipfile import ZipFile
from io import BytesIO
from pathlib import Path


class Config:
    repo_suffix = '_exercises'
    url_code_base = 'http://codeload.github.com/feabhas/'
    url_code_path = '/zip/refs/heads/main'
    branch = 'main'
    cpp_courses = [
        'AC++11-401 "Transitioning to Modern C++ (C++11/14/17)"',
        'AC++11-501 "Advanced Modern C++ for Embedded Developers (C++11/14/17)"',
        'AC++11-502 "Advanced Real-Time Modern C++ (C++11/14/17)"',
        'AC++11-CACHE-502 "Advanced Modern C++ Customised for Cache & Performance"',
        'C++11-501 "Modern C++ for Embedded Systems (C++11/14/17)"',
        'C++11-502 "Real-Time Modern C++ (C++11/14/17")',
        'C++20-302 "Migrating to C++20/23"',
    ]
    other_courses = [
        'AC-401 "Advanced C Programming"',
        'C-501 "C for Real - Time Embedded Developers"',
        'TDDC-301 "TDD for Embedded C"',
        'TDDC++-301 "TDD for Embedded C+"+',
        'DP11-403 "Design Patterns in Modern C++"',
        'DP11-404 "Real-Time Design Patterns in Modern C++"',
    ]


def read_course_code():
    print('''If you know your course code enter it now or just
press enter to see a list of available courses.''')
    return input('? ').strip().lower()


def choose_course(options: list, heading: str = None, default: str = None):
    if heading:
        print(heading)
    for n, option in enumerate(options, 1):
        print(f'{n:2d} {option}')
    if default:
        print(default)
    choice = input('Enter course code, choice as a number or q to quit? ').strip().lower()
    if not choice:
        return ''
    if choice.startswith('q'):
        raise UserWarning('No choice made')
    if choice.isdigit():
        n = int(choice) - 1
        if 0 <= n < len(options):
            course = options[n]
            return course.split()[0]
    return choice


def download_course(course: str):
    try:
        repo = course + Config.repo_suffix
        url = Config.url_code_base + repo + Config.url_code_path
        path = Path() / f'{repo}'
        if path.exists():
            print(f'Solutions folder "{path.name}" already exists')
            choice = input('Do you want to replace this folder [y/N]? ').strip().lower()
            if not choice.startswith('y'):
                raise UserWarning(f'{path.name} download abandoned')
            shutil.rmtree(path)
        print(f'Downloading archive "{path.name}.zip"\n  {url}')
        with urllib.request.urlopen(url) as fp:
            zipfile = ZipFile(BytesIO(fp.read()))
            for name in zipfile.namelist():
                if name.startswith('.git'):
                    continue
                zipfile.extract(name)
        unzip = Path() / f'{repo}-{Config.branch}'
        unzip.rename(repo)
    except urllib.error.HTTPError:
        print(f'Cannot find exercises for course "{course}"\nPlease check your spelling or ask your instructor for help')


def course_repo(code: str):
    repo = code.replace('++', 'pp').lower()
    return 'acpp20-302' if repo == 'cpp20-302' else repo


def do_fetch_exercises():
    course = read_course_code()
    if not course:
        course = choose_course(Config.cpp_courses,
                               heading='\nC++ courses',
                               default='Press enter for a list of C, TDD or design pattern courses.')
        if not course:
            course = choose_course(Config.other_courses, heading='\nOther courses')
    if not course:
        raise UserWarning('No course chosen')
    repo = course_repo(course)
    download_course(repo)


def main():
    status = 1
    try:
        do_fetch_exercises()
        status = 0
    except UserWarning as ex:
        print(ex, file=sys.stderr)
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as ex:
        print(ex, file=sys.stderr)
        import traceback
        print(traceback.format_exc(), file=sys.stderr)
    if sys.platform == 'win32' and not os.getenv('PROMPT'):
        input('Press enter to close the window')
    exit(status)


if __name__ == '__main__':
    main()
