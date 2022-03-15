class Transferable:
    def __init__(self):
        self.transfers = []
        self.num_of_transfers = 0
    def getTransfers(self):
        return self.transfers
    def addTransfer(self, transfer):
        self.transfers.append(transfer)
        self.num_of_transfers += 1
    def sort(self):
        self.transfers.sort()
