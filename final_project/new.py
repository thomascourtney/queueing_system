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

class MMcSystem:
    def __init__(self, daily_data, num_service_points):
        self.daily_data = daily_data
        self.num_service_points = num_service_points
        self.current_time = 0
        self.queues = [WaitingQueue() for _ in range(len(daily_data))]
        self.service_points = [ServicePoint(i) for i in range(num_service_points)]
        self.total_waiting_time = [0] * len(daily_data)
        self.total_service_time = [0] * len(daily_data)
        self.num_clients_served = [0] * len(daily_data)
        self.total_simulation_time = []

    def generate_interarrival_time(self, day_index):
        return random.expovariate(1/(self.daily_data[day_index]["arrival_rate"]))

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


    def calculate_server_utilization(self):
        total_busy_time = sum(self.total_service_time)
        total_simulation_time = sum(self.total_simulation_time)
        num_servers = self.num_service_points

        if total_simulation_time > 0:
            for i in range(1, num_servers+1):
                utilization_percentage = (total_busy_time / total_simulation_time) / i 
                utilization_percentage -= 1
            return utilization_percentage
        else:
            return 0


    def output_results_table(self, mean_waiting_time, mean_service_time, server_utilization):
        headers = ["Day", "Mean Waiting Time", "Mean Service Time", "Server Utilization", "Number of Servers"]
        data = []

        for day, day_info in self.daily_data.items():
            day_index = list(self.daily_data.keys()).index(day)
            row = [day, mean_waiting_time[day_index], mean_service_time[day_index], server_utilization[day_index], self.num_service_points]
            data.append(row)

        utilization_percentage = self.calculate_server_utilization()

        print(tabulate.tabulate(data, headers=headers, tablefmt="grid"))
        print(utilization_percentage)

    def simulate(self, num_iterations):
        total_simulation_time = 0 

        for _ in range(num_iterations):
            total_simulation_time = 0
            for day_index, (day, day_info) in enumerate(self.daily_data.items()):
                interarrival_time = self.generate_interarrival_time(day)
                total_simulation_time += interarrival_time 
                self.current_time += interarrival_time

                for _ in range(day_info["num_clients"]):
                    client = Client(id=None, arrival_time=None, service_time=self.generate_service_time(day))
                    self.enqueue(client, day_index)

                self.serve_clients()
                self.total_simulation_time.append(total_simulation_time)


                finished_clients = self.finish_service()

                for client, service_point_id in finished_clients:
                    self.total_waiting_time[day_index] += self.current_time - client.arrival_time
                    self.total_service_time[day_index] += client.service_time
                    self.num_clients_served[day_index] += 1

            # Append the total simulation time for this iteration
            self.total_simulation_time.append(total_simulation_time)

        mean_waiting_time = [total_waiting_time / sum(self.num_clients_served) if num_clients_served > 0 else 0
                     for total_waiting_time, num_clients_served in zip(self.total_waiting_time, self.num_clients_served)]
        mean_service_time = [total_service_time / sum(self.num_clients_served) if num_clients_served > 0 else 0
                     for total_service_time, num_clients_served in zip(self.total_service_time, self.num_clients_served)]

        server_utilization = [.01*total_service_time / total_simulation_time if total_service_time > 0 else 0 for total_service_time, total_simulation_time in zip(self.total_service_time, self.total_simulation_time)]

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
    num_servers = 6

    mean_waiting_time_by_servers = []
    mean_service_time_by_servers = []
    util = []

    for num_service_points in range(1, num_servers+1):
        mmc_system = MMcSystem(daily_data_services, num_service_points)

        mean_waiting_time, mean_service_time = mmc_system.simulate(num_iterations)
        utilization_percentage = mmc_system.calculate_server_utilization()
        util.append(utilization_percentage)
        mean_waiting_time_by_servers.append(mean_waiting_time)
        mean_service_time_by_servers.append(mean_service_time)


    def get_line_chart(data, title, days_of_week, max_servers):
        plt.figure(figsize=(10, 6))

        num_servers = len(data[0])
        line_styles = ["-", "--", "-.", ":", "-"] 
        for i in range(len(days_of_week)):
            plt.plot(range(1, max_servers + 1), [data[j][i] for j in range(max_servers)], label=f"{days_of_week[i]}",
                    linestyle=line_styles[i % len(line_styles)])

        plt.xlabel("Number of Servers")
        plt.ylabel("Time (units)")
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    #get_line_chart(mean_waiting_time_by_servers, "Mean Waiting Time", days_of_week, num_servers)
    #get_line_chart(mean_service_time_by_servers, "Mean Service Time", days_of_week, num_servers)



    def plot_server_utilization(data, title):
       
        plt.figure(figsize=(10, 6))

        plt.plot(data, label='Server Utilization')

        plt.xlabel("Number of Servers")
        plt.ylabel("Server Utilization (%)")
        plt.xlim(0, num_servers)
        plt.ylim(0, 1)
        plt.title(title)

        plt.legend()

        plt.grid(True)
        plt.show()


    plot_server_utilization(util, "Server Utilization for Different Numbers of Servers")


    def get_bar_chart(data, labels, title):
        plt.figure(figsize=(10, 6))

        num_servers = range(1, len(data[0]) + 1)
        bar_width = 0.09

        for i, mean in enumerate(data):
            x_values = np.arange(len(labels)) + bar_width * i
            plt.bar(x_values, mean, width=bar_width, label=f"Server {i + 1}", alpha=0.7)

        if data == mean_waiting_time_by_servers:
            plt.ylim(400,700)

        plt.xlabel("Day of the Week")
        plt.ylabel("Time (units)")
        
        plt.title(title)
        plt.xticks(np.arange(len(labels)) + bar_width * (len(data) - 1) / 2, labels)
        plt.legend()

        plt.show()



    #get_bar_chart(mean_waiting_time_by_servers, list(daily_data_services.keys()), "Waiting Time")
    #get_bar_chart(mean_service_time_by_servers, list(daily_data_services.keys()), "Service Time")



            
        
        

    

        