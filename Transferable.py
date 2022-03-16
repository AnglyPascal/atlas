class Transferable:
    def __init__(self):
        self.transfers = set()
        self.value_without_loan = 0
        self.value_with_loan = 0
    def getTransfers(self):
        return self.transfers
    def addTransfer(self, transfer):
        self.transfers.add(transfer)
        self.value_with_loan += transfer.fee
        if not transfer.isLoan:
            self.value_without_loan += transfer.fee
    def num_of_transfers(self):
        return len(self.transfers)
    def sort(self):
        self.transfers = sorted(self.transfers)
