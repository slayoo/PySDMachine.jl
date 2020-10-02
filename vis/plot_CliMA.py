import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl
from netCDF4 import Dataset
from copy import copy

# TODO:
# - don't hardcode file names
# - plot dry density, not the total

clima_output = "../ClimateMachine.jl/output/"

# TODO - find those file automatically
aux_f = clima_output + "KinematicModel_DumpAux-2020-10-01T15.11.44.564.nc"
state_f = clima_output + "KinematicModel_DumpState-2020-10-01T15.11.44.564.nc"

aux_data = Dataset(aux_f, 'r')
state_data = Dataset(state_f, 'r')

# read the data
y_idx = 5
z = state_data["z"][:]
x = state_data["x"][:]
time = aux_data["time"][:]
rho = np.array(state_data["ρ"][:])[:, :,  y_idx, :]

vars = ["p", "u", "w", \
        "q_tot", "q_vap", "q_liq", "q_ice",\
        "e_tot", "e_kin", "e_pot", "e_int", "T", "S", "RH"]
data_dict = {}
for var in vars:
    data_dict[var] = np.array(aux_data.variables[var][:])[:, :,  y_idx, :]

t_idx = 0 #[0, 1, ..., 6]

# plot velocity field
fig, axs = plt.subplots(1,2, figsize=(9, 4))
im1 = axs[0].contourf(x, z, data_dict["u"][t_idx, :, :])
im2 = axs[1].contourf(x, z, data_dict["w"][t_idx, :, :])
axs[0].set_title("u [m/s]")
axs[1].set_title("w [m/s]")
fig.colorbar(im1, ax=axs[0])
fig.colorbar(im2, ax=axs[1])
plt.tight_layout()
plt.show()

# plot water
cmap2 = copy(mpl.cm.get_cmap("viridis"))
fig, axs = plt.subplots(1,2, figsize=(9, 4))
im1 = axs[0].contourf(x, z, data_dict["q_vap"][t_idx, :, :] * 1e3)
im2 = axs[1].contourf(x, z, data_dict["q_liq"][t_idx, :, :] * 1e3, vmin=0.0, cmap=cmap2)
im2.cmap.set_under('red')
axs[0].set_title("q_vap [g/kg]")
axs[1].set_title("q_liq [g.kg]")
fig.colorbar(im1, ax=axs[0])
fig.colorbar(im2, ax=axs[1])
plt.tight_layout()
plt.show()

def dry_density(rho, q_tot, q_vap, q_liq):
    #TODO
    return rho

#plot initial profiles of T, p, RH, rho (TODO - should be dry density)
fig, axs = plt.subplots(2,2, figsize=(8, 8))
im1 = axs[0, 0].plot(np.average(data_dict["T"][t_idx, :, :], axis=1), z)
im2 = axs[0, 1].plot(np.average(data_dict["p"][t_idx, :, :], axis=1), z)
im3 = axs[1, 0].plot(np.average(data_dict["RH"][t_idx, :, :], axis=1), z)
im4 = axs[1, 1].plot(np.average(rho[t_idx, :, :], axis=1), z)
axs[0, 0].set_title("T [K]")
axs[0, 1].set_title("p [hPa]")
axs[1, 0].set_title("RH [-]")
axs[1, 1].set_title("rho [kg/m3]")
for xx in range(2):
    for yy in range(2):
        axs[xx,yy].set_ylim((0, 1500))
plt.tight_layout()
plt.show()
