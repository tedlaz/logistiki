import sys
import shutil
import zipfile
from pathlib import Path


class ZipProcessor:
    def __init__(self, zipname: str) -> None:
        self.zipname = zipname
        self.temp_directory = Path(f"unzipped-{zipname[:-4]}")

    def process_zip(self):
        self.unzip_files()
        self.process_files()
        self.zip_files()

    def process_files(self):
        raise NotImplementedError("Has to be implemented on child")

    def unzip_files(self):
        self.temp_directory.mkdir()
        with zipfile.ZipFile(self.zipname) as zip:
            zip.extractall(self.temp_directory)

    def zip_files(self):
        with zipfile.ZipFile(self.zipname, "w") as fil:
            for filename in self.temp_directory.iterdir():
                fil.write(filename, filename.name)
        shutil.rmtree(self.temp_directory)


class ZipReplace(ZipProcessor):
    def __init__(self, filename, search: str, replace: str) -> None:
        super().__init__(filename)
        self.search_string = search
        self.replace_string = replace

    def process_files(self):
        for filename in self.temp_directory.iterdir():
            with filename.open() as fil:
                contents = fil.read()
            contents = contents.replace(
                self.search_string, self.replace_string)
            with filename.open("w") as fil:
                fil.write(contents)


if __name__ == "__main__":
    ZipReplace(*sys.argv[1:4]).process_zip()
