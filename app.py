import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.interpolate import CubicSpline

st.set_page_config(page_title="Supersonic Nozzle CFD", layout="centered")
st.title("Supersonic Nozzle Solver v0.3")
st.markdown("Open-source CFD solver for rocket nozzle design, built by Loughborough University Aeronautical Engineering MEng Student. X:@LaytonLNicol")

# Sidebar inputs
st.sidebar.header("Nozzle Design Parameters")
p0 = st.sidebar.slider("Stagnation Pressure p₀ (MPa)", 0.5, 10.0, 1.0, 0.1) * 1e6
T0 = st.sidebar.slider("Stagnation Temperature T₀ (K)", 200, 1000, 300, 10)
pe = st.sidebar.slider("Exit Pressure p_e (kPa)", 10, 500, 100, 10) * 1e3
A_ratio = st.sidebar.slider("Area Ratio A_exit/A_throat", 1.5, 10.0, 5.0, 0.1)

gamma = 1.4
R = 287.0

# Solve exit Mach number (supersonic branch)
def area_mach(M, ratio):
    return (1/M) * ((2 + (gamma-1)*M**2)/(gamma+1))**((gamma+1)/(2*(gamma-1))) - ratio

M_exit = fsolve(area_mach, 2.5, args=(A_ratio,))[0]

# Calculate exit properties
T_exit = T0 / (1 + 0.5*(gamma-1)*M_exit**2)
a_exit = np.sqrt(gamma * R * T_exit)
V_exit = M_exit * a_exit

# Results
col1, col2, col3 = st.columns(3)
col1.metric("Exit Mach Number", f"{M_exit:.3f}")
col2.metric("Exit Velocity", f"{V_exit:.0f} m/s")
col3.metric("Exit Temperature", f"{T_exit:.1f} K")

# 2D Rao bell nozzle geometry
R_t = 0.1
R_e = R_t * np.sqrt(A_ratio)
x_norm = np.array([-1.5, -1.0, -0.5, 0.0, 0.4, 0.8, 1.2, 1.6])
r_norm = np.array([2.0, 1.55, 1.15, 1.0, 1.0, 1.3, 1.8, np.sqrt(A_ratio)])

x = x_norm * R_t
r = r_norm * R_t

cs = CubicSpline(x, r, bc_type='natural')
x_fine = np.linspace(x[0], x[-1], 800)
r_fine = cs(x_fine)

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(x_fine, r_fine, 'navy', lw=3, label='Nozzle wall')
ax.plot(x_fine, -r_fine, 'navy', lw=3)
ax.axhline(0, color='gray', lw=1)
ax.set_title(f"2D Axisymmetric Rao Bell Nozzle – A_ratio = {A_ratio:.2f}")
ax.set_xlabel("Axial Position (m)")
ax.set_ylabel("Radius (m)")
ax.grid(alpha=0.3)
ax.axis('equal')
ax.legend()
st.pyplot(fig)

st.success("v0.3 LIVE – Interactive Supersonic Nozzle Calculator")
st.caption("GitHub: https://github.com/LaytonLNicol/Supersonic-Nozzle-CFD")

p_exit_isentropic = p0 * (T_exit / T0)**(gamma / (gamma-1))
st.metric("Isentropic Exit Pressure", f"{p_exit_isentropic / 1e3:.1f} kPa")
mismatch = abs(pe - p_exit_isentropic) / p_exit_isentropic * 100
st.caption(f"Back pressure mismatch: {mismatch:.1f}% → {'Perfectly expanded' if mismatch < 5 else 'Shocks expected in real flow'}")