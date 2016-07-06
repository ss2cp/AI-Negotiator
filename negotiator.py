from negotiator_base import BaseNegotiator
from random import random


# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class Negotiator(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
    def make_offer(self, offer):
        self.offer = offer
        if random() < 0.1 and offer is not None:
            # Very important - we save the offer we're going to return as self.offer
            print "[RN]Random Negotiator agree that you can take " + str(self.offer)
            self.offer = BaseNegotiator.set_diff(self)
            print "[RN]Negotiator will take: " + str(self.offer)
            return self.offer
        else:
            ordering = self.preferences
            ourOffer = []
            for item in ordering.keys():
                if random() < 0.5:
                    ourOffer = ourOffer + [item]
            print "[RN]Random Negotiator made an offer" + str(ourOffer)
            self.offer = ourOffer
            return self.offer
