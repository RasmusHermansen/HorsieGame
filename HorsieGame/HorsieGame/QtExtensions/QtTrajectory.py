
delta = 1e-10;

class LinearMovement(object):
    ''' Animate a simple linear path '''

    def __init__(self, obj, distanceX, distanceY, steps):
        self.steps = steps;
        self.gradX = distanceX/steps;
        self.gradY = distanceY/steps;
        self.obj = obj;
        self.updates = 0;

    def _Update(self):
        self.updates = self.updates + 1;
        # Move
        self.obj.moveBy(self.gradX,self.gradY)

        # Check if done
        if(self.updates >= self.steps):
            return True;
        return False;

class LoopingLinearPath(LinearMovement):
    ''' Animate a simple linear path, upon reaching end return to start and repeat '''
    def __init__(self, obj, fromX, fromY, toX, toY, steps):
        super().__init__(obj, toX-fromX, toY-fromY, steps)
        self.fromX = fromX;
        self.fromY = fromY;
        self.firstcall = True;

    def _Update(self):
        if self.firstcall:
            self.obj.setPos(self.fromX,self.fromY);
            self.firstcall = False;

        if(super()._Update()):
            self.updates = 0;
            self.obj.setPos(self.fromX,self.fromY);
        return False;

class SlowingLinearPath(LinearMovement):
    ''' Animate a simple linear path with decaying speed '''

    def __init__(self, obj, distanceX, distanceY, steps):
        super().__init__(obj, distanceX, distanceY, steps)

        self.smoothing = -0.5e-5;
        # Take advantage of gradX, weight movements s.t they sum to steps => We are at terminal point.
        # Solve sum of 2nd order equations
        self.c = (self.smoothing*(steps*(steps+1)*(2*steps+1)/6)-self.steps)/self.steps

    def _Update(self):        
        self.updates = self.updates + 1;
        w = pow(self.updates,2)*self.smoothing-self.c;
        # Move
        self.obj.moveBy(self.gradX*w,self.gradY*w);

        # Check if done
        if(self.updates >= self.steps):
            return True;
        return False;

class Rotate(object):

    def __init__(self, obj, amount, steps):
        self.amount = amount/steps;
        self.steps = steps;
        self.obj = obj;

        self.updates = 0;

        self.obj.setTransformOriginPoint(self.obj.boundingRect().center())
        
    def _Update(self):
        self.obj.setRotation(self.obj.rotation()+self.amount)
        self.updates = self.updates + 1;
        # Check if done
        if(self.updates >= self.steps):
            return True;
        return False;

class Swing(Rotate):

    def __init__(self, obj, amount, steps):
        self.firstCall = False;
        super().__init__(obj, amount, steps);

    def _Update(self):
        if(super()._Update()):
            self.updates = 0;
            self.amount = -self.amount;
            if self.firstCall:
                self.amount = self.amount*2;
                self.steps = self.steps*2;
        return False;
