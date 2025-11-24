import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# v0.2 – Realistic 2D Axisymmetric Rao Bell Nozzle (A_exit/A_throat = 5.0)
R_t = 0.1                                 # Throat radius [m]
A_ratio = 5.0
R_e = R_t * np.sqrt(A_ratio)              # ≈0.2236 m

# NASA-standard Rao bell contour (normalised points)
x_norm = np.array([-1.5, -1.0, -0.5, 0.0, 0.4, 0.8, 1.2, 1.6])
r_norm = np.array([2.0, 1.55, 1.15, 1.0, 1.0, 1.3, 1.8, 2.236])  # sqrt(5)≈2.236

x = x_norm * R_t
r = r_norm * R_t

# Smooth cubic spline
cs = CubicSpline(x, r, bc_type='natural')
x_fine = np.linspace(x[0], x[-1], 800)
r_fine = cs(x_fine)

# Plot
plt.figure(figsize=(11,6))
plt.plot(x_fine, r_fine, 'navy', lw=3, label='Nozzle wall')
plt.plot(x_fine, -r_fine, 'navy', lw=3)
plt.axhline(0, color='gray', lw=1)
plt.title('v0.2 – 2D Axisymmetric Supersonic Nozzle (A_exit/A_throat = 5.0)', fontsize=14)
plt.xlabel('Axial Position (m)')
plt.ylabel('Radius (m)')
plt.grid(alpha=0.3)
plt.axis('equal')
plt.legend()
plt.tight_layout()
plt.savefig('nozzle_2d_bell.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"v0.2 COMPLETE – Throat radius = {R_t:.3f} m | Exit radius = {R_e:.4f} m")