from negotiator_base import BaseNegotiator
from random import random


# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class ss2cp(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
    def make_offer(self, offer):
        self.offer = offer
        if random() < 1 and offer is not None:
            # Very important - we save the offer we're going to return as self.offer
            #print "ss2cp agree that you can take " + str(self.offer)
            #self.offer = BaseNegotiator.set_diff(self)
            print "ss2cp will take: " + str(self.offer) + ". My utility will be " + str(self.utility())
            return self.offer
        else:
            ordering = self.preferences
            print ordering
            ourOffer = []
            for item in ordering.keys():
                if random() < .5:
                    ourOffer = ourOffer + [item]
            self.offer = ourOffer
            return self.offer
