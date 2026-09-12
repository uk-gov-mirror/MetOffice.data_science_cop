#!/bin/bash -l
#SBATCH --job-name=era5_download
#SBATCH --mem=16G
#SBATCH --time=350:00
#SBATCH --cpus-per-task=5
#SBATCH --output=era5_download_%j.out
#SBATCH --error=era5_download_%j.err

# Load the conda environment
conda activate dscop_cds

export DOWNLOAD_DIR=$SCRATCH/era5_nowcast/

echo year $YEAR
echo month $MONTH

# Run the ERA5 download script
# Default example: download 2010 data for selected variables and pressure levels
python era5_download.py \
    --data-dir $DOWNLOAD_DIR \
    --year ${YEAR} \
    --month ${MONTH} \
    --variables geopotential specific_humidity temperature u_component_of_wind v_component_of_wind \
    --pressure-levels 500 850 1000

