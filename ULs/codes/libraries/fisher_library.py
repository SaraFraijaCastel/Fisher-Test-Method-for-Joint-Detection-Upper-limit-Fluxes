
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2
import csv
def process_file(df, ref_psf,transit):
    results = []
    for _, row in df.iterrows():
        name = row['Name']
        sig = row['Significance']
        psf = row['Error_Radius']
        p_val =norm.cdf(abs(sig))
        pdf_val =1-norm.pdf(abs(sig))
        if psf>ref_psf:
            trials_factor= (psf**2) / (ref_psf**2)
        else:
            trials_factor=1
        p_corr = np.power(p_val, trials_factor)
        sig_corr = -norm.isf(p_corr)
        results.append((name,transit, sig, sig_corr, p_val, 1-p_corr, pdf_val))
    return results

def fisher_combined(pvalues):
    X2 = -2 * np.sum(np.log(pvalues))
    dof = 2 * len(pvalues)
    p_comb = chi2.sf(X2, dof)
    return X2, dof, p_comb

def run_fisher_test(config):
    file_1_1 = config['File_1st_transit']
    file_2_1 = config['File_2nd_transit']
    GRBs_INFO=config['GRBsINFO']
    file_1=pd.read_csv(file_1_1,sep='\s+',names=['Name','Spectrum','TS','Significance','Flux', 'lowerErr',   'upperErr' , 'lowerBound ', 'upperBound'])
    file_2=pd.read_csv(file_2_1,sep='\s+',names=['Name','Spectrum','TS','Significance','Flux', 'lowerErr',   'upperErr' , 'lowerBound ', 'upperBound'])
    GRBs=pd.read_csv(GRBs_INFO)
    file1_1=pd.merge(left=file_1,right=GRBs,on='Name',how='left')
    file2_1=pd.merge(left=file_2,right=GRBs,on='Name',how='left')
    file2=file2_1[file2_1['Name']!='GRB200415367']
    file1=file1_1[file1_1['Name']!='GRB200415367']
    ref_psf = config['bin_size']
    NAME=config['name']
    # coord1=config['File_1st_transit_coord'];coord_1=pd.read_csv(coord1)
    # coord2=config['File_2nd_transit_coord'];coord_1=pd.read_csv(coord2)
    data1 = process_file(file1, ref_psf,1)
    data2 = process_file(file2, ref_psf,2)
    all_data= data1 + data2
    significances = [r[2] for r in all_data if not np.isnan(r[2])]
    corrected_significances = [r[3] for r in all_data if not np.isnan(r[3])]
    corrected_pvalues = [r[5] for r in all_data if not np.isnan(r[5])]
    X2, dof, p_comb = fisher_combined(corrected_pvalues)
    z = ((X2 / dof)**(1/3) - (1 - 2/(9*dof))) / np.sqrt(2/(9*dof))
    p_norm = norm.sf(z)
    Lenght=len(corrected_pvalues)
    print("=== Resultados del Test de Fisher ===")
    print(f"X² = {X2:.2f}, dof = {dof}")
    print(f"p-value combinado (chi²) = {p_comb:.2e}")
    print(f"Significance combinada ≈ {z:.2f}σ")
    print(f"p-value (normal approx) ≈ {p_norm:.2e}")
    print(f'The list of p-values are{corrected_pvalues}')
    print(f'List lenght:{len(corrected_pvalues)}')
    print(f'The list of corrected significances are{corrected_significances}')
    print(f'The list of original significances are{significances}')
    print(f'List corrected  lenght:{len(corrected_significances)}')
    print(f'List not corrected lenght:{len(significances)}')
    print(f'Lenght pvalues{Lenght}')
    output_dir = os.path.join(config['PATH_LATEX'], f"Upper_Limits/PSF_{config['bin_size']}/{config['spectral_index']}/")
    dataframe_dir=os.path.join(output_dir, f'{NAME}.csv')
    # all_data.to_csv(dataframe_dir)
    return all_data, X2, dof, p_comb, z, p_norm

