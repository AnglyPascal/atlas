class Transferable:
    def __init__(self):
        self.transfers = []
    def getTransfers(self):
        return self.transfers
    def addTransfer(self, transfer):
        self.transfers.append(transfer)
    def sort(self):
        self.transfers.sort()
