class GameSettings(object):
    """GameSettings holds the general important properties"""
    # Tuple: (Required,Example Value (Default value for Required = False))
    URL = (True,"Local") # The URL the game should connect to
    DEBUG = (False, False)

    def __init__(self, *initial_data, **kwargs):
        # Write properties
        for dictionary in initial_data:
            for key in dictionary:
                if hasattr(self,key):
                    self.__setNewattr(key, dictionary[key])
        for key in kwargs:
            if hasattr(self,key):
                self.__setNewattr(key, kwargs[key])
        # Check input
        for prop in self.__dir__():
            if(isinstance(getattr(self, prop), tuple) and len(getattr(self, prop)) == 2):
                definition = getattr(self, prop)
                # Check required
                if(definition[0]):
                    raise ValueError("The property {0} is required, but was not set".format(prop))
                # Set not required to default
                setattr(self, prop, definition[1])

    def __setNewattr(self, key, value):
        definition = getattr(self, key)
        if(isinstance(value,type(definition[1]))):
            setattr(self, key, value)
        else:
            try: #Try to cast
                    CastedVal = type(definition[1])(value)
                    setattr(self, key, CastedVal)
            except (TypeError, ValueError) as e:
                raise TypeError("The property {0} supplied to GameSettings was of the wrong datatype, expected {1} got {2}".format(key,type(definition[1]),type(value)))
