#!/usr/bin/env bash
#SBATCH --mem-per-cpu=4GB
#SBATCH -o /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/healpix_maps_2.07_ER/GRB170803729/GRB170803729/maps/codes/HIST.out
#SBATCH --mail-type=all
#SBATCH --mail-user=smfraijac@astro.unam.mx
#SBATCH -J ULGRB170803729
# Author: Sara_Fraija

source /data/disk01/home/smfraijac/.bashrc
hawc_aerie

command -v plotMercator.py >/dev/null 2>&1 || { echo >&2 "plotMercator.py no encontrado"; exit 1; }

RA=174.935
DEC=-16.311944444444446
Bin_size=0.3
Hist_path=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.3/alfa=2.07/SIG_ALL_GRBs
Window_size=0.6
for Label in 1 2; do
    GRB=GRB170803729_$Label
    label2=${Label%%_*}
    output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.3/alfa=2.07/SIG_ALL_GRBs/GRB170803729_PSF_0.3_Hist$Label.txt
    max_output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.3/alfa=2.07//MaxSigHist_0.3_${label2}.txt
    rm -f "$output_file"

    transit_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/healpix_maps_2.07_ER/GRB170803729/transit_${label2}/GRB170803729_transit_$Label.fits.gz

    PL=$(plotMercator.py "$transit_file" --magma --cross --circle $RA $DEC $Bin_size --circleproperty white 2 1 --origin $RA $DEC $Window_size $Window_size -o "/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.3/alfa=2.07/SIG_ALL_GRBs/GRB170803729.png")
    echo -e "$PL" > "$output_file"

    Maxi=$(grep "Max" "$output_file")
    if [[ -z "$Maxi" ]]; then
        echo "GRB170803729,$Label,Max not found or file corrupt" >> "$max_output_file"
        echo "[WARNING] Max not found for GRB170803729 label $Label. Possible file corruption." >&2
    else
        echo -e "GRB170803729,$Label,$Maxi" >> "$max_output_file"
    fi

done
