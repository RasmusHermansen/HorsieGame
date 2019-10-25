import Singleton;

class GameSettings(object, metaclass=Singleton.Singleton):
    ''' A singleton pattern implementing GameSettings '''
    # Tuple: (Required, Example Value)
    Url = (True,"Local") # The URL the game should connect to
    Height = (True, 1440) # Height in resolution
    Width = (True, 810) # Width in resolution
    Debug = (False, False) # True if Debug else false
    AntiAliasing = (False, 2) # 0 => None, 1 => Std, 2 => High 
    PlayMusic = (True, True);
    PlayEffects = (True, True);

    def __init__(self, *initial_data, **kwargs):
        # Write properties
        for dict in initial_data:
            for key in dict:
                if hasattr(self,key):
                    self.__setAttr(key, dict[key])
        for key in kwargs:
            if hasattr(self,key):
                self.__setAttr(key, kwargs[key])
        # Check input
        for prop in self.__dir__():
            if(isinstance(getattr(self, prop), tuple) and len(getattr(self, prop)) == 2):
                definition = getattr(self, prop)
                # Check required
                if(definition[0]):
                    raise ValueError("The property {0} is required, but was not set".format(prop))
                # Set not required to default
                setattr(self, prop, definition[1])

        Settings = self;

    def __setAttr(self, key, value):
        definition = getattr(self, key)
        if(isinstance(value,type(definition[1]))):
            setattr(self, key, value)
        else:
            try: #Try to cast
                    CastedVal = type(definition[1])(value)
                    setattr(self, key, CastedVal)
            except (TypeError, ValueError) as e:
                raise TypeError("The property {0} supplied to GameSettings was of the wrong datatype, expected {1} got {2}".format(key,type(definition[1]),type(value)))
