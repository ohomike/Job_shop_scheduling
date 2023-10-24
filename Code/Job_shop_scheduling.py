import random
import pandas as pd
import matplotlib.pyplot as plt
def job_shop_scheduling(TASKS):
    # Create a list of machines and jobs from the input TASKS
    machines = sorted(list(set(task['machine'] for task in TASKS)))
    jobs = sorted(list(set(task['job'] for task in TASKS)))
    # Initialize dictionaries to track job and machine times
    job_times = {job: 0 for job in jobs}
    machine_times = {machine: 0 for machine in machines}
    # Create a schedule to store the order of tasks
    schedules = []
    while TASKS:
        # Find tasks with prec = None
        no_prec_tasks = [task for task in TASKS if task['prec'] is None]
        if no_prec_tasks:
            # Randomly choose one of the tasks with prec = None
            next_task = random.choice(no_prec_tasks)
        else:
            # If no task with prec = None is available, select any task randomly
            next_task = random.choice(TASKS)
        job, machine = next_task['job'], next_task['machine']
        start_time = max(job_times[job], machine_times[machine])
        end_time = start_time + next_task['dur']
        schedule = (job, machine, start_time, end_time)
        job_times[job] = end_time
        machine_times[machine] = end_time
        schedules.append(schedule)
        TASKS.remove(next_task)
    return schedules
def sampling_jss(TASKS , rev):
  all_schedules = {}
  for i in range(rev):
    # Make a copy of the original_TASKS to use in each example
    task = TASKS.copy()
    example_schedule = job_shop_scheduling(task)
    # Store the schedule in the dictionary with the example number as the key
    all_schedules[i] = example_schedule
  return all_schedules  
def Create_Df(result):
    df = pd.DataFrame(columns=['Example', 'Job', 'Machine', 'Start Time', 'End Time'])
    # Iterate through the schedules and add them to the DataFrame
    for example, schedule in result.items():
        for step, (job, machine, start_time, end_time) in enumerate(schedule, start=1):
            df = df.append({'Example': example, 'Job': job, 'Machine': machine, 'Start Time': start_time, 'End Time': end_time}, ignore_index=True)
    return df

original_TASKS = [
    {'job': 'J1', 'machine': 'M1', 'dur': 45, 'prec': None},
    {'job': 'J1', 'machine': 'M3', 'dur': 10, 'prec': ('J1', 'M1')},
    {'job': 'J1', 'machine': 'M2', 'dur': 20, 'prec': ('J1', 'M3')},
    {'job': 'J2', 'machine': 'M1', 'dur': 20, 'prec': ('J2', 'M2')},
    {'job': 'J2', 'machine': 'M2', 'dur': 10, 'prec': None},
    {'job': 'J2', 'machine': 'M3', 'dur': 34, 'prec': ('J2', 'M1')},
    {'job': 'J3', 'machine': 'M1', 'dur': 12, 'prec': ('J3', 'M3')},
    {'job': 'J3', 'machine': 'M2', 'dur': 17, 'prec': ('J3', 'M1')},
    {'job': 'J3', 'machine': 'M3', 'dur': 28, 'prec': None}]
result = sampling_jss(original_TASKS , 20)
df = Create_Df(result)
