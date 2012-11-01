import validator_core

from os import listdir

imports = listdir(locals()['__path__'][0])

for bla in [ i for i in imports if i.endswith(".py")]:
    if not bla.startswith("__") and not bla.startswith(".") :
        try:            
            __import__(bla[:-3],globals(),'',[])
        except ImportError:
            pass
