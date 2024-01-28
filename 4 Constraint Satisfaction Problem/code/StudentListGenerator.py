import random
import os

def generate_random_time(available_times=None):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_hours = range(1, 13)
    time_minutes = [0, 15, 30, 45]
    meridiems = ['AM', 'PM']

    while True:  # keep generating until we find an available time if a list is provided
        day = random.choice(days)
        hour = random.choice(time_hours)
        minute = random.choice(time_minutes)
        meridiem = random.choice(meridiems)
        time = f"{day} {hour}:{str(minute).zfill(2)} {meridiem}"
        if not available_times or time in available_times:
            return time

def generate_student_list(num_students, num_times, leader_times):
    student_data = {}
    for i in range(1, num_students + 1):
        student_name = f"student{i}"
        times = [generate_random_time(leader_times) for _ in range(num_times)]
        student_data[student_name] = times
    return student_data

def generate_section_leader_list(num_leaders, num_times):
    leader_data = {}
    all_leader_times = []
    for i in range(1, num_leaders + 1):
        leader_name = f"*leader{i}"
        times = [generate_random_time() for _ in range(num_times)]
        all_leader_times.extend(times)
        leader_data[leader_name] = times
    return leader_data, list(set(all_leader_times))

def save_to_file(filename, data):
    with open(filename, 'w') as file:
        for name, times in data.items():
            file.write(f"{name}, {', '.join(times)}\n")

def main():
    num_students = 3
    num_leaders = 3
    num_times = 3

    leaders, leader_times = generate_section_leader_list(num_leaders, num_times)
    students = generate_student_list(num_students, num_times, leader_times)

    all_data = {**students, **leaders}
    filename = f"input.txt"
    save_to_file(filename, all_data)

    print(f"Student list generated successfully!")

if __name__ == "__main__":
    main()
