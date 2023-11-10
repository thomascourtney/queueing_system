import random

def mm1_queue_simulation(arrival_rate, registration_rate_per_hour, consultation_rate_per_hour, pharmacy_rate, num_customers):
    time = 0
    clock = 0
    arrival_times = []
    registration_times = []
    consultation_times = []
    pharmacy_times = []
    waiting_times_registration = []
    waiting_times_consultation = []
    waiting_times_pharmacy = []
    queue_length_registration = 0
    queue_length_consultation = 0
    queue_length_pharmacy = 0
    total_waiting_time_registration = 0
    total_waiting_time_consultation = 0
    total_waiting_time_pharmacy = 0

    for _ in range(num_customers):
        interarrival_time = random.expovariate(arrival_rate)
        registration_time = random.expovariate(registration_rate_per_hour)
        consultation_time = random.expovariate(consultation_rate_per_hour)
        pharmacy_time = random.expovariate(pharmacy_rate)

        clock += interarrival_time
        arrival_times.append(clock)

        # Registration Queue
        if clock < time:
            waiting_time = time - clock
            total_waiting_time_registration += waiting_time
            queue_length_registration += 1
        else:
            waiting_time = 0
        registration_times.append(clock + waiting_time)



        # Consultation Queue
        if queue_length_registration > 0:
            queue_length_registration -= 1
            waiting_time = random.expovariate(consultation_rate_per_hour)
            total_waiting_time_registration += waiting_time
            queue_length_consultation += 1
            waiting_times_registration.append(total_waiting_time_registration)
        else:
            waiting_time = 0
        consultation_times.append(clock + waiting_time)

        # Pharmacy Queue
        if queue_length_consultation > 0:
            queue_length_consultation -= 1
            waiting_time = random.expoviate(pharmacy_rate)
            total_waiting_time_consultation += waiting_time
            queue_length_pharmacy += 1
            waiting_times_consultation.append(total_waiting_time_consultation)
        else:
            waiting_time = 0
        pharmacy_times.append(clock + waiting_time)

        waiting_times_pharmacy.append(0)

        time = min(registration_times[-1], consultation_times[-1], pharmacy_times[-1])

    # Calculate mean waiting times in the system (Ws) and mean waiting times in the queue (Wq)
    Ws_registration = sum(waiting_times_registration) / num_customers
    Ws_consultation = sum(waiting_times_consultation) / num_customers
    Ws_pharmacy = sum(waiting_times_pharmacy) / num_customers

    Wq_registration = Ws_registration - 1 / registration_rate_per_hour
    Wq_consultation = Ws_consultation - 1 / consultation_rate_per_hour
    Wq_pharmacy = Ws_pharmacy - 1 / pharmacy_rate

    return Ws_registration, Wq_registration, Ws_consultation, Wq_consultation, Ws_pharmacy, Wq_pharmacy
"""
# Define data for each day of the week
day_data = {
    "Monday": {
        "interarrival_time": 4.90,
        "arrival_rate": 12.22,
        "registration_rate_per_hour": 60,
        "consultation_rate_per_hour": 16.67,
        "pharmacy_rate": 16.85,
        "num_customers": 75,
    },
    "Tuesday": {
        "interarrival_time": 5.24,
        "arrival_rate": 11.45,
        "registration_rate_per_hour": 59.11,
        "consultation_rate_per_hour": 15.36,  # Corrected key here
        "pharmacy_rate": 15.82,
        "num_customers": 67,
    },
    "Wednesday": {
        "interarrival_time": 5.19,
        "arrival_rate": 11.4,
        "registration_rate_per_hour": 591.6,
        "consultation_rate_per_hour": 15.78,
        "pharmacy_rate": 15.71,
        "num_customers": 71,
    },
    "Thursday": {
        "interarrival_time": 4.67,
        "arrival_rate": 12.86,
        "registration_rate_per_hour": 47.02,
        "consultation_rate_per_hour": 15.91,
        "pharmacy_rate": 17.28,
        "num_customers": 87,
    },
    "Friday": {
        "interarrival_time": 4.58,
        "arrival_rate": 13.10,
        "registration_rate_per_hour": 53.02,
        "consultation_rate_per_hour": 16.89,
        "pharmacy_rate": 15.61,
        "num_customers": 76,
    },
}
"""

