import random
import statistics

class Customer:
    def __init__(self, customer_id, arrival_time, service_time):
        self.customer_id = customer_id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.waiting_time = 0
        self.system_time = 0

class QueueingSystem:
    def __init__(self):
        self.customers = []
        self.current_time = 0

    def generate_inter_arrival_time(self):
        return max(0, random.normalvariate(30, 6))

    def generate_service_time(self):
        return max(0, random.normalvariate(20, 4))

    def simulate(self, num_customers):
        for customer_id in range(1, num_customers + 1):
            inter_arrival_time = self.generate_inter_arrival_time()
            self.current_time += inter_arrival_time
            arrival_time = self.current_time

            service_time = self.generate_service_time()

            waiting_time = max(0, self.current_time - arrival_time)
            system_time = waiting_time + service_time

            customer = Customer(customer_id, arrival_time, service_time)
            customer.waiting_time = waiting_time
            customer.system_time = system_time
            self.customers.append(customer)

            self.current_time += service_time

    def display_results(self):
        for customer in self.customers:
            print(f"Waiting time for customer {customer.customer_id}: {customer.waiting_time:.2f} sec")
            print(f"Total system time for customer {customer.customer_id}: {customer.system_time:.2f} sec")

        average_waiting_time = statistics.mean(customer.waiting_time for customer in self.customers)
        average_system_time = statistics.mean(customer.system_time for customer in self.customers)

        print(f"Average waiting time: {average_waiting_time:.2f} sec")
        print(f"Average total system time: {average_system_time:.2f} sec")

if __name__ == "__main__":
    queueing_system = QueueingSystem()
    queueing_system.simulate(15)
    queueing_system.display_results()
