import argparse
import list_snarl_paths
import snarl_vcf_parser
import p_value_analysis
import time

parser = argparse.ArgumentParser('List path through the netgraph of each snarl in a pangenome')
parser.add_argument('-p', help='the input pangenome .pg file', required=True)
parser.add_argument('-d', help='the input distance index .dist file',required=True)
parser.add_argument("-t", type=list_snarl_paths.check_threshold, help='Children threshold', required=False)
parser.add_argument("-v", type=snarl_vcf_parser.check_format_vcf_file, help="Path to the vcf file (.vcf or .vcf.gz)", required=True)
parser.add_argument("-r", type=snarl_vcf_parser.check_format_vcf_file, help="Path to the vcf file referencing all position of snarl (.vcf or .vcf.gz)")

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-b", "--binary", type=snarl_vcf_parser.check_format_group_snarl, help="Path to the binary group file (.txt or .tsv)")
group.add_argument("-q", "--quantitative", type=snarl_vcf_parser.check_format_pheno, help="Path to the quantitative phenotype file (.txt or .tsv)")
parser.add_argument("-o", "--output", type=str, required=False, help="Path to the output file")
args = parser.parse_args()

# Create list of path snarls to analyse
start = time.time()
stree, pg, root = list_snarl_paths.parse_graph_tree(args.p, args.d)
snarls = list_snarl_paths.create_snarls(stree, root)

if args.t :
    snarl_paths = list_snarl_paths.loop_over_snarls(stree, snarls, pg, args.t)
else :
    snarl_paths = list_snarl_paths.loop_over_snarls(stree, snarls, pg)

print(f"Time list snarl paths : {time.time() - start} s")

# Parse vcf merge and fill the matrix
start = time.time()
vcf_dict = snarl_vcf_parser.parse_vcf_to_dict(args.vcf_pangenome)
vcf_object = snarl_vcf_parser.SnarlProcessor(args.v, vcf_dict)
vcf_object.fill_matrix(args.vcf_path)
print(f"Time Matrix : {time.time() - start} s")

start = time.time()
# Binary case 
if args.binary:
    binary_group = snarl_vcf_parser.parse_group_file(args.binary)
    if args.output :
        vcf_object.binary_table(snarl_paths, binary_group, args.output)
    else :
        vcf_object.binary_table(snarl_paths, binary_group)

    output_binary_file_manh = "output/manhattan_plot_binary.png"
    output_binary_file_qq = "output/qq_plot_binary.png"
    output_binary_file_significatif = "output/top_variant_quantitative.tsv"
    p_value_analysis.significative_snarl_binary(args.output, output_binary_file_significatif)
    p_value_analysis.plot_manhattan_binary(args.output, output_binary_file_manh)
    p_value_analysis.qq_plot(args.output, output_binary_file_qq)

# Quantitative case 
if args.quantitative:
    quantitative = snarl_vcf_parser.parse_pheno_file(args.quantitative)
    if args.output :
        vcf_object.quantitative_table(snarl_paths, quantitative, args.output)
    else :
        vcf_object.quantitative_table(snarl_paths, quantitative)

    output_quantitative_file_manh = "output/manhattan_plot_quantitative.png"
    output_quantitative_file_qq = "output/qq_plot_quantitative.png"
    output_quantitative_file_significatif = "output/top_variant_quantitative.tsv"
    p_value_analysis.significative_snarl_quantitatif(args.output, output_quantitative_file_significatif)
    p_value_analysis.plot_manhattan_quantitative(args.output, output_quantitative_file_manh)
    p_value_analysis.qq_plot(args.output, output_quantitative_file_qq)

print(f"Time P-value : {time.time() - start} s")

"""
    python3 src/snarl_project.py -p ../../snarl_data/fly.pg -d ../../snarl_data/fly.dist -v ../../snarl_data/fly.merged.vcf \
    -q ../../snarl_data/updated_phenotypes.txt -o output/simulation_quantitative.tsv
"""