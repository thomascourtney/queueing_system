import math

day_data_services = {
    "Monday": {
        "interarrival_time": 4.90,
        "arrival_rate": 12.22,
        "num_customers": 75,
        "service_rate": 93.52,
    },
    "Tuesday": {
        "interarrival_time": 5.24,
        "arrival_rate": 11.45,
        "num_customers": 67,
        "service_rate": 90.29,
    },
    "Wednesday": {
        "interarrival_time": 5.19,
        "arrival_rate": 11.4,
        "num_customers": 71,
        "service_rate": 622.09,
    },
    "Thursday": {
        "interarrival_time": 4.67,
        "arrival_rate": 12.86,
        "num_customers": 87,
        "service_rate": 80.21,
    },
    "Friday": {
        "interarrival_time": 4.58,
        "arrival_rate": 13.10,
        "num_customers": 76,
        "service_rate": 86.52,
    },
}

day_data_combined = {
    "Monday": {
        "Ls": 5.6546,
        "Lq": 3.9915
    },
    "Tuesday": {
        "Ls": 5.7159,
        "Lq": 4.0578
    },
    "Wednesday": {
        "Ls": 5.7350,
        "Lq": 4.0737
    },
    "Thursday": {
        "Ls": 7.4852,
        "Lq": 5.6601
    },
    "Friday": {
        "Ls": 9.0040,
        "Lq": 7.1419
    },
}



for day, data in day_data_combined.items():
    arrival_rate = day_data_services[day]["arrival_rate"]
    service_rate = day_data_services[day]["service_rate"]
    Ls = day_data_combined[day]["Ls"]
    Lq = day_data_combined[day]["Lq"]
    data["Lq_calc"] = Lq
    data["Ls_calc"] = Ls
    data["Ws"] = Ls / arrival_rate
    data["Wq"] = Lq / arrival_rate

print("\n")
# Display the results nicely
print("Day\t\t\tWs (h)\t\tWq (h)")
print("-" * 50)
for day, data in day_data_combined.items():
    print(f"{day.ljust(10)}\t\t{data['Ws']:.4f}\t\t{data['Wq']:.4f}")

print("\n")
print(f"Day\t\t\tLs_calc")
print("-" * 50)
for day, data in day_data_combined.items():
    print(f"{day.ljust(10)}\t\t{data['Ls_calc']:.4f}")


print("\n")
for c_val in range(1, 5):
    print(f"\nLq calc Results for c = {c_val}:")
    print("-" * 50)
    for day, data in day_data_combined.items():
        arrival_rate = day_data_services[day]["arrival_rate"]
        service_rate = day_data_services[day]["service_rate"]
        rho = arrival_rate / (service_rate * c_val)
        Lq = rho / (1 - rho)
        data[f"Lq_calc_c{c_val}"] = Lq
        print(f"{day.ljust(15)}\t\t{data[f'Lq_calc_c{c_val}']:.4f}")

