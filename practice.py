x = {'a': 'b', 'b': 'c'}

def decorator(**kw):
    def trytoplot(func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except:
                print "It didn't work" + kw['z']
            else:
                print 'It did work'
        return inner
    return trytoplot
    
@decorator(z='aaa')
def hello(y):
    print y['c']

hello(x)

print hello.__name__
