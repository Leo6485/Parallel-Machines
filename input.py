
def read(filename):
    with open(filename, "r") as f:
        data = f.read().split("\n")
        num_tasks, num_machines = map(int, data[0].split())

        times = [[0, set()] for i in range(num_tasks)]

        for i, line in enumerate(data[1:]):
            line_data = list(map(int, line.split()))
            
            times[i][0] = line_data[0]

            for task in line_data[1:]:
                times[task - 1][1].add(i) # As tasks na lista tem i adicionado como prioridade, -1 pois a task 1 terá o id 0
    
    return num_tasks, num_machines, times