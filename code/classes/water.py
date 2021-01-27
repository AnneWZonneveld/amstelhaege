###############################################################################
# water.py
#
# Programmeertheorie
# Anne Zonneveld, Fleur Tervoort, Seike Appold
#
# - A class to create Water instances.
###############################################################################


class Water():
    def __init__(self):
        self.coordinates = {}
        self.id = None
        

    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        
        return f"Water_{self.id}"