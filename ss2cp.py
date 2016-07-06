from negotiator_base import BaseNegotiator
from random import random
from functools import wraps
import random


# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class ss2cp(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.




    # a getter method to get the maxTurns
    def getTurns(self):
        return self.iter_limit

    # a counter method to keep track of the currentTurn
    def counter(func):
        @wraps(func)
        def tmp(*args, **kwargs):
            tmp.count += 1
            return func(*args, **kwargs)

        tmp.count = 0
        return tmp

    # initialize a global variable to store the maxTurns
    maxTurns = 0

    oppo_dict = {}

    def oppoEstimation(self, offer):
        # type: (object) -> object
        global oppo_dict
        if self.offer is not None:
            for item in offer:
                if oppo_dict is None:
                    oppo_dict = {
                        item: 1
                    }
                else:
                    if item not in oppo_dict:
                        oppo_dict[item] = 1
                        return oppo_dict
                    else:
                        oppo_dict[item] += oppo_dict[item]
                        return oppo_dict

    @counter
    def make_offer(self, offer):
        global maxTurns
        global oppo_dict
        # print the number of current turn
        print self.make_offer.count
        # get the current turn
        currentTurn = self.make_offer.count
        # default method to get the offer
        self.offer = offer

        totalReward = 0;
        ordering = self.preferences
        for item in ordering.keys():
            totalReward += ordering.get(item)

        if currentTurn is 1:
            if offer is None:
                maxTurns = ss2cp.getTurns(self) + 1
                print "[SS}ss2cp starts first, max turns is " + str(maxTurns)
                # then there will be an extra chance to accept an offer in the end
                ourOffer = []
                totalOffer = 0
                # store keys in another list to shuffle
                keys = list(ordering.keys())
                random.shuffle(keys)

                for item in keys:
                    totalOffer += ordering.get(item)
                    if totalOffer < (totalReward / 3 * 2):
                        ourOffer = ourOffer + [item]
                    else:
                        ourOffer = ourOffer + [item]
                        break
                self.offer = ourOffer

                print "[SS]ss2cp will take: " + str(ourOffer) + ". My utility will be " + str(self.utility())

                return self.offer

            if offer is not None:
                maxTurns = ss2cp.getTurns(self)
                print "[SS}ss2cp starts second, incrementing the max turn by 1, max turns is " + str(maxTurns)
                # then there will be no extra chance to accept an offer in the end

        # to see if it is the last turn, and accept what ever offer
        if currentTurn is maxTurns:
            self.offer = offer
            self.offer = BaseNegotiator.set_diff(offer)
            print "[SS}Last chance to make offer, will accept any offer" + str(self.offer)
            return self.offer

            oppo_dict = self.oppoEstimation(offer)
            print "oppo_dict: " + str(oppo_dict)

        if offer is not None:
            # Very important - we save the offer we're going to return as self.offer
            # print "ss2cp agree that you can take " + str(self.offer)
            # offerDiff = BaseNegotiator.set_diff(self)
            print "[SS]ss2cp will take: " + str(self.offer) + ". My utility will be " + str(self.utility())
            return self.offer
