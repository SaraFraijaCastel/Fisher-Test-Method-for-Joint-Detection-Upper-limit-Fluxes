#!/usr/bin/env bash
#SBATCH --mem-per-cpu=4GB
#SBATCH -o /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/healpix_maps_2.07_ER/GRB171007498/GRB171007498/maps/codes/HIST.out
#SBATCH --mail-type=all
#SBATCH --mail-user=smfraijac@astro.unam.mx
#SBATCH -J ULGRB171007498
# Author: Sara_Fraija

source /data/disk01/home/smfraijac/.bashrc
hawc_aerie

command -v plotMercator.py >/dev/null 2>&1 || { echo >&2 "plotMercator.py no encontrado"; exit 1; }

RA=135.54416666666663
DEC=42.848888888888894
Bin_size=0.15
Hist_path=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.15/alfa=2.07/SIG_ALL_GRBs
Window_size=0.3

for Label in 1 2; do
    GRB=GRB171007498_$Label
    output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.15/alfa=2.07/SIG_ALL_GRBs/GRB171007498_PSF_0.15_Hist$Label.txt
    max_output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.15/alfa=2.07//MaxSigHist_0.15_$Label.txt
    rm -f "$output_file"

    transit_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/healpix_maps_2.07_ER/GRB171007498/transit_$Label/GRB171007498_transit_$Label.fits.gz

    PL=$(plotMercator.py "$transit_file" --magma --cross --circle $RA $DEC $Bin_size --circleproperty white 2 1 --origin $RA $DEC $Window_size $Window_size -o "/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.15/alfa=2.07/SIG_ALL_GRBs/GRB171007498.png")
    echo -e "$PL" > "$output_file"

    Maxi=$(grep "Max" "$output_file")
    if [[ -z "$Maxi" ]]; then
        echo "GRB171007498,$Label,Max not found or file corrupt" >> "$max_output_file"
        echo "[WARNING] Max not found for GRB171007498 label $Label. Possible file corruption." >&2
    else
        echo -e "GRB171007498,$Label,$Maxi" >> "$max_output_file"
    fi

done
