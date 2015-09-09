#Requirements:
#    python (sudo apt-get install python)
#    pyopencl (sudo apt-get install python-pyopencl)
#    numpy (sudo apt-get install python-numpy)
#

platform_id = 1 #Set this to -1 to choose manually, or 0 if it isn't working









import pyopencl as cl
import numpy as np

class GPU:
    def __init__(self, filename=None):
        
        self.hasSetup = False
        
        if platform_id == -1:
            self.ctx = cl.create_some_context()
        else:
            platform = cl.get_platforms()
            
            gpus = platform[platform_id]\
                   .get_devices(device_type=cl.device_type.GPU)
            self.ctx = cl.Context(devices=gpus)
            
        self.queue = cl.CommandQueue(self.ctx)

        
        if filename == None:
            return
        self.open(filename)

    def open(self, filename):
        self.clCode = open(filename).read()
        
        self.program = cl.Program(self.ctx,
                                  self.clCode).build(
                                      ['-I \
/usr/include/x86_64-linux-gnu/c++/4.9/ -I /usr/include/x86_64-linux-gnu/\
-I /usr/include/c++/4.9'
                                       ])

    def readFromString(self, s):
        self.program = cl.Program(self.ctx,
                                  s).build(
                                      ['-I \
/usr/include/x86_64-linux-gnu/c++/4.9/ -I /usr/include/x86_64-linux-gnu/ \
-I /usr/include/c++/4.9'
                                       ])
    
    def setup(self, inputs, output):
        memflags = cl.mem_flags
        
        self.inputs = inputs
        
        self.inputbuffers = [
        cl.Buffer(self.ctx,
                  memflags.READ_ONLY | memflags.COPY_HOST_PTR,
                  hostbuf = inp)
        for inp in self.inputs]
        
        self.output = output
        
        self.outputbuffer = cl.Buffer(self.ctx, memflags.WRITE_ONLY,
                                      self.output.nbytes)

        self.hasSetup = True

    def run(self, functionName, globalSize, *args):

        if not self.hasSetup:
            raise Exception('GPU has not setup')

        exec 'self.program.' + functionName + '''(self.queue, globalSize, None,
*(self.inputbuffers + [self.outputbuffer]))'''
        
        
        
        cl.enqueue_read_buffer(self.queue, self.outputbuffer,
                               self.output).wait()

        return self.output
