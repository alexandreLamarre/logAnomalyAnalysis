import difflib

def debugStringDiff(a,b):
    """
    Debug string differences between string a and b

    https://stackoverflow.com/questions/17904097/python-difference-between-two-strings

    @type str a : the first string to compare
    @type str b : the second string to compare
    @rtype iostream output
    """
    print('{} => {}'.format(a,b))  
    for i,s in enumerate(difflib.ndiff(a, b)):
        if s[0]==' ': continue
        elif s[0]=='-':
            print(u'Delete "{}" from position {}'.format(s[-1],i))
        elif s[0]=='+':
            print(u'Add "{}" to position {}'.format(s[-1],i))    
    print()    