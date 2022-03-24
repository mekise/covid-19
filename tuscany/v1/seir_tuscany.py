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
# popolazione esposta iniziale (eh... questa l'ho messa un po' a caso)
e0 = 250
# popolazione a rischio infezione
s0 = N - i0 - r0 - e0
# parametro "virulenza" = beta/gamma
R0 = 2.6
# rate di incubazione: il tempo di incubazione è 5.2 giorni, ma pare che si possa essere sensibilmente contagiosi anche se si sta incubando
sigma = 1./5.2
# rate di infettività, preso da https://cmmid.github.io/topics/covid19/current-patterns-transmission/wuhan-early-dynamics.html, sta a indicare che in media passano 2.9 giorni prima che chi è contagioso si autoisoli.
gamma = 1./2.9
# rate di contatto
beta = R0 * gamma

def beta2(t):
	if t < 2:
		return 2.6 * gamma
	elif t < 16:
		return 1.9 * gamma    # il tempo per cui R0 diventa 1.9 e il valore di 1.9 sono presi da questo studio https://www.nature.com/articles/s41421-020-0148-0.pdf
	else:
		return 0.65 * gamma   # questo è temo imprevedibile, nello studio di nature sono stati fatti esempi con 0.9 e 0.5. La risposta cinese è poi stata migliore, ma dubito che si riesca a ripetere in Italia.

t = np.arange(0, 100, 0.1)
t1 = np.arange(0, 100, 1)

# modello SEIR
def deriv(y, t, N, beta, sigma, gamma):
    s, e, i, r = y
    dsdt = -beta * s * i / N
    dedt = beta * s * i / N - sigma * e
    didt = sigma*e - gamma * i
    drdt = gamma * i
    return dsdt, dedt, didt, drdt

# modello SEIR modificato
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
ax1.plot(t, i, 'k', alpha=0.7, lw=2, label='Infettati')
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
ax2.plot(t, i2, 'k', alpha=0.7, lw=2, label='Infettati')
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

