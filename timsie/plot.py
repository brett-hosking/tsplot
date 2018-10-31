import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})

class Series:

    def __init__(self,X,Y,xlabels_l1=[None,None],xlabels_l2=[None,None],ylabel=None,xlim=[None,None],ylim=[None,None]):
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
        self.fig, self.ax 	= plt.subplots(figsize=(27, 9), dpi=60, facecolor='w', edgecolor='k')
        self.X              = X
        self.Y              = Y
        # self.xlabels_l1     = xlabels_l1
        # self.xlabels_l2     = xlabels_l2
        # self.ylabel         = ylabel
        # self.xlim           = xlim

        if not None in xlabels_l1:
            self.ax.set_xticks(xlabels_l1[1])
            self.ax.set_xticklabels(xlabels_l1[0])

        plt.grid(True)
        if not ylabel == None:
            plt.ylabel(ylabel)
       

        # if not None in xlabels_l2:
        # Set scond x-axis
        self.ax2 = self.ax.twiny()
        # self.ax2.set_xlim(self.ax.get_xlim())
        self.ax2.set_xticks(xlabels_l2[1])
        self.ax2.set_xticklabels(xlabels_l2[0])

        self.ax2.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
        self.ax2.spines['bottom'].set_position(('outward', 36))

        if None in xlim:
            self.ax.set_xlim((min(X),max(X)))
            self.ax2.set_xlim((min(X),max(X)))
        else:
            self.ax.set_xlim((xlim[0],xlim[1]))
            self.ax2.set_xlim((xlim[0],xlim[1]))

        if None in ylim:
            self.ax.set_ylim((min(Y),max(Y)))
        else:
            self.ax.set_ylim((ylim[0],ylim[1]))

        self.fig.tight_layout()

    def scatter(self,s=10,alpha=1,c='mediumblue'):        
        self.ax.scatter(self.X,self.Y,s=s,alpha=alpha,c=c)

    def line(self,Y=[None],linewidth=2,c='midnightblue'):
        if None in Y:
            self.ax.plot(self.X,self.Y,c=c)
        else:
            self.ax.plot(self.X,Y,linewidth=linewidth,c=c)

    def save(self,path='figure.png'):      
        plt.savefig(path)      

    def show(self):
        plt.show()





def egplot(X,Y,xlabels_l1=[None,None],xlabels_l2=[None,None],ylabel=None,xlim=[None,None]):

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
    ax.plot(X,Y,linewidth=3)
    # ax.scatter(X,Y,s=10)

    if not None in xlabels_l1:
        ax.set_xticks(xlabels_l1[1])
        ax.set_xticklabels(xlabels_l1[0])

    
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

    if None in xlim:
        ax.set_xlim((min(X),max(X)))
        ax2.set_xlim((min(X),max(X)))
    else:
        ax.set_xlim((xlim[0],xlim[1]))
        ax2.set_xlim((xlim[0],xlim[1]))

    fig.tight_layout()
    # if not save == None:
    #     plt.savefig(save)
    # if show:
    plt.show()