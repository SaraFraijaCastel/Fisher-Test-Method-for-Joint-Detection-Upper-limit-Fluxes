from libraries import load_config
import importlib
import os
import subprocess

from libraries import script
from libraries import coordinate_processing
# from libraries import ul_script
# from libraries import ul_plot
# from libraries import fisher_library

def main():
    config = load_config.load_config("../config/config.yml")
    bin_size = config["bin_size"]
    PATH_GRBs_Healpix = config["PATH_GRBs_Healpix"]

    importlib.reload(script)
    script.generate_scripts_for_all_grbs(bin_size, PATH_GRBs_Healpix, config)
    script.generate_batch_sender(bin_size, config)

    # PATH_CODES = os.path.join(config['PATH_GENERAL'], 'scripts')
    # batch_script = os.path.join(PATH_CODES, f'BatchSenderMax_{bin_size}.sh')
    # subprocess.run(["bash", batch_script])

    # coordinate_processing.process_coordinates(config)

if __name__ == "__main__":
    main()