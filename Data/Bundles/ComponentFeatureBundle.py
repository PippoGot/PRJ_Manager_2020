from .AbstractFeatureBundle import AbstractFeatureBundle

class ComponentFeatureBundle(AbstractFeatureBundle):
    """
    self.numberID
    self.name
    self.description
    self.comment

    self.packageQuantity
    self.quantity
    self.price

    self.type
    self.manufacture
    self.status

    self.seller
    self.link
    """

    def __init__(self, **features):
        """
        Initialise the basic component properties to None.
        """

        self.featureList = COMPONENT_VALUES

        self.addEmptyFeatures(*COMPONENT_VALUES)

        self.addFeatures(**features)

    def addFeature(self, featureKey, featureValue):
        """
        Reimplements the superclass method to check that a different feature is not
        added to the node.

        Args:
            featureKey (str): the feature to add
            featureValue (PyObject): the value of the feature
        """

        if featureKey not in self.featureList: return
        super().addFeature(featureKey, featureValue)

COMPONENT_VALUES = [
    'numberID',
    'name',
    'description',
    'comment',
    'packageQuantity',
    'quantity',
    'price',
    'type',
    'manufacture',
    'status',
    'seller',
    'link'
]


# TEST CODE
if __name__ == '__main__':
    pass