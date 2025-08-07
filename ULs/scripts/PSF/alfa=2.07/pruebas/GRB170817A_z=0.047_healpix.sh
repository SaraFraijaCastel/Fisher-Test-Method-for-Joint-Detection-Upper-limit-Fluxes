#! /usr/bin/env bash
#SBATCH --mem-per-cpu=4GB
#SBATCH -o /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/codes/PSF_0.3/alfa=2.07/pruebas/logs/ULGRB170817529_healpix.out
#SBATCH --mail-type=all
#SBATCH --mail-user=smfraijac@astro.unam.mx
#SBATCH --time=1-24:00:00
#SBATCH -J UL
# Author: Sara Fraija
source /data/disk01/home/jorgeamontes/.bashrc
hawc_aerie
EBL='Gilmore12Fiducial,0.047'
output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/files/PSF_0.3/alfa=2.07//pruebas/UpperLimit_1_Franceschini08_GRB170817529.csv
DR51=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN//config/pass5.f_DR/zebra-100pct-FHit.root
dir=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/corrected/
# output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/files/PSF_0.3/alfa=2.07//pseudo/UpperLimit_1_Franceschini08_GRB170817529.csv
# rm -f ${output_file}
E_min=7.6
E_max=20
PL='PowerLaw,1.0e-10,2.07'
z=0.047

# ULs=$(zebra-flux-norm-fit -i $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB6C0_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB9C1_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB9C0_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB1C1_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB5C1_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB0C1_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB6C1_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB2C1_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB8C0_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB5C0_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB7C0_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB4C1_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB7C1_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB1C0_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB2C0_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB3C0_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB10C0_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB8C1_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB3C1_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB4C0_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB0C0_N1024.fits.gz $dir/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB10C1_N1024.fits.gz -b B6C0 B9C1 B9C0 B1C1 B5C1 B0C1 B6C1 B2C1 B8C0 B5C0 B7C0 B4C1 B7C1 B1C0 B2C0 B3C0 B10C0 B8C1 B3C1 B4C0 B0C0 B10C1 --extrapolate-low-z --dr $DR51 --ra 197.67 --dec -23.36 -s $PL --ebl $EBL --pivot 1 --minE ${E_min} --maxE ${E_max} --fc 2 -V 3)
# echo -e "GRB170817529 ${ULs}" >> $output_file

# INPUT=(/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/corrected/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB{0..10}C{0..1}_N1024.fits.gz)
Output=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/codes/PSF_0.3/alfa=2.07/pruebas/GRB170817529_transit_1FINAL.fits.gz
output_image=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/codes/PSF_0.3/alfa=2.07/pruebas/GRB170817529_transit_1FINAL.png
zebra-HealpixSigFluxMap --input /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/corrected/GRB170817529/transit_1/GRB170817529_corrected_transit_1_binB{0..10}C{0..1}_N1024.fits.gz \
-b B{0..10}C{0..1} --dr /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/config/pass5.f_DR/zebra-100pct-FHit.root -s PowerLaw,1e-8,2.07 --pivot 1 --minE $E_min --maxE $E_max \
--ebl $EBL --window 197.45 336.61861111111114 3.5 3.5 --nthreads 10 --nside 1024 -o $Output

plotMercator.py $Output --magma --cross --circle 197.45 -23.38138888888889 0.3 \
--circleproperty white 2 1 --origin 197.45 -23.38138888888889 2 2 -m 0 -M 3 -o $output_image \
--fermicat /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/config/gll_psc_v27.fit --fermicat-labels --title "GRB170817529 transit 1" \
--cat-labels-angle 0 --tevcat /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/../GRB_GW/config/sources/tevcat_data_2023-01-19.txt --tevcat-labels

# zebra-flux-norm-fit -i ${INPUT[@]}  -b B{0..10}C{0..1} --dr /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/config/pass5.f_DR/zebra-100pct-FHit.root --ra 197.45 --dec 336.61861111111114 -s PowerLaw,1e-8,2.07 --ebl Gilmore12Fiducial,0.0093 --pivot 1 --minE  7.6 --maxE 49.3 --fc 2





