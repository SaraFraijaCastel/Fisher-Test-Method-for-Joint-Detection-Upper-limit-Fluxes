source /data/disk01/home/smfraijac/.bashrc
hawc_aerie
FILE_1=/lustre/hawcz01/scratch/userspace/mfercg/J1837-0650/test_crab/single_point/fitResults/sys-fHit_zoneL3-9_step1_pointSource_powerlaw/map/residual.fits
FILE_2=/lustre/hawcz01/scratch/userspace/mfercg/J1837-0650/test_crab/single_point/fitResults/sys-fHit_zoneL3-9_step1_pointSource_powerlaw/map/model.fits
RA=83.6
DEC=22.015
err=30
makeSignificanceHistogram.py $FILE_1 -o residual.png --includeArea --binsize $err --ra $RA --dec $DEC  
makeSignificanceHistogram.py $FILE_2 -o model.png --includeArea --binsize $err --ra $RA --dec $DEC  