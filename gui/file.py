import csv


class FileOp():
    def __init__(self):
        self.path = '../param/GainParam.txt'

    def reset_char(self):
        with open(self.path, mode='w') as f:
            f.write("")

    def write_char(self, str):
        with open(self.path, mode='a') as f:
            f.write(str, "\n")

    def write_list(self, list):
        with open(self.path, mode='a') as f:
            f.write('\t'.join([str(float(j)) for j in list]))
            f.write('\n')

    def read_char(self):
        with open(self.path) as f:
            print(f.read())

    def read_list(self):
        with open(self.path, mode='r') as f:
            read_data = [row for row in csv.reader(f, delimiter="\t")]
            return read_data
