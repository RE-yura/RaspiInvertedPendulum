import csv


class FileOp():
    def __init__(self):
        self.path = './GainParam.txt'

    def ResetChar(self):
        with open(self.path, mode='w') as f:
            f.write("")

    def WriteChar(self, str):
        with open(self.path, mode='a') as f:
            f.write(str, "\n")

    def WriteList(self, list):
        with open(self.path, mode='a') as f:
            f.write('\t'.join([str(float(j)) for j in list]))
            f.write('\n')

    def ReadChar(self):
        with open(self.path) as f:
            print(f.read())

    def ReadList(self):
        with open(self.path, mode='r') as f:
            read_data = [row for row in csv.reader(f, delimiter="\t")]
            return read_data
