I. GENERAL INFORMATION

1. Title
Dataset of "Degeneracy and Scaling Properties of Self-Dual Fracton Spin Models"

2. Author Information
  
Giovanni Canossa [1,2], Lode Pollet [1,2,3], Miguel A. Martin-Delgado [4], Hao Song [5], and Ke Liu [1,2]
1. Arnold Sommerfeld Center for Theoretical Physics,  University of Munich
2. Munich Center for Quantum Science and Technology (MCQST)
3. Wilczek Quantum Center, School of Physics and Astronomy, Shanghai Jiao Tong University
4. Departamento de Física Teórica, Universidad Complutense, 28040 Madrid, Spain
5. CAS Key Laboratory of Theoretical Physics, Institute of Theoretical Physics, Chinese Academy of Sciences, China

Links to publications that cite or use the data:
TBA

II. Files

1. Convention

Datas from the multicanonical MC simulations are stored in "Tetra-Ising" and "Fractal-Ising" folders.

Lattice size: Each subfolder is named "L=value" where value denotes the linear system size.

Multicanonical weights: Files "g_init_T=value.data" contains the set of log(weights) at a given temperature and lattice size, derived from the iterative weight-learning procedure.

Datas: HDF5 files "name.out.h5" contain the results of the multicanonical MC simulation at a given lattice size.


III. Data in HDF5 file

1. Convention

The results obtained at each temperature point is stored in a separate subdirectory of the .out.h5 file. Each of these subdirectories contains:

Energy_Hist: normalized energy histograms obtained from the multicanonical MC simulation (unweighted)

Energy_Hist_rw: normalized reweighted energy histograms. For each bin, Energy_Hist_rw[i] = Energy_Hist[i] * e**g[i] / norm, where norm = sum( Energy_Hist[i] * e**g[i] ).

c: 1/norm. Gives an estimate of the ratio Z_muca/Z_ca.

g: vector containing the weights used for the multicanonical MC simulation at that specific temperature. These are derived from reweighting the weights in "g_init_T=value.data" file.

Energy, Energy_Susc, Energy_Kurt Q_x, Q_x_Susc, Q_x_Kurt: canonical expectation value of each relevant observables, along with their susceptibilities and Kurtosis, obtained by reweighting each measurement taken during the simulation by the appropriate weight. (NB: Energy and Q_x need to be multiplied by C in order to give the correct canonical expectation value.)


2. Relevance

These data reproduce Figs. 4 & 5 in the manuscript.


III. Finite size scaling

1. Convention

All estimated transition temperatures with their respective uncertainties are stored in "fitting_Tetra" and "fitting_Fractal" folders in the fittemps.txt file.

2. Relevance

These data reproduce Figs. 2 & 3 in the manuscript.
 
