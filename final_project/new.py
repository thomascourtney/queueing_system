import random
import matplotlib.pyplot as plt
import tabulate
import numpy as np

class Client:
    def __init__(self, id, arrival_time, service_time):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time

    def __str__(self):
        return f"Client {self.id}"



class ServicePoint:
    def __init__(self, id):
        self.id = id
        self.busy = False
        self.current_client = None
        self.service_start_time = 0
        self.total_service_time = 0

    def serve_client(self, client, current_time):
        self.busy = True
        self.current_client = client
        self.service_start_time = current_time

    def finish_serving(self, current_time):
        self.busy = False
        self.total_service_time += current_time - self.service_start_time
        finished_client = self.current_client
        self.current_client = None
        return finished_client



class WaitingQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, client):
        self.queue.append(client)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            return None

    def is_empty(self):
        return len(self.queue) == 0



class mmcSystem:
    def __init__(self, daily_data, num_service_points):
        self.daily_data = daily_data
        self.num_service_points = num_service_points
        self.current_time = 0
        self.queues = [WaitingQueue() for _ in range(len(daily_data))]
        self.service_points = [ServicePoint(i) for i in range(num_service_points)]
        self.total_waiting_time = [0] * len(daily_data)
        self.total_service_time = [0] * len(daily_data)
        self.num_clients_served = [0] * len(daily_data)

    def generate_interarrival_time(self, day_index):
        return random.expovariate((1/self.daily_data[day_index]["arrival_rate"])*10)

    def generate_service_time(self, day):
        return random.expovariate(1 / self.daily_data[day]["service_rate"])

    def enqueue(self, client, day_index):
        client.arrival_time = self.current_time
        self.queues[day_index].enqueue(client)

    def serve_clients(self):
        for service_point in self.service_points:
            if not service_point.busy:
                for day_index in range(len(self.daily_data)):
                    if not self.queues[day_index].is_empty():
                        client = self.queues[day_index].dequeue()
                        service_point.serve_client(client, self.current_time)

    def finish_service(self):
        finished_clients = []
        for service_point in self.service_points:
            if service_point.busy:
                finished_client = service_point.finish_serving(self.current_time)
                finished_clients.append((finished_client, service_point.id % len(self.daily_data)))
        return finished_clients

    def output_results_table(self, mean_waiting_time, mean_service_time, server_utilization):
        headers = ["Day", "Mean Waiting Time", "Mean Service Time", "Server Utilization"]
        data = []

        for day, day_info in self.daily_data.items():
            day_index = list(self.daily_data.keys()).index(day)
            row = [day, mean_waiting_time[day_index], mean_service_time[day_index], server_utilization[day_index]]
            data.append(row)

        print(tabulate.tabulate(data, headers=headers, tablefmt="grid"))


    def simulate(self, num_iterations):
        total_simulation_time = 0 

        for _ in range(num_iterations):
            for day_index, (day, day_info) in enumerate(self.daily_data.items()):
                interarrival_time = self.generate_interarrival_time(day)
                total_simulation_time += interarrival_time 
                self.current_time += interarrival_time

                for _ in range(day_info["num_clients"]):
                    client = Client(id=None, arrival_time=None, service_time=self.generate_service_time(day))
                    self.enqueue(client, day_index)

                self.serve_clients()

                finished_clients = self.finish_service()

                for client, service_point_id in finished_clients:
                    self.total_waiting_time[day_index] += self.current_time - client.arrival_time
                    self.total_service_time[day_index] += client.service_time
                    self.num_clients_served[day_index] += 1


        mean_waiting_time = [total_waiting_time / sum(self.num_clients_served) if num_clients_served > 0 else 0
                     for total_waiting_time, num_clients_served in zip(self.total_waiting_time, self.num_clients_served)]
        mean_service_time = [total_service_time / sum(self.num_clients_served) if num_clients_served > 0 else 0
                     for total_service_time, num_clients_served in zip(self.total_service_time, self.num_clients_served)]



        server_utilization = [total_service_time / total_simulation_time if total_simulation_time > 0 else 0
                              for total_service_time in self.total_service_time]

        self.output_results_table(mean_waiting_time, mean_service_time, server_utilization)

        return mean_waiting_time, mean_service_time


if __name__ == "__main__":
    daily_data_services = {
        "Monday": {
            "interarrival_time": 4.90,
            "arrival_rate": 12.22,
            "num_clients": 75,
            "service_rate": 93.52,
        },
        "Tuesday": {
            "interarrival_time": 5.24,
            "arrival_rate": 11.45,
            "num_clients": 67,
            "service_rate": 90.29,
        },
        "Wednesday": {
            "interarrival_time": 5.19,
            "arrival_rate": 11.4,
            "num_clients": 71,
            "service_rate": 622.09,
        },
        "Thursday": {
            "interarrival_time": 4.67,
            "arrival_rate": 12.86,
            "num_clients": 87,
            "service_rate": 80.21,
        },
        "Friday": {
            "interarrival_time": 4.58,
            "arrival_rate": 13.10,
            "num_clients": 76,
            "service_rate": 86.52,
        },
    }

    num_iterations = 120
    num_servers = 5

    mean_waiting_time_by_servers = []
    mean_service_time_by_servers = []

    for num_service_points in range(1, num_servers+1):
        mmc_system = mmcSystem(daily_data_services, num_service_points)
        mean_waiting_time, mean_service_time = mmc_system.simulate(num_iterations)

        mean_waiting_time_by_servers.append(mean_waiting_time)
        mean_service_time_by_servers.append(mean_service_time)

    def get_graph(data, mean, label:str):
        for i in range(len(data[0])):
            plt.plot(range(1, num_servers+1), [mean[i] for mean in data], label=f"Server {i+1} - {label}")
        plt.xlabel("Number of Servers")
        plt.ylabel("Time (units)")
        plt.title("Simulation Results by Number of Servers")
        plt.legend()
        plt.show()


    get_graph(mean_waiting_time_by_servers, mean_waiting_time, "Waiting Time")

    get_graph(mean_waiting_time_by_servers, mean_service_time, "Service Time")

    def get_bar_chart(data, labels, title):
        plt.figure(figsize=(10, 6))

        num_servers = range(1, len(data[0]) + 1)
        bar_width = 0.09

        for i, mean in enumerate(data):
            x_values = np.arange(len(labels)) + bar_width * i
            plt.bar(x_values, mean, width=bar_width, label=f"Server {i + 1}", alpha=0.7)

        plt.xlabel("Day of the Week")
        plt.ylabel("Time (units)")
        plt.title(title)
        plt.xticks(np.arange(len(labels)) + bar_width * (len(data) - 1) / 2, labels)
        plt.legend()

        plt.show()



    get_bar_chart(mean_waiting_time_by_servers, list(daily_data_services.keys()), "Waiting Time")
    get_bar_chart(mean_service_time_by_servers, list(daily_data_services.keys()), "Service Time")



            
        
        

    

        