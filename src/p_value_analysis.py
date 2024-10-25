import pandas as pd
import matplotlib.pyplot as plt
import qmplot

def significative_snarl_binary(file_path, output_snarl):

    # df : CHR POS P_Fisher P_Chi2
    df = pd.read_csv(file_path, sep='\t')
    df['P_Fisher'] = pd.to_numeric(df['P_Fisher'], errors='coerce')
    df['P_Chi2'] = pd.to_numeric(df['P_Chi2'], errors='coerce')
    df = df.dropna(subset=['P_Fisher', 'P_Chi2'])

    significance_threshold = 0.00001
    tupple_snarl = df[(df['P_Fisher'] < significance_threshold) & (df['P_Chi2'] < significance_threshold)][['CHR', 'POS', 'P_Fisher', 'P_Chi2']].itertuples(index=False, name=None)
    write_significative_snarl_binary(tupple_snarl, output_snarl)

def significative_snarl_quantitatif(file_path, output_snarl):
    
    df = pd.read_csv(file_path, sep='\t')
    df['P'] = pd.to_numeric(df['P'], errors='coerce')
    df = df.dropna(subset=['P'])

    significance_threshold = 0.00001
    tupple_snarl = df[df['P'] < significance_threshold][['CHR', 'POS', 'P']].itertuples(index=False, name=None)
    write_significative_snarl_quantitatif(tupple_snarl, output_snarl)

def write_significative_snarl_binary(tupple_snarl, output_snarl) :
    with open(output_snarl, "w") as f :
        for CHR, POS, P_Fisher, P_Chi2 in tupple_snarl :
            f.write(f'{CHR}\t{POS}\t{P_Fisher}\t{P_Chi2}\n')

def write_significative_snarl_quantitatif(tupple_snarl, output_snarl) :
    with open(output_snarl, "w") as f :
        for CHR, POS, P in tupple_snarl :
            f.write(f'{CHR}\t{POS}\t{P}\n')

def qq_plot(file_path, output_qqplot="output/qq_plot.png") :
    
    data = pd.read_csv(file_path, sep="\t")
    data = data.dropna(subset=['P'])

    # Create a Q-Q plot
    _, ax = plt.subplots(figsize=(6, 6), facecolor="w", edgecolor="k")
    qmplot.qqplot(data=data["P"],
           marker="o",
           xlabel=r"Expected $-log_{10}{(P)}$",
           ylabel=r"Observed $-log_{10}{(P)}$",
           ax=ax)

    plt.savefig(output_qqplot)

def plot_manhattan_quantitative(file_path, output_manhattan="output/manhattan_plot_quantitative.png") :
    
    data = pd.read_csv(file_path, sep="\t")
    data = data.dropna(how="any", axis=0)  # clean data

    _, ax = plt.subplots(figsize=(12, 4), facecolor='w', edgecolor='k')
    qmplot.manhattanplot(data=data,
                marker=".",
                chrom="CHR",
                sign_marker_p=1e-6,  # Genome wide significant p-value
                sign_marker_color="r",
                snp="POS",
                xlabel="Chromosome",
                ylabel=r"$-log_{10}{(P)}$",
                is_annotate_topsnp=True,
                text_kws={"fontsize": 12,  # The fontsize of annotate text
                            "arrowprops": dict(arrowstyle="-", color="k", alpha=0.6)},
                ax=ax)

    plt.savefig(output_manhattan)

def plot_manhattan_binary(file_path, output_manhattan="output/manhattan_plot_binary.png") :
    
    data = pd.read_csv(file_path, sep="\t")
    data = data.dropna(how="any", axis=0)  # clean data

    _, ax = plt.subplots(figsize=(12, 4), facecolor='w', edgecolor='k')
    qmplot.manhattanplot(data=data,
                  marker=".",
                  chrom="CHR",
                  sign_marker_p=1e-6,  # Genome wide significant p-value
                  sign_marker_color="r",
                  snp="ID",

                  xlabel="Chromosome",
                  ylabel=r"$-log_{10}{(P)}$",

                  sign_line_cols=["#D62728", "#2CA02C"],
                  hline_kws={"linestyle": "--", "lw": 1.3},

                  is_annotate_topsnp=True,
                  ld_block_size=500000,  # 500000 bp
                  text_kws={"fontsize": 12,  # The fontsize of annotate text
                            "arrowprops": dict(arrowstyle="-", color="k", alpha=0.6)},
                  ax=ax)

    plt.savefig(output_manhattan)

if __name__ == "__main__" :

    file_path = 'output/snarl_pan.tsv'
    output_snarl = "output/droso_top_significative_snarl.tsv"
    significative_snarl_quantitatif(file_path, output_snarl)
    qq_plot(file_path, output_qqplot="output/qq_plot.png")
    plot_manhattan_quantitative(file_path)

    #python3 src/p_value_analysis.py 
