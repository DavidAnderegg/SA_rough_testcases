import numpy as np

bc_file = 'bcfile'
n_blocks = 30 

pre_wall = """1 iLow bcsymmetryplane sym1
1 iHigh bcsymmetryplane sym2
1 kLow bcsymmetryplane sym
1 kHigh bcfarfield far
1 jLow bcinflow in\n"""

wall = """{n} iLow bcsymmetryplane sym
{n} iHigh bcsymmetryplane sym2
{n} kLow bcwall wall{m} BCDataSet_1 BCWall Dirichlet SandGrainRoughness {ks}
{n} kHigh bcfarfield far\n"""

last = '{n} jHigh bcoutflowsubsonic out BCDataSet_1 BCOutFlowSubsonic Dirichlet Pressure 101300\n'


with open(bc_file, 'w') as f:
    f.write(pre_wall)

    ks = np.zeros(29)
    for n in range(2, n_blocks):
        f.write(wall.format(n=n, m=n-1, ks=ks[n-1]))

    f.write(last.format(n=n))
f.close()
