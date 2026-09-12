"""
ERA5 Data Download Script

This module downloads ERA5 reanalysis data from the Copernicus Climate Data Store (CDS)
for specified variables and pressure levels.
"""

import argparse
import cdsapi
import pathlib


# Constants
DATASET = "reanalysis-era5-pressure-levels"


# Default days and times for all months
DAYS = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09",
    "10", "11", "12", "13", "14", "15", "16", "17", "18",
    "19", "20", "21", "22", "23", "24", "25", "26", "27",
    "28", "29", "30", "31"
]

TIMES = [
    "00:00", "01:00", "02:00", "03:00", "04:00", "05:00",
    "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
    "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
    "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
]

UK_BOUNDS = [48, -5, 60, 5]
DATA_BOUNDS = UK_BOUNDS


def get_cmd_args():
    """
    Parse command line arguments for ERA5 download script.

    Returns:
        argparse.Namespace: Parsed arguments containing:
            - year: The year to download data for
            - variables: List of variable names to download
            - pressure_levels: List of pressure levels to download
    """
    parser = argparse.ArgumentParser(
        description="Download ERA5 reanalysis data from Copernicus CDS"
    )
    parser.add_argument(
        "--data-dir",
        dest="data_dir",
        type=pathlib.Path,
        required=True,
        help="Directory to save downloaded data (e.g., /path/to/data/)",
    )

    parser.add_argument(
        "--year",
        type=int,
        required=True,
        help="Year to download data for (e.g., 2010)"
    )
    parser.add_argument('--month',
                        type=int,
                        required=True,
                        help="Month to download data for (e.g., 2 for February)",
                        )

    parser.add_argument(
        "--variables",
        nargs="+",
        required=True,
        help="List of variables to download (e.g., geopotential temperature u_component_of_wind)"
    )

    parser.add_argument(
        "--pressure-levels",
        nargs="+",
        required=True,
        help="List of pressure levels to download (e.g., 200 500 750 800 1000)"
    )

    return parser.parse_args()


def main():
    """
    Main function to download ERA5 data.

    Downloads ERA5 reanalysis data from the Copernicus Climate Data Store for the
    specified year, variables, and pressure levels. Data is downloaded on a monthly
    basis (February through December by default) and saved as NetCDF files.
    """
    args = get_cmd_args()

    # Create CDS client
    client = cdsapi.Client()

    # Ensure output directory exists
    download_dir = args.data_dir
    download_dir.mkdir(parents=True, exist_ok=True)

    # Build base request dictionary
    request = {
        "product_type": ["reanalysis"],
        "year": [f'{args.year:04d}'],
        "month": [f'{args.month:02d}'],
        "day": DAYS,
        "time": TIMES,
        "pressure_level": args.pressure_levels,
        "data_format": "netcdf",
        "download_format": "unarchived",

        "area": DATA_BOUNDS,
    }

    # Download data for each variable and month
    for var_name in args.variables:
        print(
            f'Processing data for {var_name}, '
            f'time {args.year:04d}-{args.month:02d}'
        )
        fname = f'era5_{var_name}_{args.year:04d}{args.month:02d}.nc'
        request['variable'] = [var_name]

        client.retrieve(
            DATASET,
            request,
            str(download_dir / fname),
        )


if __name__ == '__main__':
    main()
