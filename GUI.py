import matplotlib
import numpy as np
matplotlib.use('TkAgg')

##GUI Class: Responsible for Displaying All of the Information about Round Results
##In a future update, this will also house the UserInterface for playing against an AI
class GUI():

    # init(self : GUI)
        #Sets the initial fields for the GUI class
    def __init__(self):
        self.A_Round_Results = [0]
        self.B_Round_Results = [0]
        self.num_Rounds = [0]

    # make_final_round_graph(self : GUI)
        #Makes the Graph of the Cumulative results from all of the rounds
    def make_post_round_graph(self,A_Utility,B_Utility,rounds,results):

        if(len(self.num_Rounds)>0):
            self.num_Rounds.append(self.num_Rounds[len(self.num_Rounds)-1]+1)
            self.A_Round_Results.append(self.A_Round_Results[len(self.A_Round_Results)-1] + results[1])
            self.B_Round_Results.append(self.B_Round_Results[len(self.B_Round_Results)-1] + results[2])
        else:
            self.num_Rounds.append(1)
            self.A_Round_Results.append(results[1])
            self.B_Round_Results.append(results[2])

        matplotlib.pyplot.scatter(rounds,A_Utility)
        matplotlib.pyplot.plot(rounds,A_Utility)
        matplotlib.pyplot.scatter(rounds,B_Utility)
        matplotlib.pyplot.plot(rounds,B_Utility)
        matplotlib.pyplot.ylabel("Utility")
        matplotlib.pyplot.xlabel("Turn")
        matplotlib.pyplot.title("Round Summary")
        matplotlib.pyplot.xticks(np.arange(1, len(B_Utility)+1, 1.0))
        matplotlib.pyplot.show()

    # make_final_round_graph(self : GUI)
        #Makes the Graph of the Cumulative results from all of the rounds
    def make_final_round_graph(self):

        matplotlib.pyplot.scatter(self.num_Rounds,self.A_Round_Results)
        matplotlib.pyplot.plot(self.num_Rounds,self.A_Round_Results)
        matplotlib.pyplot.scatter(self.num_Rounds,self.B_Round_Results)
        matplotlib.pyplot.plot(self.num_Rounds,self.B_Round_Results)
        matplotlib.pyplot.ylabel("Utility")
        matplotlib.pyplot.xlabel("Round")
        matplotlib.pyplot.title("Final Summary")
        matplotlib.pyplot.xticks(np.arange(0, max(self.num_Rounds)+1, 1.0))
        matplotlib.pyplot.show()