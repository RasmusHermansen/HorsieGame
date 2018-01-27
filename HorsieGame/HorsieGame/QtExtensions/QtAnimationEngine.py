from enum import Enum;


class QtAnimationEngine():
    
    def __init__(self):
        self.ActiveAnims = [];

    def update(self):
        # Update animation and check if done
        self.ActiveAnims[:] = [animation for animation in self.ActiveAnims if not animation.process()]

    def addAnimation(self, animation, callback = None):
        self.ActiveAnims.append(self.animationContainer(animation, 0, callback));

    def addAnimationSequence(self, animations, loop = 0, callback = None):
        self.ActiveAnims.append(self.animationContainer(animations,loop,callback));


    class animationContainer(object):

        def __init__(self, animation, loop = 0, callback = None, **kwargs):

            self.animation = animation;
            self.loop = loop;
            self.callback = callback;

            if isinstance(animation, str):
                self.Sequence = True;
                self.idx = 0;
            else:
                self.Sequence = False;

        def process(self):
            if(self._update()):
                # check loop only if sequence
                if(self.loop>0 and self.Sequence):
                    self.idx = 0;
                    self.loop = self.loop -1;
                    return False;
                # check callback
                if(callable(self.callback)):
                    self.callback();
                return True;
            else:
                return False;

        def _update(self):
            # If sequence update and check if last part
            if(self.Sequence):
                if(self.animation(self.idx)._Update()):
                    self.idx = self.idx + 1;
                    if(self.idx >= len(self.animation)):
                        return True;
            # Else just update and return whether finished
            else:
                return self.animation._Update();