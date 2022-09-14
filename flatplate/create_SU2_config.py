import os
from testcases import testcases, levels




for name, case in testcases.items():
    for finish in case['finishes']:
        cfg_file_raw = os.path.join(case['base_path'], f'flatplate_{name}_{finish}.cfg')
        cfg_file_final = os.path.join(case['base_path'], 'flatplate_{name}_{finish}_{level}.cfg')

        if not os.path.exists(cfg_file_raw):
            continue

        # create SU2 Folder if it does not exist
        su2_folder = os.path.join(case['base_path'], 'SU2')
        if not os.path.exists(su2_folder):
            os.mkdir(su2_folder)

        for level in levels:
            # read raw file
            f = open(cfg_file_raw, 'r')
            cfg_raw = f.read()
            f.close()

            # replace all "GRIDLEVEL" with the current level
            cfg_final = cfg_raw.replace('GRIDLEVEL', level)

            # save the new file
            f = open(cfg_file_final.format(finish=finish, name=name, level=level), 'w')
            f.write(cfg_final)
            f.close
