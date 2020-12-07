class AbstractFeatureBundle():
    """
    Class to store an arbitrary number of parameters and to manage them in a
    non confusing way.

    self.featureList
    """

    def __init__(self, **features):
        """
        Creates the list parameter and stores any feature key passed in.
        """

        self.featureList = []

        self.addFeatures(**features)

# FEATURES HANDLING

    def addFeature(self, featureKey, featureValue):
        """
        Adds a single feature to this bundle.

        Args:
            featureKey (str): the key of the value (realistically it's name)
            featureValue (PyObject): the item to store under the given key
        """

        if featureKey not in self.featureList:
            self.featureList.append(featureKey)

        setattr(self, featureKey, featureValue)

    def addFeatures(self, **features):
        """
        Adds an arbitrary number of features, passed in by keyword arguments.
        """

        for featureKey, featureValue in features.items():
            self.addFeature(featureKey, featureValue)

    def addEmptyFeature(self, featureKey):
        """
        Adds an empty feature (featureKey: None).

        Args:
            featureKey (str): the name of the feature
        """

        self.addFeature(featureKey, None)

    def addEmptyFeatures(self, *featureKeys):
        """
        Adds an arbitrary number of empty features.
        """

        for featureKey in featureKeys:
            self.addEmptyFeature(featureKey)

    def updateFeature(self, featureKey, featureValue):
        """
        Same as addFeature. Implemented for the more appropriate name.

        Args:
            featureKey (str): the key of the value (realistically it's name)
            featureValue (PyObject): the item to store under the given key
        """

        self.addFeature(featureKey, featureValue)

    def deleteFeature(self, featureKey):
        """
        Deletes an existing feature from the bundle. If the feature does not exist
        an error is printed but no exception is thrown.

        Args:
            featureKey (str): the feature to delete if it exists
        """

        delattr(self, featureKey)
        self.featureList.remove(featureKey)

    def deleteFeatures(self, *featureKeys):
        """
        Deletes an arbitrary number of features from this bundle.
        """

        for featureKey in featureKeys:
            self.deleteFeature(featureKey)

    def getFeature(self, featureKey):
        """
        Returns the value of a feature in this bundle if it exists. If the the
        feature doesn't exist an error is printed but no exceptions are thrown
        and None is returned.

        Args:
            featureKey (str): the feature to return

        Returns:
            PyObject: the value under the given featureKey
        """

        return getattr(self, featureKey, None)

# COPY

    def copy(self):
        """
        Returns a copy of this bundle instance. The features are completely independent
        from the copied versions.

        Returns:
            AbstractFeatureBundle: the copied bundle
        """

        newBundle = self.__class__()
        features = self.getBundleDictionary().copy()
        newBundle.addFeatures(**features)
        return newBundle

# REPRESENTATION

    def toString(self):
        """
        Creates and treturns a string to represent this object. It consist in a list
        of keys and values.

        Returns:
            str: the string representing this item
        """

        bundleDictionary = self.getBundleDictionary()
        outputString = ''
        for featureKey, featureValue in bundleDictionary.items():
            outputString += f'{featureKey}: {featureValue}\n'
        return outputString

    def getBundleDictionary(self):
        """
        Returns the dictionary with this bundle's feature keys and values.

        Returns:
            dict[str, PyObject]: the dictionary with this bundle's values
        """

        return self.getSelectedFeatures(*self.featureList)

    def getSelectedFeatures(self, *featureKeys):
        """
        Returns the dictionary with this bundle's feature keys and values from the selected
        ones.

        Returns:
            dict[str, PyObject]: the dictionary with this bundle's values
        """

        bundleDictionary = {}
        for featureKey in featureKeys:
            featureValue = self.getFeature(featureKey)
            if featureValue:
                bundleDictionary[featureKey] = featureValue
        return bundleDictionary

    def getBundleKeys(self):
        """
        Returns the list of the features stored in this bundle.

        Returns:
            list[str]: the list of featureKeys
        """

        return self.featureList

    def getBundleValues(self):
        """
        Returns the list of the values stored in this bundle.

        Returns:
            list[PyObjects]: the list of values of this bundle
        """

        valuesList = []
        for featureKey in self.featureList:
            valuesList.append(self.getFeature(featureKey))
        return valuesList

# DUNDERS

    def __repr__(self):
        return self.toString()

    def __str__(self):
        return self.toString()


# TEST CODE
if __name__ == '__main__':
    pass