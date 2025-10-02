from gen import Ag
import csv
import matplotlib.pyplot as plt


def read(filename):
    global num_tasks, num_machines, times
    with open(filename, "r") as f:
        data = f.read().split("\n")
        num_tasks, num_machines = map(int, data[0].split())
        
        times = [[0, set()] for i in range(num_tasks)]

        for i, line in enumerate(data[1:]):
            line_data = list(map(int, line.split()))
            
            times[i][0] = line_data[0]

            for task in line_data[1:]:
                times[task - 1][1].add(i)

def calc(chromo):
    global times, num_machines

    machines = [[0, 0] for i in range(num_machines)]
    ref_task = [-1] * num_machines
    concluidas = set()
    chromo = chromo[:]

    while chromo:
        new_chromo = []

        for task in chromo:
            idx = machines.index(min(machines, key=lambda x: x[0]))
            if times[task][1].issubset(concluidas):
                ref_task[idx] = task
                machines[idx][1] = times[task][0] # Tempo restante
            else:
                new_chromo.append(task) # Tarefas que ferem a restrição de prioridade são adiadas
            
            # Pegar o menor time left que não seja 0, para evitar ciclos em máquinas ociosas
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
    return max(machines)[0]


num_tasks = None
num_machines = None
times = None
read("dificil.txt")


population_size = [100]
elite_size = [2]
mut_prob = [0.05]
cross_prob = [0.8]
sel_mode = [1]
geracoes = [100]

all_data = []

for g in geracoes:
    for i in population_size:
        for e in elite_size:
            for m in mut_prob:
                for c in cross_prob:
                    for sel in sel_mode:
                        ag = Ag(i, chromo_size=num_tasks, mut_prob=m, cross_prob=c, elite_size=e, funct=calc, sel_mode=sel)
                        ag.fit(g)
                        mode = "roleta" if sel else "torneio"
                        all_data.append((ag.data, (m, e, i, c, mode, g)))


best_data, best_params = min(all_data, key=lambda x: x[0][-1][2])
print(f"Melhor execução: {best_params}\nDistância: {best_data[-1][2]}")
gens = list(range(1, len(best_data) + 1))

elite_vals = [t[0] for t in best_data]
plt.figure(figsize=(8, 5), dpi=300)
plt.plot(gens, elite_vals, linewidth=2, marker='o', markersize=4)
plt.xlabel('Geração')
plt.ylabel('Distância')
plt.title('Melhor Individuo')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('best.png')
plt.close()

max_vals    = [t[1] for t in best_data]
min_vals    = [t[2] for t in best_data]
mean_vals   = [t[3] for t in best_data]
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
plt.savefig('best_2.png')
plt.close()

plt.figure(figsize=(10, 6), dpi=300)

for idx, (run_data, params) in enumerate(all_data, start=1):
    mean_run = [t[3] for t in run_data]
    gens_run = list(range(1, len(run_data) + 1))
    plt.plot(gens_run, mean_run, linewidth=1.5, alpha=0.7, label=f'Run {idx}')

plt.xlabel('Geração')
plt.ylabel('Distância Média')
plt.title('Distância Média de Cada Execução')
plt.legend(fontsize='small', ncol=2)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('all.png')
plt.close()

with open('all_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['mutate_prob', 'elite_size', 'individuos', 'cross_prob', 'selecao', 'geracoes', 'geracao', 'elite', 'max', 'min', 'mean', 'median', 'std'])
    for run_data, (m, e, i, c, sel, gen_total) in all_data:
        for idx, values in enumerate(run_data, start=1):
            elite, mx, mn, mean, median, std = values
            writer.writerow([m, e, i, c, sel, gen_total, idx, elite, mx, mn, mean, median, std])
