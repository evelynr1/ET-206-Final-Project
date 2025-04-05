import os


def get_api_key(filename):
    # source_dir = os.path.dirname(__file__)
    # full_path = os.path.join(source_dir, filename)
    # with open(full_path) as f:
    with open(filename) as f:
        return f.read()

def call_api():
    harvard_api_key = get_api_key("Harvard_API_KEY.txt")


def main():
    #harvard_api_key = get_harvard_api_key()
    call_api()

if __name__ == "__main__":
    main()
