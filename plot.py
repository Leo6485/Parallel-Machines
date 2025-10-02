import matplotlib.pyplot as plt
import csv




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
                elite, mx, mn, mean, median, std, _ = values
                writer.writerow([m, e, i, c, sel, gen_total, idx, elite, mx, mn, mean, median, std])