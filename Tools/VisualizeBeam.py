import matplotlib.pyplot as plt

def plot_traj(x, y, alpha=0.3, xlabel='x', ylabel='y', savefig=False, 
        figname='default_name.png', fig=plt, xlim=None, ylim=None):
    for idx in range(len(x)):
        if idx < len(x)/3:
            if idx == 0:
                fig.plot(x[idx], y[idx], color='blue',
                         label="m = 235", alpha=alpha)
            else:
                fig.plot(x[idx], y[idx], color='blue',
                         alpha=0.3)
        elif idx >= len(x)/3 and idx < 2*len(x)/3:
            if idx == len(x)/3:
                fig.plot(x[idx], y[idx], color='green',
                         label="120 < m < 160", alpha=alpha)
            else:
                fig.plot(x[idx], y[idx], color='green',
                         alpha=0.3)
        else:
            if idx == 2*len(x)/3:
                fig.plot(x[idx], y[idx], color='red',
                         label="70 < m < 120", alpha=alpha)
            else:
                fig.plot(x[idx], y[idx], color='red',
                         alpha=0.3)
    fig.legend()
    if fig == plt:
        fig.xlabel(xlabel)
        fig.ylabel(ylabel)
        if xlim:
            fig.xlim(xlim)
        if ylim:
            fig.ylim(ylim)
    else:
        fig.set_xlabel(xlabel)
        fig.set_ylabel(ylabel)
        if xlim:
            fig.set_xlim(xlim)
        if ylim:
            fig.set_ylim(ylim)
    if savefig:
        fig.savefig(figname)