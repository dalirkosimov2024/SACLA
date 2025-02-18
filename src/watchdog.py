import sys
import time

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv)>1 else '.'
    print(path)
