import math as m

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

number_of_queue = 4


def calculate_and_display_metrics(day_data_combined, day_data_services, c):
    print("\nDay\t\t\tWs (h)\t\tWq (h)")
    print("-" * 47)

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
        print(f"{day.ljust(14)}\t\t{data['Ws']:.4f}\t\t{data['Wq']:.4f}")


print("\n\n")
calculate_and_display_metrics(day_data_combined, day_data_services, number_of_queue)

print("\n\n")

print("TRAFFIC INTENSITY = ρ")
def get_mmc_traffic_intensity(c):
    intensity_dict = {}
    for day, data in day_data_services.items():
        arrival = data["arrival_rate"]
        service = data["service_rate"]
        data_list = []
        for i in range(1, c + 1):
            val = arrival / (i * service)
            data_list.append(val)
        intensity_dict[day] = data_list
    
    return intensity_dict

intensity_dict = get_mmc_traffic_intensity(number_of_queue)
print(intensity_dict)
print("\n\n")

print("PROBABILITY OF ZERO = π")
def calculate_probability_of_zero(c, rho_dict):
    probabilities_dict = {}

    for key, rho_values in rho_dict.items():
        probabilities = []

        for rho in rho_values:
            probability_of_zero = 0

            for i in range(c):
                probability_of_zero += (m.pow(rho, i) / (m.factorial(i) * (1 - rho)))

            probability_of_zero = 1 / (1 + probability_of_zero)
            probabilities.append(probability_of_zero)

        probabilities_dict[key] = probabilities
    
    return probabilities_dict


probability_of_zero_dict = calculate_probability_of_zero(number_of_queue, intensity_dict)
print(probability_of_zero_dict)
print("\n\n")


print("Lq")
def get_mmc_Lq(c):
    lq_dict = {}

    for day, data_rho in intensity_dict.items():
        lq_values = []
        for rho, prob in zip(data_rho, probability_of_zero_dict[day]):
            for i in range(1, c+1):
                val = (((rho) ** (i + 1))*(1-rho) / (m.factorial(i - 1) * (1 - rho) ** 2)) * prob
            lq_values.append(val)

        lq_dict[day] = lq_values

    return lq_dict



lq_dict = get_mmc_Lq(number_of_queue)
print(lq_dict)
print("\n\n")

 
print("Ls")
def get_mmc_ls(c):
    ls_dict = {}

    for day, data in intensity_dict.items():
        ls_list = []
        
        for rho in data:

            for i in range(1, c+1):
                val = ( (rho * (1 + (((i*rho)**i)/m.factorial(i)*(1-rho))) / (1-rho)**2) )
            
            ls_list.append(val)
        
        ls_dict[day] = ls_list


    return ls_dict



Ls = get_mmc_ls(number_of_queue)
print(Ls)
print("\n\n")


print("Wq")
def get_mmc_wq(c):
    wq_dict = {}
    arrival_list = []
    
    for day, data in day_data_services.items():
        arrival_data = data["arrival_rate"]
        arrival_list.append(arrival_data)

    for day_rho, data_rho in intensity_dict.items():
        wq_list = []
        for rho, arrival in zip(data_rho, arrival_list):

            for i in range(1, c+1):
                val = ((rho ** (i + 1) * (1 - rho)) / ((i) * (i - rho))) * (1 / arrival)
            wq_list.append(val)
        
        wq_dict[day_rho] = wq_list

    return wq_dict


wq = get_mmc_wq(number_of_queue)
print(wq)
print("\n\n")

print("Ws")
def get_mmc_ws(c):
    ws_dict = {}
    arrival_list = []
    
    for day, data in day_data_services.items():
        arrival_data = data["arrival_rate"]
        arrival_list.append(arrival_data)

    for day_rho, data_rho in intensity_dict.items():
        wq_list = []
        for rho, arrival in zip(data_rho, arrival_list):
            
            for i in range(1, c+1):
                val = (((rho**(i+1)) + 1-rho) / ((m.factorial(i-1))*((1-rho)**2)*(arrival))) * 1/arrival
            wq_list.append(val)
        ws_dict[day_rho] = wq_list
 
    return ws_dict

ws = get_mmc_ws(4)
print(ws)