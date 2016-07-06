__author__ = 'Nick'
from negotiator_base import BaseNegotiator
from Tkinter import *
import matplotlib

matplotlib.use('TkAgg')



class negotiatorUI(BaseNegotiator):

    def __init__(self):
        ##set up window here
        self.window = Tk()
        self.window.geometry("500x500+300+100")
        self.window.title("Human Negotiator")
        self.buttonlist = []
        self.madeoffer = False
        BaseNegotiator.__init__(self)
        self.checkstate = []
        self.currUtility = StringVar()
        self.lastOffer = StringVar()
        self.theirUtility = "0"

    def initialize(self, preferences, iter_limit):
        ##add all items to window
        self.preferences = preferences
        latestOffer = Label(self.window, textvariable = self.lastOffer).pack()
        currentUtility = Label(self.window, textvariable=self.currUtility).pack()
        self.currUtility.set("Your Share's Utility: 0")
        self.lastOffer.set("None")
        i = 0
        for x in self.preferences:
            y = self.preferences.get(x,0)
            print str(y)
            buttonvar = IntVar()
            self.buttonlist.append(buttonvar)
            newCheckbutton = Checkbutton(self.window, text = str(x) + " = " + str(y),variable = self.buttonlist.__getitem__(i), command = self.updateItem).pack()
            i+=1
        sendButton = Button(self.window, text = "Send Offer",command = self.sendoffer).pack()
        BaseNegotiator.initialize(self, preferences, iter_limit)

    def updateItem(self):
            self.checkCheckboxes()


    def sendoffer(self):
        self.madeoffer=True
        self.window.quit()

    def make_offer(self, offer):
        self.madeoffer = False
        self.offer = offer
        self.lastOffer.set("They want " + str(self.offer) + " for an estimated " + self.theirUtility)
        if offer is None:
            self.offer = []
        self.window.mainloop()
        while(not self.madeoffer):
            x = 1
        return self.offer

    def receive_utility(self, utility):
        ##write opponents utility from last offer
        self.theirUtility = str(utility)

    def receive_results(self, results):
        BaseNegotiator.receive_results(self, results)

    def utility(self):
        x = BaseNegotiator.utility(self)
        return x

    def checkCheckboxes(self):
            temp = 0
            i = 0
            self.offer = []
            for x in self.preferences:
                if(self.buttonlist[i].get()>0):
                    self.offer.append(x)
                temp+=self.buttonlist[i].get()*self.preferences.get(x,0)
                i+=1

            string = str(temp)
            print string
            print str(self.offer)
            self.currUtility.set("Your Share's Utility: " + string)



