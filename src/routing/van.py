class Van(object):
    """
    Simple class for vans.
    """

    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return self.name
