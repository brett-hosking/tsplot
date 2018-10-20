import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})

def series(X,Y,xlabels_l1=[None,None],xlabels_l2=[None,None],ylabel=None,save=None):
    '''
        Plot a time series of variable Y over time X

        Parameters
        ----------
        X : array
            time index
        Y: array
            variable values
        xlabels_l1 : list of length 2
            [labels,tick positions] for xaxis 1
        xlabels_l2 : list of length 2
            [labels,tick positions] for xaxis 2
        ylabel : string
            label for variable Y
        save : string
            figure save path
        Returns
        '''''''
        None

    '''
    fig, ax 	= plt.subplots(figsize=(27, 9), dpi=60, facecolor='w', edgecolor='k')
    ax.scatter(X,Y,s=20)

    if not None in xlabels_l1:
        ax.set_xticks(xlabels_l1[1])
        ax.set_xticklabels(xlabels_l1[0])

    ax.set_xlim((min(X),max(X)))
    plt.grid(True)
    if not ylabel == None:
        plt.ylabel(ylabel)
    ax.set_ylim((min(Y),max(Y)))

    # if not None in xlabels_l2:
    # Set scond x-axis
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(xlabels_l2[1])
    ax2.set_xticklabels(xlabels_l2[0])

    ax2.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
    ax2.spines['bottom'].set_position(('outward', 36))
    ax2.set_xlim((min(X),max(X)))

    fig.tight_layout()
    if not save == None:
        plt.savefig(save)
