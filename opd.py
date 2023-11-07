import random

def mm1_queue_simulation(arrival_rate, registration_rate, consultation_rate, pharmacy_rate, num_customers):
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
        registration_time = random.expovariate(registration_rate)
        consultation_time = random.expovariate(consultation_rate)
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
            waiting_time = random.expoviate(registration_rate)
            total_waiting_time_registration -= waiting_time
            queue_length_consultation += 1
            waiting_times_registration.append(total_waiting_time_registration)
        consultation_times.append(clock + waiting_time)

        # Pharmacy Queue
        if queue_length_consultation > 0:
            queue_length_consultation -= 1
            waiting_time = random.expoviate(consultation_rate)
            total_waiting_time_consultation -= waiting_time
            queue_length_pharmacy += 1
            waiting_times_consultation.append(total_waiting_time_consultation)
        pharmacy_times.append(clock + waiting_time)

        waiting_times_pharmacy.append(0)

        time = min(registration_times[-1], consultation_times[-1], pharmacy_times[-1])

    # Calculate mean waiting times in the system (Ws) and mean waiting times in the queue (Wq)
    Ws_registration = sum(waiting_times_registration) / num_customers
    Ws_consultation = sum(waiting_times_consultation) / num_customers
    Ws_pharmacy = sum(waiting_times_pharmacy) / num_customers

    Wq_registration = Ws_registration - 1 / registration_rate
    Wq_consultation = Ws_consultation - 1 / consultation_rate
    Wq_pharmacy = Ws_pharmacy - 1 / pharmacy_rate

    return Ws_registration, Wq_registration, Ws_consultation, Wq_consultation, Ws_pharmacy, Wq_pharmacy

# Define data for each day of the week
day_data = {
    "Monday": {
        "interarrival_time": 4.90,
        "registration_rate": 12.22,
        "consultation_rate": 16.67,
        "pharmacy_rate": 16.85,
        "num_customers": 75,
    },
    "Tuesday": {
        "interarrival_time": 5.24,
        "registration_rate": 11.45,
        "consultation_rate": 15.36,
        "pharmacy_rate": 15.82,
        "num_customers": 67,
    },
    "Wednesday": {
        "interarrival_time": 5.19,
        "registration_rate": 11.54,
        "consultation_rate": 15.78,
        "pharmacy_rate": 15.71,
        "num_customers": 71,
    },
    "Thursday": {
        "interarrival_time": 4.67,
        "registration_rate": 12.86,
        "consultation_rate": 15.91,
        "pharmacy_rate": 17.28,
        "num_customers": 87,
    },
    "Friday": {
        "interarrival_time": 4.58,
        "registration_rate": 13.10,
        "consultation_rate": 16.89,
        "pharmacy_rate": 15.61,
        "num_customers": 76,
    },
}

# Run the simulation for each day of the week
for day, data in day_data.items():
    interarrival_time = data["interarrival_time"]
    registration_rate = data["registration_rate"]
    consultation_rate = data["consultation_rate"]
    pharmacy_rate = data["pharmacy_rate"]
    num_customers = data["num_customers"]

    Ws_registration, Wq_registration, Ws_consultation, Wq_consultation, Ws_pharmacy, Wq_pharmacy = mm1_queue_simulation(
        1 / interarrival_time,
        1 / registration_rate,
        1 / consultation_rate,
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
day_data = {
    "Monday": {
        "Ls": 0.2559,
        "Ls2": 2.7551,
        "Ls3": 2.6435,
        "Lq": 0.0521,
        "Lq2": 2.0214,
        "Lq3": 1.9180,
    },
    "Tuesday": {
        "Ls": 0.2402,
        "Ls2": 2.8571,
        "Ls3": 2.6185,
        "Lq": 0.0465,
        "Lq2": 2.1164,
        "Lq3": 1.8949,
    },
    "Wednesday": {
        "Ls": 0.2424,
        "Ls2": 2.7272,
        "Ls3": 2.7653,
        "Lq": 0.0473,
        "Lq2": 1.9955,
        "Lq3": 2.0308,
    },
    "Thursday": {
        "Ls": 0.3762,
        "Ls2": 4.2051,
        "Ls3": 2.9038,
        "Lq": 0.1028,
        "Lq2": 3.3972,
        "Lq3": 2.1600,
    },
    "Friday": {
        "Ls": 0.3282,
        "Ls2": 3.4615,
        "Ls3": 5.2142,
        "Lq": 0.0811,
        "Lq2": 2.6856,
        "Lq3": 4.3752,
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
