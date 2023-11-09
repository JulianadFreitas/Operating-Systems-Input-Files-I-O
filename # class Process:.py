# class Process:
#     def __init__(self, name, execution_time, chance_to_request_ES):
#         self.name = name
#         self.execution_time = execution_time
#         self.chance_to_request_ES = chance_to_request_ES

# def generate_random_info(chance_to_request_ES):
#     # Implement your function here
#     pass

# def execute_processes(processes):
#     blocked_processes = []
#     global_counter = 0
#     current_execution_time = 0
#     current_time_unit = 0

#     while processes:
#         current_process = processes.pop(0)

#         random_info, blocking_point = generate_random_info(current_process.chance_to_request_ES)
#         if random_info:
#             print(random_info)
#             global_counter = 0
#             current_execution_time = 0

#         while current_process.execution_time > 0:
#             if blocking_point is not None and current_time_unit == blocking_point:
#                 blocked_processes.append((current_process.name, devices[2]))  # Assuming devices is defined elsewhere
#                 break

#             print(f"Time {current_time_unit}: {current_process.name} | {current_process.execution_time}")
#             current_process.execution_time -= 1
#             current_time_unit += 1
#             # time.sleep(1)

#             global_counter += 1
#             current_execution_time += 1

#             if global_counter == 10 or current_execution_time == 10:
#                 break

#         if current_process.execution_time > 0:
#             processes.append(current_process)
#         else:
#             print(f"{current_process.name} completed.")

# # Usage
# processes = [Process('Process1', 10, 5), Process('Process2', 15, 7)]
# execute_processes(processes)




class Process:
    def __init__(self, name, execution_time, chance_to_request_ES):
        self.name = name
        self.execution_time = execution_time
        self.chance_to_request_ES = chance_to_request_ES

def generate_random_info(chance_to_request_ES):
    # Implement your function here
    pass

def execute_processes(processes):
    blocked_processes = []
    global_counter = 0
    current_execution_time = 0
    current_time_unit = 0

    while processes:
        current_process = processes.pop(0)

        random_info, blocking_point = generate_random_info(current_process.chance_to_request_ES)
        if random_info:
            print(random_info)
            global_counter = 0
            current_execution_time = 0

        while current_process.execution_time > 0:
            if blocking_point is not None and current_time_unit == blocking_point:
                blocked_processes.append((current_process.name, devices[2]))  # Assuming devices is defined elsewhere
                break

            print(f"Time {current_time_unit}: {current_process.name} | {current_process.execution_time}")
            current_process.execution_time -= 1
            current_time_unit += 1
            # time.sleep(1)

            global_counter += 1
            current_execution_time += 1

            if global_counter == 10 or current_execution_time == 10:
                break

        if current_process.execution_time > 0:
            processes.append(current_process)
        else:
            print(f"{current_process.name} completed.")

# Usage
processes = [Process('Process1', 10, 5), Process('Process2', 15, 7)]
execute_processes(processes)