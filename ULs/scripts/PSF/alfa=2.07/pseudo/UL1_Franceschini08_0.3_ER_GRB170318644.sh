#! /usr/bin/env bash
#SBATCH --mem-per-cpu=4GB
#SBATCH -o /lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/codes/PSF_0.3/alfa=2.07//pseudo//logs/ULGRB170318644.out
#SBATCH --mail-type=all
#SBATCH --mail-user=smfraijac@astro.unam.mx
#SBATCH --time=1-24:00:00
#SBATCH -J UL
# Author: Sara Fraija
source /data/disk01/home/smfraijac/.bashrc
hawc_aerie
output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/files/PSF_0.3/alfa=2.07//pseudo/UpperLimit_1_Franceschini08_GRB170318644.csv
DR51=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN//config/pass5.f_DR/zebra-100pct-FHit.root
dir=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/corrected/
output_file=/lustre/hawcz01/scratch/userspace/jorgeamontes/GRB_KN/data/ULs/files/PSF_0.3/alfa=2.07//pseudo/UpperLimit_1_Franceschini08_GRB170318644.csv
rm -f ${output_file}
 PL="PowerLaw,1.0e-10,2.07"
ULs=$(zebra-flux-norm-fit -i $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB10C1_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB0C0_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB3C0_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB2C0_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB4C1_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB8C1_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB4C0_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB6C1_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB7C1_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB10C0_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB5C0_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB3C1_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB1C0_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB0C1_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB9C0_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB2C1_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB1C1_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB9C1_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB5C1_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB6C0_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB7C0_N1024.fits.gz $dir/GRB170318644/transit_1/GRB170318644_corrected_transit_1_binB8C0_N1024.fits.gz -b B10C1 B0C0 B3C0 B2C0 B4C1 B8C1 B4C0 B6C1 B7C1 B10C0 B5C0 B3C1 B1C0 B0C1 B9C0 B2C1 B1C1 B9C1 B5C1 B6C0 B7C0 B8C0 --extrapolate-low-z --dr $DR51 --ra 283.97 --dec 6.62 -s $PL --ebl Franceschini08,0.009 --pivot 1 --minE 4.9 --maxE 45.2 --fc 2 -V 3)
echo -e "GRB170318644 ${ULs}" >> $output_file
