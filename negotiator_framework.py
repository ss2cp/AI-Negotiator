##Negotiator-Framework
##Main file for running negotiations between two negotiators

from csv import DictReader
from sys import argv, exit

from ky2cg3 import ky2cg
from negotiator import Negotiator
from ss2cp import ss2cp
from random import randint

##GUI Related Imports
import matplotlib
matplotlib.use('TkAgg')
import pylab
import matplotlib.pylab as plt
from GUI import GUI
g = GUI()

#set_diff(a: list, b: list)
    #Performs the set difference of sets A and B and returns it
def set_diff(a,b):
    B = set(b)
    return [aa for aa in a if aa not in B]

# read_scenario(parameterfile_name : String) --> (int, list(dict))
    # Utility function to read in a single scenario from a csv file
    # Expects a single int on the first line, specifying the iteration limit,
    # and then an arbitrary number of rows of three comma-separated columns,
    # specifying the name of each item, its rank (where 1 is best) for negotiator A,
    # and the same for negotiator B
def read_scenario(parameterfile_name):
    # Open the file for reading
    with open(parameterfile_name, 'r') as parameterfile:
        # Consume the first line, getting the iteration limit
        number_iterations = parameterfile.readline()
        return (
                int(number_iterations),
                # Use Python's builtin CSV reader to read the rest of the file as specified
                list(DictReader(parameterfile, fieldnames=["item_name", "negotiator_a", "negotiator_b"]))
                )
# end_of_round_graph(negotiator_a: negotiator, negotiator_b: negotiator, list: list of items)
    #formats information about the round to be turned into a graph
def end_of_round_graph(negotiator_a,negotiator_b,list):
    numrounds = []
    A_Utility = []
    B_Utility = []
    i = 0;
    for x in list:
        i+=1
        numrounds.append(i)
        As_items = x[0]
        Bs_items = x[1]
        negotiator_a.offer = As_items
        negotiator_b.offer = Bs_items
        A_Utility.append(negotiator_a.utility())
        B_Utility.append(negotiator_b.utility())
    return (A_Utility,B_Utility,numrounds)

# negotiate(num_iterations :  Int, negotiator_a : BaseNegotiator, negotiator_b : BaseNegotiator) --> (Boolean, list(String), Int)
    # The main negotiation function, responsible for running a single scenario & coordinating interactions between the two
    # negotiators.
def negotiate(num_iterations, negotiator_a, negotiator_b, items):
    # Get the initial offer from negotiator a - we pass in None to signify that no previous opposing offers have been made
    offersList = []
    (offer_a, offer_b) = (negotiator_a.make_offer(None), None)
    offersList.append([set(offer_a),set(items) - set(offer_a)])

    # We scale the reported utility by a random factor
    a_scale = randint(1, 11)
    b_scale = randint(1, 11)

    # Keep trading offers until we reach an agreement or the iteration limit, whichever comes first
    for i in range(num_iterations):

        # Get from each negotiator the utility it received from the offer it most recently gave
        utility = (a_scale * negotiator_a.utility(), b_scale * negotiator_b.utility())
        # Send b the latest offer from a and allow it to rebut
        negotiator_b.receive_utility(utility[0])
        offer_b = negotiator_b.make_offer(offer_a)

        # We signify agreement by both offers being structurally equal
        if set(offer_b) == (set(items) - set(offer_a)):
            print "Deal Reached"
            return (True, offer_a, offersList)

        offersList.append([set(items) - set(offer_b),set(offer_b)])

        # If we didn't agree, let a respond to b's offer, recalculate utility and send 'a' the info
        utility = (a_scale * negotiator_a.utility(), b_scale * negotiator_b.utility())
        negotiator_a.receive_utility(utility[1])
        offer_a = negotiator_a.make_offer(offer_b)

        if set(offer_a) == (set(items) - set(offer_b)):
            print "Deal Reached"
            return (True, offer_a, offersList)

        offersList.append([set(offer_a),set(items) - set(offer_a)])


    # If we failed overall, then there's no ordering to return
    return (False, None, offersList)

##Main Method for Running Negotiations


if __name__ == "__main__":
    # We can't run without at least one scenario. We can, however, run with multiple provided scenarios

    if len(argv) < 2:
        print("Please provide at least one scenario file, in csv format.")
        exit(-42)
    score_a = score_b = 0
    # We will replace Negotiator here with <your id>_Negotiator, as specified in the Readme



    negotiator_a = ss2cp()
    negotiator_b = ky2cg()



    for scenario in argv[1:]:
        # Get the scenario parameters
        (num_iters, mapping) = read_scenario(scenario)
        # Separate the mapping out for each negotiator
        # based upon the preferences of each negotiator
        a_mapping = {item["item_name"] : int(item["negotiator_a"]) for item in mapping}
        a_order = sorted(a_mapping, key=a_mapping.get, reverse=True)
        b_mapping = {item["item_name"] : int(item["negotiator_b"]) for item in mapping}
        for item in a_mapping:
            print str(item) + " " + str(a_mapping[item]) + ", " + str(b_mapping[item])
        b_order = sorted(b_mapping, key=b_mapping.get, reverse=True)
        # Give each negotiator their preferred item ordering
        negotiator_a.initialize(a_mapping, num_iters)
        negotiator_b.initialize(b_mapping, num_iters)
        # Get the result of the negotiation
        (result, order, roundinfo) = negotiate(num_iters, negotiator_a, negotiator_b, sorted(a_mapping.keys()))
        # Assign points to each negotiator. Note that if the negotiation failed, each negotiatior receives a negative penalty
        # However, it is also possible in a "successful" negotiation for a given negotiator to receive negative points
        if result:
            (points_a, points_b) = (negotiator_a.utility(), negotiator_b.utility())
        else:
            (points_a, points_b) = (-len(a_order), -len(b_order))
        results = (result, points_a, points_b, len(roundinfo))
        score_a += points_a
        score_b += points_b
        # Update each negotiator with the final result, points assigned, and number of iterations taken to reach an agreement
        negotiator_a.receive_results(results)
        negotiator_b.receive_results(results)
        #Create Post-Round Graph Information
        (A_Utility,B_Utility,theRounds) = end_of_round_graph(negotiator_a,negotiator_b,roundinfo)
        #Make Post-Round Graph
        print("{} negotiation:\n\tNegotiator A: {}\n\tNegotiator B: {}".format("Successful" if result else "Failed", points_a, points_b))
        #g.make_post_round_graph(A_Utility,B_Utility,theRounds,results)

    print("Final result:\n\tNegotiator A: {}\n\tNegotiator B: {}".format(score_a, score_b))
    #Make Post-Game Graph
    #g.make_final_round_graph()

