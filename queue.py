import numpy as np

class Customer:
    def __init__(self, customer_id, arrival_mean, arrival_stddev, service_mean, service_stddev):
        self.id = customer_id
        self.inter_arrival_time = max(0, np.random.normal(arrival_mean, arrival_stddev))
        self.service_time = max(0, np.random.normal(service_mean, service_stddev))
        self.waiting_time = 0
        self.total_system_time = 0

class QueueSimulation:
    def __init__(self, num_customers, arrival_mean, arrival_stddev, service_mean, service_stddev):
        self.num_customers = num_customers
        self.arrival_mean = arrival_mean
        self.arrival_stddev = arrival_stddev
        self.service_mean = service_mean
        self.service_stddev = service_stddev
        self.simulation_time = 0
        self.customers = []
        self.waiting_times = []
        self.service_times = []

    def run_simulation(self):
        for customer_id in range(1, self.num_customers + 1):
            customer = Customer(customer_id, self.arrival_mean, self.arrival_stddev, self.service_mean, self.service_stddev)

            customer.waiting_time = max(0, self.simulation_time - customer.inter_arrival_time)

            self.simulation_time += customer.inter_arrival_time + customer.service_time
            
            self.customers.append(customer)
            
            self.waiting_times.append(customer.waiting_time)
            self.service_times.append(customer.service_time)

    def display_customer_information(self):
        for customer in self.customers:
            print(f"Customer {customer.id}:")
            print(f"Inter-arrival time: {customer.inter_arrival_time:.2f} sec")
            print(f"Waiting time: {customer.waiting_time:.2f} sec")
            print(f"Service time: {customer.service_time:.2f} sec")
            print()



if __name__ == "__main__":
    num_customers = 15
    arrival_mean = 30
    arrival_stddev = 6
    service_mean = 20
    service_stddev = 4

    simulation = QueueSimulation(num_customers, arrival_mean, arrival_stddev, service_mean, service_stddev)
    simulation.run_simulation()
    simulation.display_customer_information()