def generate_latex_report(all_data, X2, dof, p_comb, z, p_norm, config,psf):
    import matplotlib.pyplot as plt

    output_dir = os.path.join(config['PATH_LATEX'], f"Upper_Limits/PSF_{config['bin_size']}/{config['spectral_index']}/")
    output_tex = f"fisher_results_{config['bin_size']}_{config['spectral_index']}.tex"
    output_tex_var = f"fisher_var_{config['bin_size']}_{config['spectral_index']}.tex"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Filtrar NaNs
    valid_data = [row for row in all_data if not np.isnan(row[3])]
    corrected_significances = [row[3] for row in valid_data]

    # Histograma de significancias corregidas
    plt.figure()
    bins = np.arange(0, 3, 0.3)
    plt.hist(corrected_significances, bins=bins, edgecolor='black')
    plt.xlabel('Significance Corregida')
    plt.ylabel('Frecuencia')
    plt.ylim([0, 5])
    plt.title('Histogram of Corrected Significances')
    hist_filename = os.path.join(output_dir, 'corrected_significance_hist.png')
    plt.savefig(hist_filename)
    plt.close()

    # Tabla LaTeX
    header = ("\\textbf{GRB} & \\textbf{Transit} & \\textbf{Significance} & "
              "\\textbf{Significance Corregida} & \\textbf{p-value} & "
              "\\textbf{Corrected p-value} & \\textbf{PDF} \\\\ \\midrule\n")
    data_rows = "\n".join([
        "{} & {} & {:.2f} & {:.2f} & {:.3e} & {:.3e} & {:.3e} \\\\".format(name, transit, sig, corr_sig, p_val, corr_p, pdf_val)
        for name, transit, sig, corr_sig, p_val, corr_p, pdf_val in valid_data
    ])
    table = (
        "\\begin{table}[h!]\n"
        "\\centering\n"
        "\\resizebox{\\textwidth}{!}{%\n"
        "\\begin{tabular}{l c c c c c c}\n"
        "\\toprule\n" + header + data_rows + "\n\\bottomrule\n"
        "\\end{tabular}%\n"
        "}\n\\caption{Lista de GRBs with sus Transits, Significances, Significances Corregidas, p-values, "
        "p-values Corregidos y valores PDF.}\n\\end{table}"
    )

    figure = (
        "\\begin{figure}[h!]\n"
        "\\centering\n"
        "\\includegraphics[width=0.6\\textwidth]{corrected_significance_hist.png}\n"
        "\\caption{Histogram of Corrected Significances.}\n"
        "\\end{figure}"
    )

    critical_value = chi2.ppf(0.95, dof)
    decision = "rechazamos" if X2 > critical_value else "no rechazamos"
    
    conclusion = (
        "\\section*{{Conclusion}}\n"
        "The Fisher combined test integrates individual p-values to evaluate a global hypothesis.\n"
        "The resulting test statistic was $X^2 = {:.3f}$ with {:d} degrees of freedom.\n".format(X2, dof) +
        "For a significance level of 0.05, the critical value is {:.3f}.\n".format(critical_value) +
        "Since $X^2$ is {} than the critical value, we {} the null hypothesis of independence.\n".format(
            "greater" if X2 > critical_value else "less than or equal", decision) +
        "Normal approximation: p-value = {:.3e}, significance ≈ {:.2f} sigma.\n".format(p_norm, z)
    )
    if psf == 0.3:
        fisher = (f"\\newcommand\\FisherProb{{{p_comb:.2e}}}\n"
                f"\\newcommand\\FisherProbChi{{{X2:.3f}}}\n")
    elif psf == 0.15:
        fisher = (f"\\newcommand\\FisherProbl{{{p_comb:.2e}}}\n"
                f"\\newcommand\\FisherProbChil{{{X2:.3f}}}\n")
    elif psf == 0.6:
                fisher = (f"\\newcommand\\FisherProbh{{{p_comb:.2e}}}\n"
                f"\\newcommand\\FisherProbChih{{{X2:.3f}}}\n")
    else:
        fisher = (f"\\newcommand\\FisherProb{{{p_comb:.2e}}}\n"
                f"\\newcommand\\FisherProbChi{{{X2:.3f}}}\n")


        
    latex = (
        "\\documentclass[12pt]{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage{booktabs}\n"
        "\\usepackage{geometry}\n"
        "\\usepackage{graphicx}\n"
        "\\geometry{a4paper, margin=1in}\n"
        "\\title{Results of the Fisher Combined Test}\n"
        "\\author{Sara Fraija}\n"
        "\\date{\\today}\n"
        "\\begin{document}\n"
        "\\maketitle\n"
        "\\section{Resultados}\n\n" +
        table + "\n\n" + figure + "\n\n" + conclusion + "\n\\end{document}"
    )
    ""
    tex_path = os.path.join(output_dir, output_tex)
    variable_path=os.path.join(output_dir,output_tex_var)
    with open(tex_path, 'w') as f:
        f.write(latex)
    with open(variable_path,'w') as f:
        f.write(fisher)  
    print("📄 Documento LaTeX guardado en:", tex_path)

