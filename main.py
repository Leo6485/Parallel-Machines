from gen import Ag
from plot import export_csv, plot_all_runs, plot_best, plot_stats
from input import read
from time import time

# Calcula a função objetivo e realiza uma correção para indivíduos inválidos
def calc(chromo):
    global times, num_machines

    machines = [[0, 0] for i in range(num_machines)]
    ref_task = [-1] * num_machines
    concluidas = set()
    chromo = chromo[:]

    sequencia_corrigida = []

    while chromo:
        new_chromo = []

        for task in chromo:
            # Como todas as máquinas são iguais, basta executar na que está livre, logo a sequência determina onde cada task irá ser executada
            # Isso é válido para os problemas "facil.txt" e "dificil.txt"
            idx = machines.index(min(machines, key=lambda x: x[0]))
            if times[task][1].issubset(concluidas):
                ref_task[idx] = task
                machines[idx][1] = times[task][0] # Tempo restante
                sequencia_corrigida.append(task)
            else:
                new_chromo.append(task) # Tarefas que ferem a restrição de prioridade são adiadas
            
            
            # Calcula o menor tempo restante nas máquinas ocupadas
            mtl = [i[1] for i in machines]
            temp = sorted(list(filter(lambda x: x, mtl)))
            temp.append(0)
            min_machine = temp[0]

            for i in range(len(machines)):
                if machines[i][1] == 0: continue

                machines[i][1] -= min_machine
                machines[i][0] += min_machine
                if machines[i][1] == 0:
                    concluidas.add(ref_task[i])

        chromo = new_chromo
    return max(machines)[0], sequencia_corrigida


# Valida a solução e formata a saída
def calc2(chromo):
    global times, num_machines

    machines = [0]*num_machines
    machines_result = [[] for i in range(num_machines)]
    concluidas = set()
    for task in chromo:
        idx = machines.index(min(machines))
        machines[idx] += times[task][0]
        
        if set(times[task][1]).issubset(concluidas):
            concluidas.add(task)
            machines_result[idx].append(f"{task - 1}({machines[idx]})")
        else:
            print("Sequência inválida")
            return float("inf")

    for i, machine in enumerate(machines_result):
        print(f"Máquina {i} time: task\n{' -> '.join(machine)}")
    
    print(f"Resultado obtido: {max(machines)}")
    return max(machines)

num_tasks, num_machines, times = read(filename="inputs/dificil.txt")

# --------------------
# Teste fatorial
# --------------------

def fact_test():
    population_size = [100]
    elite_size = [2]
    mut_prob = [0.05]
    cross_prob = [0.8]
    sel_mode = [1] # 0 ou 1
    geracoes = [10]

    executions_data = []

    for g in geracoes:
        for i in population_size:
            for e in elite_size:
                for m in mut_prob:
                    for c in cross_prob:
                        for sel in sel_mode:
                            ag = Ag(
                                size=i, 
                                chromo_size=num_tasks, 
                                mut_prob=m, 
                                cross_prob=c, 
                                elite_size=e, 
                                funct=calc, 
                                sel_mode=sel
                            )
                            ag.fit(g)
                            mode = "roleta" if sel else "torneio"
    
                            executions_data.append((ag.data, (m, e, i, c, mode, g)))
    
                            executions_data.append((ag.data, (m, e, i, c, mode, g)))
    
    best_data, best_params = min(executions_data, key=lambda x: x[0][-1][2])
    print(f"Melhor execução: {best_params}\nDistância: {best_data[-1][2]}")

    print(f"Sequência: {best_data[-1][6]}")
    plot_best(best_data)
    plot_stats(best_data)
    plot_all_runs(executions_data)


    export_csv(executions_data)


start = time()
ag = Ag(size=100, chromo_size=num_tasks, mut_prob=0.05, cross_prob=0.8, elite_size=2, funct=calc, sel_mode=1)
ag.fit(10)

print(ag.data[-1][6])
calc2(ag.data[-1][6])

print(f"Tempo de execução: {(time() - start):.2f}")