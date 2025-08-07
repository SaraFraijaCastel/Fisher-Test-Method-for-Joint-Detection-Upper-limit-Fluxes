#!/usr/bin/env bash
#SBATCH --mem-per-cpu=4GB
#SBATCH -o /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/healpix_maps_2.07_ER/GRB180715755/GRB180715755/maps/codes/HIST.out
#SBATCH --mail-type=all
#SBATCH --mail-user=smfraijac@astro.unam.mx
#SBATCH -J ULGRB180715755
# Author: Sara_Fraija

source /data/disk01/home/smfraijac/.bashrc
hawc_aerie

command -v plotMercator.py >/dev/null 2>&1 || { echo >&2 "plotMercator.py no encontrado"; exit 1; }

RA=235.0691666666666
DEC=-0.925
Bin_size=0.15
Hist_path=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.15/alfa=2.07/SIG_ALL_GRBs
Window_size=0.3

for Label in 1 2; do
    GRB=GRB180715755_$Label
    output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.15/alfa=2.07/SIG_ALL_GRBs/GRB180715755_PSF_0.15_Hist$Label.txt
    max_output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.15/alfa=2.07//MaxSigHist_0.15_$Label.txt
    rm -f "$output_file"

    transit_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/healpix_maps_2.07_ER/GRB180715755/transit_$Label/GRB180715755_transit_$Label.fits.gz

    PL=$(plotMercator.py "$transit_file" --magma --cross --circle $RA $DEC $Bin_size --circleproperty white 2 1 --origin $RA $DEC $Window_size $Window_size -o "/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/config/Coordinates/PSF_0.15/alfa=2.07/SIG_ALL_GRBs/GRB180715755.png")
    echo -e "$PL" > "$output_file"

    Maxi=$(grep "Max" "$output_file")
    if [[ -z "$Maxi" ]]; then
        echo "GRB180715755,$Label,Max not found or file corrupt" >> "$max_output_file"
        echo "[WARNING] Max not found for GRB180715755 label $Label. Possible file corruption." >&2
    else
        echo -e "GRB180715755,$Label,$Maxi" >> "$max_output_file"
    fi

done
