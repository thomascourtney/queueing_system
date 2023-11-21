import math as m
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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



calculate_and_display_metrics(day_data_combined, day_data_services, number_of_queue)


#print("TRAFFIC INTENSITY = ρ")
def get_mmc_traffic_intensity(c):
    intensity_dict = {}

    for day, data in day_data_services.items():
        arrival = data["arrival_rate"]
        service = data["service_rate"]
        
        data_list = [arrival / (i * service) for i in range(1, c + 1)]
        
        intensity_dict[day] = data_list

    return intensity_dict

intensity_dict = get_mmc_traffic_intensity(number_of_queue)

    

#print("PROBABILITY OF ZERO = π")
def calculate_probability_of_zero(c, rho_dict):
    probabilities_dict = {}

    for key, rho_values in rho_dict.items():
        probabilities = []

        for rho in rho_values:
            probability_of_zero = 1

            for i in range(c):
                probability_of_zero += (((rho*c)**i / (m.factorial(i)) + ((c*rho)**c)/(m.factorial(c)*(1-rho))))

            probability_of_zero = 1 / (probability_of_zero)
            probabilities.append(probability_of_zero)

        probabilities_dict[key] = probabilities
    
    return probabilities_dict


probability_of_zero_dict = calculate_probability_of_zero(number_of_queue, intensity_dict)


server_utilization = {day: [1 - val for val in values] for day, values in probability_of_zero_dict.items()}



#print("Lq")
def get_mmc_Lq(c):
    lq_dict = {}

    for day, data_rho in intensity_dict.items():
        lq_values = []
        for rho, prob in zip(data_rho, probability_of_zero_dict[day]):
            val = 0
            for i in range(1, c+1):
                val += (((rho) ** (i + 1))*(1-rho) / (m.factorial(i - 1) * (1 - rho) ** 2)) * prob
            lq_values.append(val)

        lq_dict[day] = lq_values

    return lq_dict



lq_dict = get_mmc_Lq(number_of_queue)



 
#print("Ls")
def get_mmc_ls(c):
    ls_dict = {}

    for day, data in intensity_dict.items():
        ls_list = []
        
        for rho in data:
            val = 0
            for i in range(1, c+1):
                val += ( (rho * (1 + (((i*rho)**i)/m.factorial(i)*(1-rho))) / (1-rho)**2) )
            
            ls_list.append(val)
        
        ls_dict[day] = ls_list


    return ls_dict



Ls = get_mmc_ls(number_of_queue)



#print("Wq")
def get_mmc_wq(c):
    wq_dict = {}
    arrival_list = []
    
    for day, data in day_data_services.items():
        arrival_data = data["arrival_rate"]
        arrival_list.append(arrival_data)

    for day_rho, data_rho in intensity_dict.items():
        wq_list = []
        for rho, arrival in zip(data_rho, arrival_list):
            val = 0 
            for i in range(1, c+1):
                val += ((rho ** (i + 1) * (1 - rho)) / ((i) * (i - rho))) * (1 / arrival)
            wq_list.append(val)
        
        wq_dict[day_rho] = wq_list

    return wq_dict


wq = get_mmc_wq(number_of_queue)


#print("Ws")
def get_mmc_ws(c):
    ws_dict = {}
    arrival_list = []
    
    for day, data in day_data_services.items():
        arrival_data = data["arrival_rate"]
        arrival_list.append(arrival_data)

    for day_rho, data_rho in intensity_dict.items():
        wq_list = []
        for rho, arrival in zip(data_rho, arrival_list):
            val = 0
            for i in range(1, c+1):
                val += (((rho**(i+1)) + 1-rho) / ((m.factorial(i-1))*((1-rho)**2)*(arrival))) * 1/arrival
            wq_list.append(val)
        ws_dict[day_rho] = wq_list
 
    return ws_dict

ws = get_mmc_ws(number_of_queue)




def generate_list_recursive(n, current_value=1, current_count=0, result=[]):
    if current_count == n:
        return result
    
    result.append(current_value)

    return generate_list_recursive(n, current_value, current_count + 1, result) if current_count % 5 != 4 else generate_list_recursive(n, current_value + 1, current_count + 1, result)

my_list = generate_list_recursive(20)


def create_table(c):
    table_dict = {}

    days_of_week = list(wq.keys()) * 4

    wq_list = [d for data_wq in wq.values() for d in data_wq]
    ws_list = [d_ws for data_ws in ws.values() for d_ws in data_ws]
    server_list = [d_server for data_server in server_utilization.values() for d_server in data_server]

    table_dict["Number of doctors (servers)"] = my_list
    table_dict["Server Utilization"] = server_list
    table_dict["Mean waiting time in system"] = ws_list
    table_dict["Mean waiting time in queues"] = wq_list
    table_dict["Day"] = days_of_week

    return table_dict

    
print("\n\n")
table = create_table(number_of_queue)


df = pd.DataFrame(table)
df.set_index("Number of doctors (servers)", inplace=True)
print(df)

def create_hist(data, y_axis, title):
    plt.figure(figsize=(7, 5))

    days = df['Day'].unique()
    num_servers = df.index.unique()

    bar_width = 0.1

    for i, count in enumerate(num_servers):
        server_data = df[df.index == count]
        positions = np.arange(len(days)) + bar_width * i
        plt.bar(positions, server_data[data], width=bar_width, label=f'# of servers = {count}')

    plt.xlabel('Day of the Week')
    plt.ylabel(y_axis)
    plt.title(title)
    plt.xticks(np.arange(len(days)) + bar_width * (len(num_servers) - 1) / 2, days)
    plt.legend(fontsize="small")

    plt.show()


create_hist("Server Utilization", 'Server Utilization', 'Server Utilization for Different Number of Servers')
create_hist("Mean waiting time in system", "Ws", 'Server Utilization for Different Number of Servers')
create_hist("Mean waiting time in queues", "Wq", 'Server Utilization for Different Number of Servers')