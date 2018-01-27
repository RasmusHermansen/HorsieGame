
delta = 1e-10;

class LinearPath(object):
    ''' Animate a simple linear path '''

    def __init__(self, obj, fromX, fromY, toX, toY, length):
        self.toX = toX;
        self.toY = toY;
        self.length = length;
        self.gradX = (toX-fromX)/length;
        self.gradY = (toY-fromY)/length;
        self.obj = obj;
        self.updates = 0;

        self.obj.setPos(fromX,fromY);

    def _Update(self):
        self.updates = self.updates + 1;
        # Move
        self.obj.moveBy(self.gradX,self.gradY)

        # Check if done
        if(self.updates >= self.length):
            return True;
        return False;

class SlowingLinearPath(LinearPath):
    ''' Animate a simple linear path with decaying speed '''

    def __init__(self, obj, fromX, fromY, toX, toY, length):
        super().__init__(obj, fromX, fromY, toX, toY, length)

        self.smoothing = -0.5e-5;
        # Take advantage of gradX, weight movements s.t they sum to length => We are at terminal point.
        # Solve sum of 2nd order equations
        self.c = (self.smoothing*(length*(length+1)*(2*length+1)/6)-self.length)/self.length

    def _Update(self):
        self.updates = self.updates + 1;
        w = pow(self.updates,2)*self.smoothing-self.c;
        # Move
        self.obj.moveBy(self.gradX*w,self.gradY*w);

        # Check if done
        if(self.updates >= self.length):
            return True;
        return False;