day_data_services = {
    "Monday": {
        "interarrival_time": 4.90,
        "arrival_rate": 12.22,
        "num_customers": 75,
        "service_rate": 93.52,  # registration_rate + consultation_rate + pharmacy_rate
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
        "service_rate": 622.09,  # Corrected the sum of registration_rate, consultation_rate, pharmacy_rate
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


# Run the simulation for each day of the week
for day, data in day_data.items():
    interarrival_time = data["interarrival_time"]
    registration_rate_per_hour = data["registration_rate_per_hour"]
    consultation_rate_per_hour = data["consultation_rate_per_hour"]
    pharmacy_rate = data["pharmacy_rate"]
    num_customers = data["num_customers"]

    Ws_registration, Wq_registration, Ws_consultation, Wq_consultation, Ws_pharmacy, Wq_pharmacy = mm1_queue_simulation(
        1 / interarrival_time,
        1 / registration_rate_per_hour,
        1 / consultation_rate_per_hour,
        1 / pharmacy_rate,
        num_customers
    )

    print(f"Mean Waiting Time in Registration System for {day} (Ws): {Ws_registration:.2f} minutes")
    print(f"Mean Waiting Time in Registration Queue for {day} (Wq): {Wq_registration:.2f} minutes")
    print(f"Mean Waiting Time in Consultation System for {day} (Ws): {Ws_consultation:.2f} minutes")
    print(f"Mean Waiting Time in Consultation Queue for {day} (Wq): {Wq_consultation:.2f} minutes")
    print(f"Mean Waiting Time in Pharmacy System for {day} (Ws): {Ws_pharmacy:.2f} minutes")
    print(f"Mean Waiting Time in Pharmacy Queue for {day} (Wq): {Wq_pharmacy:.2f} minutes\n")

# Define the data for Ls, Ls2, Ls3, Lq, Lq2, and Lq3 for each day of the week
day_data_patients = {
    "Monday": {
        "Ls": 0.2559,
        "Lq": 0.0521,
    },
    "Tuesday": {
        "Ls": 0.2402,
        "Lq": 0.0465,
    },
    "Wednesday": {
        "Ls": 0.2424,
        "Lq": 0.0473,
    },
    "Thursday": {
        "Ls": 0.3762,
        "Lq": 0.1028,
    },
    "Friday": {
        "Ls": 0.3282,
        "Lq": 0.0811,
    },
}



# Specify the day you are interested in
selected_day = "Monday"  # You can change this to any day of the week

# Access the data for the selected day
Ls = day_data[selected_day]["Ls"]
Ls2 = day_data[selected_day]["Ls2"]
Ls3 = day_data[selected_day]["Ls3"]
Lq = day_data[selected_day]["Lq"]
Lq2 = day_data[selected_day]["Lq2"]
Lq3 = day_data[selected_day]["Lq3"]

# Now you have the calculated values for the selected day
print(f"Number of Patients in Registration System (Ls1) for {selected_day}: {Ls}")
print(f"Number of Patients in Consultation System (Ls2) for {selected_day}: {Ls2}")
print(f"Number of Patients in Pharmacy System (Ls3) for {selected_day}: {Ls3}")
print(f"Number of Patients in Registration Queue (Lq1) for {selected_day}: {Lq}")
print(f"Number of Patients in Consultation Queue (Lq2) for {selected_day}: {Lq2}")
print(f"Number of Patients in Pharmacy Queue (Lq3) for {selected_day}: {Lq3}\n")

