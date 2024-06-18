import re

path_data = "./imagedata"


def remove_non_alphanumeric(text):
    return re.sub(r'[^a-zA-ZА-Яа-я ,.-]', '', text)


def main(result: str):
    with open(f"{path_data}/{result}.txt", "r", encoding="utf-8") as file:
        result = remove_non_alphanumeric(file.read())
    return result


if __name__ == '__main__':
    print(main("tomato_late_blight"))

