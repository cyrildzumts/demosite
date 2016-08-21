
class QuantityError(Exception):
    def __init__(self, available, value):
        self.message = "Quantity Error.\n\
            Quantity Available = %d\n\
            Quantity Requested %d\n" % (available, value)

    def __str__(self):
        return self.message
