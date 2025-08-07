#!/usr/bin/env bash
#SBATCH --mem-per-cpu=4GB
#SBATCH -o /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/healpixz=0_alfa1.5/GRB160612842/GRB160612842/maps/codes/HIST.out
#SBATCH --mail-type=all
#SBATCH --mail-user=smfraijac@astro.unam.mx
#SBATCH -J ULGRB160612842
# Author: Sara_Fraija

source /data/disk01/home/smfraijac/.bashrc
hawc_aerie

command -v plotMercator.py >/dev/null 2>&1 || { echo >&2 "plotMercator.py no encontrado"; exit 1; }

RA=348.36416666666656
DEC=-25.375
Bin_size=0.3
Hist_path=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF/PSF_0.3/alfa=1.5/z=0/SIG_ALL_GRBs
Window_size=0.6
for Label in 1FINAL 2FINAL; do
    GRB=GRB160612842_$Label
    label2=${Label%%_*}
    output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF/PSF_0.3/alfa=1.5/z=0/SIG_ALL_GRBs/GRB160612842_PSF_0.3_Hist$Label.txt
    max_output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF/PSF_0.3/alfa=1.5/z=0/MaxSigHist_0.3_${label2}.txt
    rm -f "$output_file"

    transit_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/healpixz=0_alfa1.5/GRB160612842/transit_${label2}/GRB160612842_transit_$Label.fits.gz

    PL=$(plotMercator.py "$transit_file" --magma --cross --circle $RA $DEC $Bin_size --circleproperty white 2 1 --origin $RA $DEC $Window_size $Window_size -o "/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF/PSF_0.3/alfa=1.5/z=0/SIG_ALL_GRBs/GRB160612842.png")
    echo -e "$PL" > "$output_file"

    Maxi=$(grep "Max" "$output_file")
    if [[ -z "$Maxi" ]]; then
        echo "GRB160612842,$Label,Max not found or file corrupt" >> "$max_output_file"
        echo "[WARNING] Max not found for GRB160612842 label $Label. Possible file corruption." >&2
    else
        echo -e "GRB160612842,$Label,$Maxi" >> "$max_output_file"
    fi

done
