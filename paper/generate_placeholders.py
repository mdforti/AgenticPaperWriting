import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
outdir = '/home/mariano/PaperWritingLab/paper/figures'

# Figure 1: Dataset composition-phase distribution
fig, ax = plt.subplots(figsize=(8, 5))
phases = ['A15', 'C15', 'C14', 'C36', 'sigma', 'chi', 'mu']
for i, phase in enumerate(phases):
    x = np.random.uniform(0.2, 0.8, 30 + i*5)
    y = np.random.uniform(-0.1, 0.1, len(x))
    ax.scatter(x, y, alpha=0.6, label=phase)
ax.set_xlabel('Mo fraction')
ax.set_ylabel(r'$E_f^{nmhcp}$ (eV/atom)')
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(f'{outdir}/fig01_dataset.pdf')
plt.close(fig)

# Figure 3: Validation parity plots
fig, axes = plt.subplots(3, 4, figsize=(16, 10))
descriptors = ['BOP', 'ACE', 'SOAP']
phases = ['R', 'M', 'P', r'$\delta$']
for i, desc in enumerate(descriptors):
    for j, phase in enumerate(phases):
        ax = axes[i, j]
        ytrue = np.random.uniform(-0.1, 0.1, 15)
        ypred = ytrue + np.random.normal(0, 0.003 * (j + i + 1), 15)
        ax.scatter(ytrue, ypred, s=30)
        lims = [min(ytrue.min(), ypred.min()), max(ytrue.max(), ypred.max())]
        ax.plot(lims, lims, '--k', lw=1)
        ax.set_title(f'{desc} - {phase}')
        if j == 0:
            ax.set_ylabel('ML (eV/atom)')
        if i == 2:
            ax.set_xlabel('DFT (eV/atom)')
fig.tight_layout()
fig.savefig(f'{outdir}/fig03_validation.pdf')
plt.close(fig)

# Figure 4: Thermodynamic Gibbs free energy
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0.2, 0.8, 50)
phases_thermo = [('R', 'solid'), ('P', 'dashed'), ('M', 'dotted'), (r'$\sigma$', 'dashdot')]
for phase, ls in phases_thermo:
    y = -0.01 * (x - 0.5)**2 + np.random.normal(0, 0.001, len(x))
    ax.plot(x, y, label=phase, linestyle=ls)
ax.set_xlabel('Mo fraction')
ax.set_ylabel('Gibbs free energy (eV/atom)')
ax.legend()
ax.set_title('1700 K')
fig.tight_layout()
fig.savefig(f'{outdir}/fig04_thermo.pdf')
plt.close(fig)

# Figure 5: R-phase occupancy
fig, ax = plt.subplots(figsize=(8, 5))
wyckoff = ['6c1', '6c2', '18f', '18h1', '18h2', '18h3']
x_pos = np.arange(len(wyckoff))
ml_occ = np.array([0.3, 0.7, 0.5, 0.4, 0.6, 0.8])
xrd_occ = ml_occ + np.random.normal(0, 0.05, len(wyckoff))
ax.bar(x_pos - 0.2, ml_occ, 0.3, label='ML', alpha=0.8)
ax.bar(x_pos + 0.2, xrd_occ, 0.3, label='XRD', alpha=0.8)
ax.set_xticks(x_pos)
ax.set_xticklabels(wyckoff)
ax.set_ylabel('Mo site fraction')
ax.legend()
fig.tight_layout()
fig.savefig(f'{outdir}/fig05_occupancy.pdf')
plt.close(fig)

print('All placeholder figures created.')
