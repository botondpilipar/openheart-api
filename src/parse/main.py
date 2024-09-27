import focus
import sys
import pathlib

def main():
    file = pathlib.Path(sys.argv[1])
    content = file.read_text()
    parsed = focus.FocusStepSet().reduce(content)
    print('\n'.join(parsed))

if __name__ == '__main__':
    main()