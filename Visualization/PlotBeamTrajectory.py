import matplotlib.pyplot as plt
import numpy as np


def plot_traj_single_ptcl_type(x, y, alpha=0.3, xlabel='x', ylabel='y', savefig=False,
                               figname='traj_n=5e19.png', fig=plt, xlim=None, ylim=None):
    for idx in range(len(x)):
        if idx == 0:
            fig.plot(x[idx], y[idx], color='blue', label="m_Pb = 207", alpha=alpha)
        else:
            fig.plot(x[idx], y[idx], color='blue', alpha=0.3)
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


def plot_traj_multy_ptcls_type(x, y, ptcl_type_num=1, colors=('blue',), labels=None,
                               alpha=0.3, xlabel='x', ylabel='y', savefig=False,
                               figname='traj_n=5e19.png', fig=plt, xlim=None, ylim=None,
                               legend=True, linestyles=None, font_label=None):
    assert len(x) == len(y)
    idx_split = [set(item) for item in np.split(np.arange(len(x)), ptcl_type_num)]
    assert len(colors) == len(idx_split) == len(labels)
    if linestyles is None:
        linestyles = ('-',)*len(colors)
    if font_label is None:
        font_label = 8

    label_flag = dict()
    for label in labels:
        label_flag.update({label: True})
    for idx in range(len(x)):
        for idx_set, color, label, linestyle in zip(idx_split, colors, labels, linestyles):
            if idx in idx_set:
                if label_flag[label]:
                    fig.plot(x[idx], y[idx], color=color, alpha=alpha, label=label)
                    label_flag[label] = False
                else:
                    fig.plot(x[idx], y[idx], color=color, alpha=alpha, ls=linestyle)
    if legend:
        fig.legend(frameon=False)
    if fig == plt:
        fig.xlabel(xlabel, fontsize=font_label)
        fig.ylabel(ylabel, fontsize=font_label)
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