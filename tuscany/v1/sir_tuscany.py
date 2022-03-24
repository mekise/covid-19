import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import csv

# popolazione totale
N = 3737000
# popolazione infetta iniziale
i0 = 166
# popolazione guarita iniziale
r0 = 1
# popolazione esposta iniziale
e0 = 150
# popolazione a rischio infezione
s0 = N - i0 - r0 - e0
# parametro "virulenza" = beta/gamma
R0 = 1.9
# rate di incubazione: il tempo di incubazione è 5.2 giorni, ma pare che si possa essere sensibilmente contagiosi anche se si sta incubando, quindi ho ridotto
sigma = 1./2.7
# rate di infettività 2 giorni e mezzo per l'incubazione in cui uno è contagioso, un giorno e mezzo di sintomi lievi prima dell'autoisolamento o della diagnosi
gamma = 1./4
# rate di contatto
beta = R0 * gamma

def beta2(t):
	if t < 7:
		return beta
	elif t < 14:
		return beta * np.exp(-(t-7) / 20)
	else:
		return beta * np.exp(- 14 / 20)

t = np.arange(0, 20, 0.1)
t1 = np.arange(0, 20, 1)

# modello SIR
def deriv(y, t, N, beta, sigma, gamma):
    s, e, i, r = y
    dsdt = -beta * s * i / N
    dedt = beta * s * i / N - sigma * e
    didt = sigma*e - gamma * i
    drdt = gamma * i
    return dsdt, dedt, didt, drdt

# modello SIR modificato
def deriv2(y, t, N, beta, sigma, gamma):
    s2, e2, i2, r2 = y
    dsdt = -beta2(t) * s2 * i2 / N
    dedt = beta2(t) * s2 * i2 / N - sigma * e2
    didt = sigma * e2 - gamma * i2
    drdt = gamma * i2
    return dsdt, dedt, didt, drdt

# vettore condizioni iniziali
y0 = s0, e0, i0, r0
# integrazione sistema eq differenziali
ret = odeint(deriv, y0, t, args=(N, beta, sigma, gamma))
s, e, i, r = ret.T
# integrazione sistema eq differenziali con contenimento
ret2 = odeint(deriv2, y0, t, args=(N, beta2, sigma, gamma))
s2, e2, i2, r2 = ret2.T

# apri file csv e leggi dati
dati_reali = []
with open('infetti.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)
	next(csv_reader)
	dati_reali = [int(line[1]) for line in csv_reader]

# plot
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# plot condizioni normali
ax1.set_title("Infettati - condizioni normali")
# ax1.plot(t, s/N, 'k', alpha=0.7, lw=2, label='A rischio')
ax1.plot(t, i+r, 'r', alpha=0.7, lw=2, label='Casi totali')
# ax1.plot(t, r/N, 'g', alpha=0.7, lw=2, label='Guariti')
# ax1.plot(t, (i+r)/N, 'y', alpha=0.7, lw=2, label='Inf + Gua')
ax1.scatter(t1[0:len(dati_reali)]-6, dati_reali, c='k', marker='+', label='Casi totali reali')
ax1.set_xlabel('Tempo (in giorni)')
# ax1.set_ylabel('Popolazione (x 3.737 milioni)')
ax1.yaxis.set_tick_params(length=0)
ax1.xaxis.set_tick_params(length=0)
ax1.grid(b=True, which='major', lw=0.5, ls='-')
legend1 = ax1.legend()

# plot condizioni contenimento
ax2.set_title("Infettati - condizioni di contenimento")
# ax2.plot(t, s2/N, 'k', alpha=0.7, lw=2, label='A rischio')
ax2.plot(t, i2+r2, 'r', alpha=0.7, lw=2, label='Casi totali')
# ax2.plot(t, r2/N, 'g', alpha=0.7, lw=2, label='Guariti')
# ax2.plot(t, (i2+r2)/N, 'y', alpha=0.7, lw=2, label='Inf + Gua')
ax2.scatter(t1[0:len(dati_reali)]-6, dati_reali, c='k', marker='+', label='Casi totali reali')
ax2.set_xlabel('Tempo (in giorni)')
# ax2.set_ylabel('Popolazione (x 3.737 milioni)')
ax2.yaxis.set_tick_params(length=0)
ax2.xaxis.set_tick_params(length=0)
ax2.grid(b=True, which='major', lw=0.5, ls='-')
legend2 = ax2.legend()

plt.show()

