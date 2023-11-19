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
        Lq_mmc = ((arrival_rate * W) ** c) / (m.factorial(c) * (1 - rho) ** 2)
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
def calculate_probability_of_zero(c):
    probability_dict = {}
    for day, data in intensity_dict.items():
        val=0
        probability_list = []
        for d in data:
            rho = d
            val += ((rho**1)/m.factorial(1))+((rho**c)/m.factorial(c)*(1-rho))
            val = val ** -1
            probability_list.append(val)
        probability_dict[day] = probability_list
    return probability_dict


probability_of_zero_dict = calculate_probability_of_zero(4)
print(probability_of_zero_dict)
print ("\nAbove works\n")



print("Lq")
def get_mmc_Lq(c):
    # list of size 5x4 
    data_rho = []
    # list of size 5x4
    data_prob = []
    # list of size 1x5
    days_of_week = []

    lq_dict = {}

    for day_rho, data_rho_i in intensity_dict.items():
        data_rho.append(data_rho_i)
        days_of_week.append(day_rho)

    for day_prob, data_prob_i in probability_of_zero_dict.items():
        data_prob.append(data_prob_i)

    

    for i in range(len(data_rho)):
        lq_values = []
        for j in range(len(data_rho[i])):
            val = (((data_rho[i][j])**(c+1)) / (m.factorial(c-1) * (c - data_rho[i][j])**2)) * data_prob[i][j]
            lq_values.append(val)
        
        lq_dict[days_of_week[i]] = lq_values

    return lq_dict



lq_dict = get_mmc_Lq(4)
print(lq_dict)
print ("\nAbove works\n")

 
print("Ls")
def get_mmc_ls(c):
    # this list has 5 pairs of arrival/service rates for Monday-Friday 
    arrival_service = []
    # this 2d list of size 5X4 is the Monday[1, 2, 3, 4], ... , Friday[1, 2, 3, 4]
    data_list = []

    for day_c, data_c in lq_dict.items():
        rate = day_data_services[day_c]["arrival_rate"]/(day_data_services[day_c]["service_rate"]*c)
        arrival_service.append(rate)

    for day, data in lq_dict.items():
        data_list.append(data)
    
    result = [
    [arrival_service[i] * element for element in row]
    for i, row in enumerate(data_list)]

    return result

Ls = get_mmc_ls(4)
print(Ls)
print("\n\n")

print ("\nAbove works\n")



print("Wq")
def get_mmc_wq(c):
    data_rho = []
    data_prob = []
    days_of_week = []

    for day_rho, data_rho_i in intensity_dict.items():
        data_rho.append(data_rho_i)
        days_of_week.append(day_rho)
    
    for day, data in day_data_services.items():
        arrival = data["arrival_rate"]

    for i in range(c):
        val = ((data_rho[i]**(i + 1)*(1-data_rho[i])) / (i) * (i - data_rho[i]2)) * (1/arrival)
        key = (days_of_week[j], i + 1)
        lq_dict[key] = val


    return lq_dict

print("\n\n")

print("Ws")
def get_mmc_ws(c):
    data_rho = []
    data_prob = []
    days_of_week = []

    for day_rho, data_rho_i in intensity_dict.items():
        data_rho.append(data_rho_i)
        days_of_week.append(day_rho)
    
    for day, data in day_data_services.items():
        arrival = data["arrival_rate"]

    for i in range(c):
        val = ((data_rho[i]**(i + 1)*(1-data_rho[i])) / (i) * (i - data_rho[i]2)) * (1/arrival)
        key = (days_of_week[j], i + 1)
        lq_dict[key] = val


    return lq_dict

