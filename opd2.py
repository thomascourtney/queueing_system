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



def calculate_and_display_metrics(day_data_combined, day_data_services, c):
    print("\nDay\t\t\tWs (h)\t\tWq (h)\t\tLq_mmc\t\tLs_mmc")
    print("-" * 85)

    for day, data in day_data_combined.items():
        arrival_rate = day_data_services[day]["arrival_rate"]
        service_rate = day_data_services[day]["service_rate"]
        Ls = day_data_combined[day]["Ls"]
        Lq = day_data_combined[day]["Lq"]
        data["Lq_calc"] = Lq
        data["Ls_calc"] = Ls
        data["Ws"] = Ls / arrival_rate
        data["Wq"] = Lq / arrival_rate
        rho = arrival_rate / (c * service_rate)
        W = Ls / arrival_rate
        Lq_mmc = ((arrival_rate * W) ** c) / (math.factorial(c) * (1 - rho) ** 2)
        Ls_mmc = Lq + (arrival_rate / service_rate)
        data["Lq_mmc"] = Lq_mmc
        data["Ls_mmc"] = Ls_mmc
        print(f"{day.ljust(14)}\t\t{data['Ws']:.4f}\t\t{data['Wq']:.4f}\t\t{data['Lq_mmc']:.4f}\t\t{data['Ls_mmc']:.4f}")

print("\n")
calculate_and_display_metrics(day_data_combined, day_data_services, 4)

print ("Above works\n")

print("TRAFFIC INTENSITY = ρ")
def get_mmc_traffic_intensity(c):
    intensity_dict = {}
    for day, data in day_data_services.items():
        arrival = data["arrival_rate"]
        service = data["service_rate"]
        data_list = []
        for i in range(1, c+1):
            val = arrival / (i * service)
            data_list.append(val)
        intensity_dict[day] = data_list
    
    return intensity_dict

intensity_dict = get_mmc_traffic_intensity(4)
print(intensity_dict)
print ("\nAbove works\n")


print("PROBABILITY OF ZERO = π")
def calculate_probability_of_zero(num_servers):
    probability_dict = {}
    for day, data in intensity_dict.items():
        probability_of_zero = []
        for i in range(0, num_servers):
            term = (data[i]**i) / math.factorial(i)
            probability_of_zero.append(math.exp(-data[i]) * sum(term for i in range(num_servers - i + 1)))
        probability_dict[day] = probability_of_zero
    return probability_dict


probability_of_zero_dict = calculate_probability_of_zero(4)
print(probability_of_zero_dict)
print ("\nAbove works\n")




def get_mmc_Lq(c):
    data_rho = []
    data_prob = []
    days_of_week = []
    for day_rho, data_rho_i in intensity_dict.items():
        data_rho.append(data_rho_i)
        days_of_week.append(day_rho)
    for day_prob, data_prob_i in probability_of_zero_dict.items():
        data_prob.append(data_prob_i)
    
    lq_dict = {}
            
    for i in range(c):
        for j in range(5):
            val = (data_rho[j][i]**(i + 1) / (math.factorial(i) * (i - data_rho[j][i])**2)) * data_prob[j][i]
            key = (days_of_week[j], i + 1)
            lq_dict[key] = val

    print(lq_dict)


lq_dict = get_mmc_Lq(4)


'''
print("\n")
print(f"Day\t\t\tLs_calc")
print("-" * 50)
for day, data in day_data_combined.items():
    print(f"{day.ljust(10)}\t\t{data['Ls_calc']:.4f}")

print("\n")
print(f"Day\t\t\tLq_mmc")
print("-" * 50)
for day, data in day_data_combined.items():
    print(f"{day.ljust(10)}\t\t{Lq_mmc:.4f}"

print("\n")
print(f"Day\t\t\tLs_mmc")
print("-" * 50)
for day, data in day_data_combined.items():
    print(f"{day.ljust(10)}\t\t{Ls_mmc:.4f}")

print("\n")
print("Day\t\tWs")
print("-" * 20)
for day, data in day_data_combined.items():
    service_rate = day_data_services[day]["service_rate"]
    Wq = data["Wq"]
    Ws = Wq + (1 / service_rate)
    print(f"{day.ljust(10)}\t\t{Ws:.4f}")


def calculate_utilization(arrival_rate, service_rate, num_servers):
    return (arrival_rate / (service_rate * num_servers)) * 100

def calculate_waiting_time_in_system(Ls, arrival_rate):
    return Ls / arrival_rate

def calculate_waiting_time_in_queue(Lq, arrival_rate):
    return Lq / arrival_rate

def calculate_values_for_servers(day, num_servers):
    arrival_rate = day_data_services[day]["arrival_rate"]
    service_rate = day_data_services[day]["service_rate"]
    Ls = day_data_combined[day]["Ls"]
    Lq = day_data_combined[day]["Lq"]

    utilization = calculate_utilization(arrival_rate, service_rate, num_servers)
    Ws = calculate_waiting_time_in_system(Ls, arrival_rate)
    Wq = calculate_waiting_time_in_queue(Lq, arrival_rate)

    return utilization, Ws, Wq
print("\n")
# Display the table header
print("Number of Servers\tUtilization (%)\tMean Time in System\tMean Time in Queue\tDay")
print("-" * 90)

# Calculate and display values for different numbers of servers
for day in day_data_combined.keys():
    for num_servers in range(1, 5):
        utilization, Ws, Wq = calculate_values_for_servers(day, num_servers)
        print(f"{num_servers}\t\t\t{utilization:.3f}\t\t\t{Ws:.3f}\t\t\t{Wq:.3f}\t\t\t{day}")



def calculate_values_for_dispensers(day, num_dispensers):
    arrival_rate = day_data_services[day]["arrival_rate"]
    service_rate = day_data_services[day]["service_rate"]
    Ls = day_data_combined[day]["Ls"]
    Lq = day_data_combined[day]["Lq"]

    utilization = calculate_utilization(arrival_rate, service_rate, num_dispensers)
    Ws = calculate_waiting_time_in_system(Ls, arrival_rate)
    Wq = calculate_waiting_time_in_queue(Lq, arrival_rate)

    return utilization, Ws, Wq

# Display the table header
print("Number of Dispensers\tUtilization (%)\tMean Time in System\tMean Time in Queue\tDay")
print("-" * 90)

# Calculate and display values for different numbers of dispensers
for day in day_data_combined.keys():
    for num_dispensers in range(1, 5):
        utilization, Ws, Wq = calculate_values_for_dispensers(day, num_dispensers)
        print(f"{num_dispensers}\t\t\t{utilization:.3f}\t\t\t{Ws:.3f}\t\t\t{Wq:.3f}\t\t\t{day}")

'''

