# global validate map
validate = {}
        
def register_validator(func,callback):
    validate[func] = callback



#### VALIDATORS ####
"""
A little bit about validators:

Validator is a function, that checks the correctnes of answer.
If it is written in a form 'text://bla', it uses validator 
'text', passing 'bla' as an 'extra' argument. 

Other arguments are user id, question object ,answer object and input.

"""

def text(user,q,input,extra):
    """
    Does a case sensitive string compare.
    """
    return input == extra

def itext(user,q,input,extra):
    """
    Does a case INsensitive string compare.
    """
    return input.lower() == extra.lower()


def always(user,q,input):
    """
    Always returns True.
    """
    return True

def never(user,q,input):
    """
    Always returns False.
    """
    return False

def true(user,q,input):
    """
    Returns true if input=True, else false
    """
    return input

def false(user,q,input):
    """
    Returns true if input=False, else false
    """
    return not input

register_validator('text',text)
register_validator('itext',itext)
register_validator('always',always)
register_validator('never',never)
register_validator('true',true)
register_validator('false',false)

import statistika
register_validator('nal1_b', statistika.nal1_b)
