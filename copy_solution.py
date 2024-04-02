#!/usr/bin/python3
import os
import re
import shutil
import sys
from pathlib import Path


class Config:
    locations = '. .. ~'.split()
    location_names = 'current folder, parent folder or home folder'
    location_patterns = 'solutions exercises/solutions *_exercises/solutions'.split()
    sources = 'src include'.split()
    backup = Path('src.bak')
    solutions = re.compile('^[0-9]?[0-9][A-Z]?[-_]')


def find_solutions():
    for folder in Config.locations:
        root = Path(folder).expanduser()
        for location in Config.location_patterns:
            paths = list(root.glob(location))
            if not paths:
                continue
            if len(paths) > 1:
                raise UserWarning(f'Ambiguous solution locations:\n  ' + '\n  '.join(str(p) for p in paths))
            path, = paths
            if path.is_dir():
                return path
    raise UserWarning(f'Cannot find "exercises" or "solutions" folder in:\n  {Config.location_names}')


def select_solution(solutions: Path):
    folders = [s for s in solutions.iterdir() if s.is_dir() and Config.solutions.match(s.name)]
    for option in folders:
        print(f'{option.name}')
    choice = input('Enter start of solution name (you can omit a leading zero)\nor q to quit? ').strip().lower()
    if not choice or choice.startswith('q'):
        raise UserWarning('No choice made')
    found = [f for f in folders if re.match(f'^0?{choice}', f.name, re.IGNORECASE)]
    if not found:
        raise UserWarning(f'Choice {choice} did not match a solution')
    elif len(found) != 1:
        raise UserWarning(f'Choice {choice} matched more than one solution')
    return found[0]


def move_sources():
    backup = Config.backup
    backup.mkdir(parents=True, exist_ok=True)
    print(f'Moving current source files to "{backup.name}"')
    for folder in Config.sources:
        source = Path(folder)
        target = backup / folder
        if target.exists():
            shutil.rmtree(target)
        if source.exists():
            shutil.move(source, backup)


def copy_solution(solution):
    sources = Config.sources if (solution / 'src').is_dir() else ['.']
    for folder in sources:
        source = solution / folder
        if not source.exists():
            continue
        print(f'Copying solution sources from "{source.parent.name}/{source.name}"')
        target = Path(folder if folder != '.' else 'src')
        shutil.copytree(source, target)


def do_copy_solution():
    solutions = find_solutions()
    solution = select_solution(solutions)
    print(f'Copying solution "{solution.name}"')
    move_sources()
    copy_solution(solution)
    print('You should now rebuild your application')


def main():
    status = 1
    try:
        do_copy_solution()
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
