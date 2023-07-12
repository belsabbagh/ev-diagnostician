from src.config import paths
from os import listdir, path
from shutil import rmtree

validate = lambda x: x in ["y", "n", "Y", "N"]

if __name__ == "__main__":
    valid = False
    while not valid:
        confirm = input("Are you sure you want to clear the generated data? (y/n) ")
        valid = validate(confirm)
    if confirm == "n":
        exit(0)
    if confirm == "y":
        print("Clearing generated data...")
        for folder in listdir(paths.GENERATED_PATH):
            rmtree(path.join(paths.GENERATED_PATH, folder))
        print("Done.")
