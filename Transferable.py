class Transferable:
    def __init__(self):
        self.transfers = set()
    def getTransfers(self):
        return self.transfers
    def addTransfer(self, transfer):
        self.transfers.add(transfer)
    def num_of_transfers(self):
        return len(self.transfers)
    def sort(self):
        self.transfers = sorted(self.transfers)
