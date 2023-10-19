import numpy as np
import random

# Define parameters
num_customers = 15
arrival_mean = 30  # Mean inter-arrival time (seconds)
arrival_stddev = 6  # Standard deviation of inter-arrival time (seconds)
service_mean = 20  # Mean service time (seconds)
service_stddev = 4  # Standard deviation of service time (seconds)

# Initialize simulation variables
simulation_time = 0
customers = []
waiting_times = []
service_times = []

for customer_id in range(1, num_customers + 1):
    # Generate inter-arrival time and service time
    inter_arrival_time = max(0, np.random.normal(arrival_mean, arrival_stddev))
    service_time = max(0, np.random.normal(service_mean, service_stddev))

    # Calculate waiting time (time spent in the queue)
    waiting_time = max(0, simulation_time - inter_arrival_time)

    # Calculate total system time
    total_system_time = inter_arrival_time + waiting_time + service_time

    # Update simulation time
    simulation_time += inter_arrival_time + service_time

    # Append customer information
    customers.append({
        "id": customer_id,
        "inter_arrival_time": inter_arrival_time,
        "waiting_time": waiting_time,
        "service_time": service_time,
        "total_system_time": total_system_time
    })

    # Record waiting and service times for averaging
    waiting_times.append(waiting_time)
    service_times.append(service_time)

# Display customer information
for customer in customers:
    print(f"Customer {customer['id']}:")
    print(f"Inter-arrival time: {customer['inter_arrival_time']:.2f} sec")
    print(f"Waiting time: {customer['waiting_time']:.2f} sec")
    print(f"Service time: {customer['service_time']:.2f} sec")
    print(f"Total system time: {customer['total_system_time']:.2f} sec")
    print()

# Calculate and display average waiting time and average service time for all customers
avg_waiting_time = sum(waiting_times) / num_customers
avg_service_time = sum(service_times) / num_customers

print(f"Average Waiting Time for All Customers: {avg_waiting_time:.2f} sec")
print(f"Average Service Time for All Customers: {avg_service_time:.2f} sec")
