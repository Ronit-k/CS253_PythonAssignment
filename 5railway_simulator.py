from abc import ABC, abstractmethod

# 1. Custom Exception
class PhysicsConstraintError(Exception):
    # Raised when the train's weight exceeds its pulling capacity."""
    pass

# 2. Base Class for all train parts
class RollingStock(ABC):
    def __init__(self, id_str, weight):
        self.id_str = id_str
        self.weight = weight

# 3. Locomotive Class
class Locomotive(RollingStock):
    def __init__(self, id_str, weight, pull_capacity, fuel_rate):
        super().__init__(id_str, weight)
        self.pull_capacity = pull_capacity
        self.fuel_rate = fuel_rate  # liters per ton per km

# 4. FreightCar Class
class FreightCar(RollingStock):
    def __init__(self, id_str, empty_weight, cargo_weight, destination):
        # The base weight of the car itself
        super().__init__(id_str, empty_weight)
        self.cargo_weight = cargo_weight
        self.destination = destination

    @property
    def total_weight(self):
        # Dynamically calculate weight based on car + cargo
        return self.weight + self.cargo_weight

# 5. Train Management Class
class Train:
    def __init__(self):
        self.stock_list = []

    def couple(self, stock):
        # Adds a car or locomotive to the train
        self.stock_list.append(stock)

    def uncouple(self, stock_id):
        # Removes a specific car by ID and returns it
        for i, item in enumerate(self.stock_list):
            if item.id_str == stock_id:
                return self.stock_list.pop(i)
        return None

    def get_total_weight(self):
        # Calculates total weight of everything in the train
        total_weight = 0
        for item in self.stock_list:
            # Check if it's a FreightCar (which has total_weight property) or Locomotive
            if isinstance(item, FreightCar):
                total_weight += item.total_weight
            else:
                total_weight += item.weight
        return total_weight

    def get_total_pull(self):
        # Sum of pulling capacities of all attached locomotives
        total_pull = 0
        for item in self.stock_list:
            if isinstance(item, Locomotive):
                total_pull += item.pull_capacity
        return total_pull

    def validate_physics(self):
        # Checks if the locomotives can actually pull the weight
        if self.get_total_weight() > self.get_total_pull():
            raise PhysicsConstraintError("Train is too heavy for the attached locomotives!")

    def get_average_fuel_rate(self):
        # Helper function to find the mean fuel rate of all locomotives
        locos = [item for item in self.stock_list if isinstance(item, Locomotive)]
        if not locos:
            return 0
        return sum(l.fuel_rate for l in locos) / len(locos)

# 6. Network Management
class RailwayNetwork:
    def __init__(self):
        self.graph = {} # we are using a dictionary to store stations and its neighbours with the distance between them (adjacency list)

    def add_link(self, station_A, station_B, distance):
        # We store distances in a simple nested dictionary
        if station_A not in self.graph: self.graph[station_A] = {}
        self.graph[station_A][station_B] = distance

    def get_distance(self, station_A, station_B):
        return self.graph.get(station_A, {}).get(station_B, 0)

# 7. Simulation Engine
def run_delivery_schedule(train, network, route_list):
    total_fuel_consumed = 0.0
    
    # Iterate through the stations in the route
    for i, current_station in enumerate(route_list):
        
        # --- Arrival Logic ---
        # Find and uncouple cars that belong at this station
        for item in train.stock_list:
            if isinstance(item, FreightCar) and item.destination == current_station: #check if the item is a freight car and its destination is the current station
                train.uncouple(item.id_str) # if yes then remove the car from the train
        

        # --- Departure Logic ---
        # If there is a next station, calculate travel
        if i + 1 < len(route_list):
            next_station = route_list[i + 1]
            
            # Physics Check
            train.validate_physics()
            
            # Data for fuel calculation
            weight = train.get_total_weight()
            dist = network.get_distance(current_station, next_station)
            avg_fuel = train.get_average_fuel_rate()
            
            # Weight * Distance * Average Fuel Rate
            trip_fuel = weight * dist * avg_fuel
            total_fuel_consumed += trip_fuel
            
    return total_fuel_consumed

if __name__ == "__main__":
    net = RailwayNetwork()
    net.add_link("Delhi", "Kanpur", 400)
    net.add_link("Kanpur", "Prayagraj", 200)
    
    train = Train()
    train.couple(Locomotive("L1", weight=100, pull_capacity=500, fuel_rate=0.01))
    train.couple(FreightCar("C1", empty_weight=20, cargo_weight=80, destination="Kanpur"))
    train.couple(FreightCar("C2", empty_weight=20, cargo_weight=180, destination="Prayagraj"))
    
    # Train weight = 100(L) + 100(C1) + 200(C2) = 400. Capacity = 500. Valid.
    # Delhi -> Kanpur: 400km * 400 tons * 0.01 = 1600 liters.
    # At Kanpur, C1 is uncoupled. New weight = 100(L) + 200(C2) = 300.
    # Kanpur -> Prayagraj: 200km * 300 tons * 0.01 = 600 liters.
    # Total = 1600 + 600 = 2200.0
    
    try:
        total_fuel = run_delivery_schedule(train, net, ["Delhi", "Kanpur", "Prayagraj"])
        print(f"Total fuel consumed: {total_fuel}")
        # Expecting 2200.0
    except PhysicsConstraintError as e:
        print(f"Physics Error: {e}")
