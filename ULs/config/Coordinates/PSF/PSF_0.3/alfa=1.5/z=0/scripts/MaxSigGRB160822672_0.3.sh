#!/usr/bin/env bash
#SBATCH --mem-per-cpu=4GB
#SBATCH -o /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/healpixz=0_alfa1.5/GRB160822672/GRB160822672/maps/codes/HIST.out
#SBATCH --mail-type=all
#SBATCH --mail-user=smfraijac@astro.unam.mx
#SBATCH -J ULGRB160822672
# Author: Sara_Fraija

source /data/disk01/home/smfraijac/.bashrc
hawc_aerie

command -v plotMercator.py >/dev/null 2>&1 || { echo >&2 "plotMercator.py no encontrado"; exit 1; }

RA=272.1291666666666
DEC=3.583888888888889
Bin_size=0.54
Hist_path=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF/PSF_0.3/alfa=1.5/z=0/SIG_ALL_GRBs
Window_size=0.6
for Label in 1FINAL 2FINAL; do
    GRB=GRB160822672_$Label
    label2=${Label%%_*}
    output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF/PSF_0.3/alfa=1.5/z=0/SIG_ALL_GRBs/GRB160822672_PSF_0.54_Hist$Label.txt
    max_output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF/PSF_0.3/alfa=1.5/z=0/MaxSigHist_0.54_${label2}.txt
    rm -f "$output_file"

    transit_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/healpixz=0_alfa1.5/GRB160822672/transit_${label2}/GRB160822672_transit_$Label.fits.gz

    PL=$(plotMercator.py "$transit_file" --magma --cross --circle $RA $DEC $Bin_size --circleproperty white 2 1 --origin $RA $DEC $Window_size $Window_size -o "/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF/PSF_0.3/alfa=1.5/z=0/SIG_ALL_GRBs/GRB160822672.png")
    echo -e "$PL" > "$output_file"

    Maxi=$(grep "Max" "$output_file")
    if [[ -z "$Maxi" ]]; then
        echo "GRB160822672,$Label,Max not found or file corrupt" >> "$max_output_file"
        echo "[WARNING] Max not found for GRB160822672 label $Label. Possible file corruption." >&2
    else
        echo -e "GRB160822672,$Label,$Maxi" >> "$max_output_file"
    fi

done
