from PyQt5.QtWidgets import QWidget

class BasicWidget(object):
    """ A basic widget, implement setupUi to decorate the widget """    


    def __init__(self):
        self.Widget = QWidget()
        self.setupUi(self.Widget)

    def getWidget(self):
        return self.Widget