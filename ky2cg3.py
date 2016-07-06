# Ketao Yin, Shaoran Sun
# ky2cg, ss2cp

from negotiator_base import BaseNegotiator
from functools import wraps


class ky2cg(BaseNegotiator):
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
    # declare a global dict to keep track for opponent's moves
    oppo_dict = {}

    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
    @counter
    def make_offer(self, offer):
        self.offer = offer
        global maxTurns
        global oppo_dict
        # print the number of current turn
        print self.make_offer.count
        # get the current turn
        currentTurn = self.make_offer.count

        # update opponent's offer in our tracker

        oppo_dict = self.oppoEstimation(offer)
        print "oppo_dict: " + str(oppo_dict)

        if currentTurn is 1:
            if offer is None:
                # If going first, first turn decision = offer all positive util items
                maxTurns = ky2cg.getTurns(self) + 1
                print "[SS}ss2cp starts first, incrementing the max turn by 1, max turns is " + str(maxTurns)
                # then there will be an extra chance to accept an offer in the end
                self.offer = self.positiveItems()
                print "[SS]ss2cp will take: " + str(self.offer) + ". My utility will be " + str(self.utility())
                return self.offer

            if offer is not None:
                maxTurns = ky2cg.getTurns(self)
                print "[SS}ss2cp starts second, max turns remains " + str(maxTurns)
                # then there will be no extra chance to accept an offer in the end

        # to see if it is the last turn, and accept what ever offer
        if currentTurn is maxTurns:
            if currentTurn > ky2cg.getTurns(self):
                # then you are to accept the final offer

                self.offer = offer
                self.offer = BaseNegotiator.set_diff(self)

                if (self.utility() >= (self.totalUtility() / 3)):
                    print "[SS]Last chance to accept offer, will accept any offer more than 1/3 of my total utility: " + str(
                        self.offer) + " vs " + str(
                        offer) + ". My utility will be " + str(self.utility()) + ". total/3 is " + str(
                        self.totalUtility() / 3)
                    return self.offer

                else:
                    self.offer = BaseNegotiator.set_diff(self)
                    print "You bad!!! I'd rather get negative leward!!!!"
                    return self.offer
            else:
                # then you are to give the final offer
                print "[SS]Last chance to give offer, will take more than 2/3 of my total utility"
                print "oppo_dict: " + str(oppo_dict)
                total = 0
                ourOffer = []
                # look at the nonoffered items first
                ordering = self.preferences
                for item in ordering.keys():
                    if not oppo_dict:
                        break
                    if (item not in oppo_dict and ordering.get(item) >= 0):
                        ourOffer = ourOffer + [item]
                        total += ordering.get(item)
                        print "Found an item that opponent never wanted, " + str(
                            item) + ". It's value is positive, taking it. That give me total of " + str(total)
                        if (total >= (2 / 3 * self.totalUtility())):
                            self.offer = ourOffer
                            print "[SS]ss2cp will take: " + str(ourOffer) + ". My utility will be " + str(
                                self.utility())
                            return self.offer

            while total < (2 / 3 * self.totalUtility()):
                min = min(oppo_dict, key=oppo_dict.get)
                ourOffer = ourOffer + min
                total += oppo_dict.get(min)
                del oppo_dict[min]
            self.offer = ourOffer
            print "[SS]ss2cp will take: " + str(ourOffer) + ". My utility will be " + str(
                self.utility())
            return self.offer

        if offer is not None:
            # Very important - we save the offer we're going to return as self.offer
            self.offer = offer
            # If so, accept, negotiation is completed!
            if self.acceptableOffer() is True:
                print("OFFER ACCEPTABLE!!! TAKING IT!!!!")
                self.offer = BaseNegotiator.set_diff(self)
                # self.offer = self.positiveRemainingItems()
                return self.offer

            # Else, return more favorable offer to opponent
            else:  # Opponent offer currently takes more than half of total utilities
                print("ARRANGING COUNTER OFFER!!!!!!!!!!")
                currOffer = offer  # Save opponent offer to modify
                self.offer = BaseNegotiator.set_diff(self)
                ourOffer = self.positiveRemainingItems(
                )  # Instantiate our offer, currently < 1/2 * total utilities
                ourOfferUtil = 0  # Track our offer's utility

                for s in ourOffer:
                    ourOfferUtil += self.preferences.get(s, 0)

                # Loop: while our offer is still < 2/3 of total utility
                while ourOfferUtil < (2 * self.totalUtility() / 3):
                    if len(currOffer) > 0:
                        maxItem = self.maxItem(currOffer)  # Find min item in opponent's offer
                        ourOffer = ourOffer + [maxItem]
                        ourOfferUtil += self.preferences.get(maxItem, 0)
                        currOffer.remove(maxItem)
                    else:
                        break

                print("COUNTER OFFER: ")
                for s in ourOffer:
                    print(s)

                self.offer = ourOffer
                print "[SS]ss2cp will take: " + str(self.offer) + ". My utility will be " + str(self.utility())
                return self.offer

    # the real method to update opponent's moves
    def oppoEstimation(self, offer):
        # type: (object) -> object
        global oppo_dict

        if offer:
            for item in offer:
                if not self.oppo_dict:
                    # if it is empty
                    self.oppo_dict = {
                        item: 1
                    }
                else:
                    if item not in self.oppo_dict:
                        self.oppo_dict[item] = 1
                    else:
                        self.oppo_dict[item] += 1
        return self.oppo_dict

    # Return set of all positive utility items in an offer
    def positiveRemainingItems(self):
        ourOffer = []
        for item in self.offer:
            if self.preferences.get(item, 0) > 0:
                ourOffer = ourOffer + []
        return ourOffer

    # Returns set of all positive utility items
    def positiveItems(self):
        ourOffer = []
        for item in self.preferences:
            if self.preferences.get(item, 0) > 0:
                ourOffer = ourOffer + [item]
        return ourOffer

    # Returns true if the opponent's offer provides me with more than 1/3 of total utility available
    def acceptableOffer(self):
        acceptable = False
        current = self.offerUtility()
        total = self.totalUtility()
        if current < (total / 3):
            acceptable = True
        return acceptable

    # Returns current total utility in self.offer
    def offerUtility(self):
        util = 0
        for s in self.offer:
            util += self.preferences.get(s, 0)
        return util

    # Returns total utility of all items possible
    def totalUtility(self):
        util = 0
        for s in self.preferences:
            util += self.preferences.get(s, 0)
        return util

    # Find max-value item opponent's offer, using self.preferences
    def maxItem(self, currOffer):
        maxItem = currOffer[0]
        for s in currOffer:
            if self.preferences.get(s, 0) > self.preferences.get(maxItem):
                maxItem = s
        return maxItem

    # Prints my preferences (utility values)
    def printPreferences(self):
        for i in (self.preferences):
            print(self.preferences.get(i))

    # Returns number of items total
    def numItems(self):
        i = 0
        for j in (self.preferences):
            i = i + 1
        return i
