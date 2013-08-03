#!/usr/bin/env python

def carbon(distance, mpg, method):
    """ This will return a value that is g/km """
    """ CONVERT THE RETURN VALUE BASED ON USER PREFERENCES """
    PETROL_CONST = 6760;
    DIESEL_CONST = 7440;

    if method == "Driving":
        CO2 = (PETROL_CONST / mpg) * distance;
        return CO2;

    elif method == "Transit":
        """ This assumes the average 40-feet CTA bus """
        """ CTA is testing a new model, with 4.43 MPG, but I haven't seen any of those yet """
        """ It is said that the average CTA bus replaces over 70 cars in terms of CO2 emissions """
        """ I use a generous estimate of 70, to make sure the app will never overestimate the user's emissions """
        """ This is all handwavy math, a more advanced application would try to account for passenger density """
        CTA_BUS_MPG = 3.28;
        CO2 = ((DIESEL_CONST / CTA_BUS_MPG) * distance) / 70;
        return CO2;
    
    elif method == "Biking":
        return 0;

    else:
        return 0;
    pass
    

def cost(distance, fare, mpg, method, transfer):
    milesDistance = distance;
    if method == "Driving":
        """ indirectCost includes things like fixed costs, fuel, parking, pollution damage, accident cost, tickets, etc """
        indirectCostPerMile = 0.172;
        averageGasPrice = 4.043; """ Need a more reliable way of getting this. """
        directCost = (milesDistance / mpg) * averageGasPrice;
        cost = directCost + milesDistance * indirectCostPerMile;
        return cost;
    
    elif method == "Transit":
        return fare + (transfer * fare);

    elif method == "Biking":
        """ Disregards the cost of a bike """
        return 0;

    else:
        return 0;
    pass
