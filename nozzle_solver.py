import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

# Constants (air)
gamma = 1.4
R = 287  # J/kg·K

def isentropic_mach(A_ratio, gamma=1.4):
    """Solve for exit Mach number given area ratio"""
    def eq(M):
        return (1/M) * ((2 + (gamma-1)*M**2)/(gamma+1))**((gamma+1)/(2*(gamma-1))) - A_ratio
    M_guess = 2.0 if A_ratio > 1 else 0.5
    M = fsolve(eq, M_guess)[0]
    return M

def nozzle_flow(p0, T0, p_exit, A_ratio):
    M_exit = isentropic_mach(A_ratio)
    T_exit = T0 / (1 + 0.5*(gamma-1)*M_exit**2)
    a_exit = np.sqrt(gamma * R * T_exit)
    v_exit = M_exit * a_exit
    return M_exit, v_exit, T_exit

# === DEMO ===
p0, T0, p_exit = 1e6, 300, 1e5  # Pa, K, Pa
A_ratio = 5.0
M, v, T = nozzle_flow(p0, T0, p_exit, A_ratio)

print(f"Exit Mach: {M:.2f}")
print(f"Exit Velocity: {v:.0f} m/s")
print(f"Exit Temp: {T:.1f} K")

# Plot (save to repo)
x = np.linspace(0.3, 1.0, 100)
A = 1 + 4.7*(x - 0.3)**2  # Dummy bell shape
plt.plot(x, A, label="Nozzle Area")
plt.axhline(A_ratio, color='r', linestyle='--', label=f"A_exit/A_throat = {A_ratio}")
plt.xlabel("Axial Position")
plt.ylabel("Area Ratio")
plt.legend()
plt.title("Supersonic Nozzle Geometry")
plt.savefig("nozzle_demo.png")