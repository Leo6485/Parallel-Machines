from gen import Ag
import csv
import matplotlib.pyplot as plt
from input import read



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




def plot_best(best_data):
    gens = list(range(1, len(best_data) + 1))
    elite_vals = [t[0] for t in best_data]
    
    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(gens, elite_vals, linewidth=2, marker='o', markersize=4)
    plt.xlabel('Geração')
    plt.ylabel('Distância')
    plt.title('Melhor Individuo')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('results/best.png')
    plt.close()


def plot_stats(best_data):
    gens = list(range(1, len(best_data) + 1))
    max_vals = [t[1] for t in best_data]
    min_vals = [t[2] for t in best_data]
    mean_vals = [t[3] for t in best_data]
    median_vals = [t[4] for t in best_data]

    plt.figure(figsize=(8, 5), dpi=300)
    plt.plot(gens, min_vals,    label='Melhor',  linewidth=2)
    plt.plot(gens, max_vals,    label='Pior',    linewidth=2)
    plt.plot(gens, mean_vals,   label='Média',   linewidth=2)
    plt.plot(gens, median_vals, label='Mediana', linewidth=2)
    plt.xlabel('Geração')
    plt.ylabel('Distância')
    plt.title('Dados da Melhor Execução')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('results/best_2.png')
    plt.close()


def plot_all_runs(executions_data):
    plt.figure(figsize=(10, 6), dpi=300)
    for idx, (run_data, _) in enumerate(executions_data, start=1):
        mean_run = [t[3] for t in run_data]
        gens_run = list(range(1, len(run_data) + 1))
        plt.plot(gens_run, mean_run, linewidth=1.5, alpha=0.7, label=f'Run {idx}')
    plt.xlabel('Geração')
    plt.ylabel('Distância Média')
    plt.title('Distância Média de Cada Execução')
    plt.legend(fontsize='small', ncol=2)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('results/all.png')
    plt.close()


def export_csv(executions_data, filename='results/executions_data.csv'):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['mutate_prob', 'elite_size', 'individuos', 'cross_prob', 'selecao', 'geracoes', 'geracao', 'elite', 'max', 'min', 'mean', 'median', 'std'])
        for run_data, (m, e, i, c, sel, gen_total) in executions_data:
            for idx, values in enumerate(run_data, start=1):
                elite, mx, mn, mean, median, std = values
                writer.writerow([m, e, i, c, sel, gen_total, idx, elite, mx, mn, mean, median, std])


num_tasks, num_machines, times = read(filename="inputs/dificil.txt")

population_size = [100]
elite_size      = [2]
mut_prob        = [0.05]
cross_prob      = [0.8]
sel_mode        = [1] # 0 ou 1
geracoes        = [100]


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


best_data, best_params = min(executions_data, key=lambda x: x[0][-1][2])
print(f"Melhor execução: {best_params}\nDistância: {best_data[-1][2]}")

plot_best(best_data)
plot_stats(best_data)
plot_all_runs(executions_data)


export_csv(executions_data)