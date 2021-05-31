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
            f.write('\t'.join(list))
            f.write('\n')

    def ReadFile(self):
        with open(self.path) as f:
            print(f.read())

