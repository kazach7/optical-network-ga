"""
Classes providing abstraction for the elements in the network.
"""
    
# Demand, with a value and links which can be used to realize it.
class Demand:
    def __init__(self, value, links):
        self.value = value
        self.links = links 
    
# Path from one city to another, consisting of multiple connections.
class Link:
    def __init__(self, connections):
        self.connections = connections # Ordered list of connections.

# Direct connection between two cities.
class Connection:
    def __init__(self, a, b):
        self.cities = (a,b)
        self.lambdas = [] # Lambdas being in use on the connection.
    
    def add_lambda(self, lambdaNo):
        self.lambdas.append(lambdaNo)

    def check_if_lambda_occupied(self, lambdaNo):
        return (lambdaNo in self.lambdas)
    
    def clear_lambdas(self):
        self.lambdas.clear()