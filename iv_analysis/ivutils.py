import numpy as np
import matplotlib.pyplot as plt

def plot_iv(IVobject, temps="all", chans="all", showfit=True, lgcsave=False, savepath="", savename=""):
    """
    Function to plot the IV curves for the data in an IV object.
    
    Parameters
    ----------
        IVobject : class
            The IV class object that the data is stored in.
        temps : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        chans : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        showfit : boolean, optional
            Boolean flag to also plot the linear fit to the normal data
        lgcsave : boolean, optional
            Boolean flag to save the plot
        savepath : string, optional
            Path to save the plot to, saves it to the current directory by default
        savename : string, optional
            Name to append to the plot file name, if saving
    """
    
    ntemps, nch, niters = IVobject.dites.shape
    chan_names = IVobject.chan_names
    
    if temps == "all":
        trange = range(ntemps)
    elif np.isscalar(temps):
        trange = np.array([temps])
    else:
        trange = np.array(temps)
        
    if chans == "all":
        chrange = range(nch)
    elif np.isscalar(chans):
        chrange = np.array([chans])
    else:
        chrange = np.array(chans)
    
    ch_colors = plt.cm.viridis(np.linspace(0, 1, num=len(trange)*len(chrange)))
    
    fig, ax = plt.subplots(figsize=(10,6))
    
    for it, t in enumerate(trange):
        for ich, ch in enumerate(chrange):
            if ntemps > 1:
                label_str=f"Temp {t}, Channel {chan_names[ich]}"
            else:
                label_str=f"Channel {chan_names[ich]}"
            ax.scatter(IVobject.vb[t, ch]*1e6, IVobject.ites[t, ch]*1e6,label=label_str ,
                        color=ch_colors[it*len(chrange) + ich], s=10.0)
            ax.plot(IVobject.vb[t, ch]*1e6, IVobject.ites[t, ch]*1e6, color=ch_colors[it*len(chrange) + ich], alpha=0.5)
            ax.errorbar(IVobject.vb[t, ch]*1e6, IVobject.ites[t, ch]*1e6, yerr=IVobject.ites_err[t, ch]*1e6,
                         linestyle='None', color='k')
            if showfit:
                maxind = np.argmax(abs(IVobject.vb[t, ch]))
                
                if IVobject.vb[t, ch, maxind] > 0:
                    vbfit = np.linspace(0, max(IVobject.vb[t,ch]*1e6), num=10)
                else:
                    vbfit = np.linspace(min(IVobject.vb[t,ch]*1e6), 0, num=10)
                    
                ax.plot(vbfit, 1.0/(IVobject.rfit[t, ch])*vbfit, color=ch_colors[it*len(chrange) + ich], alpha=0.1)

    ax.legend(loc='best')
    ax.set_xlabel(r'Bias Voltage [$\mu V$]')
    ax.set_ylabel(r'Current through TES [$\mu A$]')
    ax.grid(linestyle='dotted')
    ax.tick_params(which='both',direction='in',right=True,top=True)
    ax.set_title("$I_0$ vs. $V_b$")
    
    if lgcsave:
        fig.savefig(savepath+f"iv_curve_{savename}.png")
        plt.close(fig)
    else:
        plt.show()

def plot_rv(IVobject, temps="all", chans="all", lgcsave=False, savepath="", savename=""):
    """
    Function to plot the resistance curves for the data in an IV object.
    
    Parameters
    ----------
        IVobject : class
            The IV class object that the data is stored in.
        temps : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        chans : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        lgcsave : boolean, optional
            Boolean flag to save the plot
        savepath : string, optional
            Path to save the plot to, saves it to the current directory by default
        savename : string, optional
            Name to append to the plot file name, if saving
    """

    ntemps, nch, niters = IVobject.r0.shape
    chan_names = IVobject.chan_names
    
    if temps == "all":
        trange = range(ntemps)
    elif np.isscalar(temps):
        trange = np.array([temps])
    else:
        trange = np.array(temps)
        
    if chans == "all":
        chrange = range(nch)
    elif np.isscalar(chans):
        chrange = np.array([chans])
    else:
        chrange = np.array(chans)
    
    ch_colors = plt.cm.viridis(np.linspace(0, 1, num=len(trange)*len(chrange)))
    
    fig, ax = plt.subplots(figsize=(10,6))
    
    for it, t in enumerate(trange):
        for ich, ch in enumerate(chrange):
            if ntemps > 1:
                label_str=f"Temp {t}, Channel {chan_names[ich]}"
            else:
                label_str=f"Channel {chan_names[ich]}"
            ax.scatter(IVobject.vb[t, ch]*1e6, IVobject.r0[t, ch]*1e3, label=label_str,
                        color=ch_colors[it*len(chrange) + ich], s=10.0)
            ax.plot(IVobject.vb[t, ch]*1e6, IVobject.r0[t, ch]*1e3, color=ch_colors[it*len(chrange) + ich], alpha=0.5)
            ax.errorbar(IVobject.vb[t, ch]*1e6, IVobject.r0[t, ch]*1e3, yerr=IVobject.r0_err[t, ch]*1e3,
                         linestyle='None', color='k')

    ax.legend(loc='best')
    ax.set_xlabel(r'Bias Voltage [$\mu V$]')
    ax.set_ylabel(r'Resistance of TES [$m \Omega$]')
    ax.grid(linestyle='dotted')
    ax.tick_params(which='both',direction='in',right=True,top=True)
    ax.set_title(r"$R_0$ vs. $V_b$")
    
    if lgcsave:
        fig.savefig(savepath+f"rv_curve_{savename}.png")
        plt.close(fig)
    else:
        plt.show()
        

def plot_pv(IVobject,  temps="all", chans="all", lgcsave=False, savepath="", savename=""):
    """
    Function to plot the power curves for the data in an IV object.
    
    Parameters
    ----------
        IVobject : class
            The IV class object that the data is stored in.
        temps : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        chans : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        lgcsave : boolean, optional
            Boolean flag to save the plot
        savepath : string, optional
            Path to save the plot to, saves it to the current directory by default
        savename : string, optional
            Name to append to the plot file name, if saving
    """

    ntemps, nch, niters = IVobject.ptes.shape
    chan_names = IVobject.chan_names
    
    if temps == "all":
        trange = range(ntemps)
    elif np.isscalar(temps):
        trange = np.array([temps])
    else:
        trange = np.array(temps)
        
    if chans == "all":
        chrange = range(nch)
    elif np.isscalar(chans):
        chrange = np.array([chans])
    else:
        chrange = np.array(chans)
    
    ch_colors = plt.cm.viridis(np.linspace(0, 1, num=len(trange)*len(chrange)))
    
    fig, ax = plt.subplots(figsize=(10,6))
    
    for it, t in enumerate(trange):
        for ich, ch in enumerate(chrange):
            if ntemps > 1:
                label_str=f"Temp {t}, Channel {chan_names[ich]}"
            else:
                label_str=f"Channel {chan_names[ich]}"
            ax.scatter(IVobject.vb[t, ch]*1e6, IVobject.ptes[t, ch]*1e12, label=label_str,
                        color=ch_colors[it*len(chrange) + ich], s=10.0)
            ax.plot(IVobject.vb[t, ch]*1e6, IVobject.ptes[t, ch]*1e12, color=ch_colors[it*len(chrange) + ich], alpha=0.5)
            ax.errorbar(IVobject.vb[t, ch]*1e6, IVobject.ptes[t, ch]*1e12, yerr=IVobject.ptes_err[t, ch]*1e12,
                         linestyle='None', color='k')

    ax.legend(loc='best')
    ax.set_xlabel(r'Bias Voltage [$\mu V$]')
    ax.set_ylabel(r'Power [$pW$]')
    ax.grid(linestyle='dotted')
    ax.tick_params(which='both',direction='in',right=True,top=True)
    ax.set_title("$P_0$ vs. $V_b$")
    ax.set_ylim(0,.8)
    ax.set_xlim(-.8,0)
    
    
    if lgcsave:
        fig.savefig(savepath+f"pv_curve_{savename}.png")
        plt.close(fig)
    else:
        plt.show()
        
def plot_all_curves(IVobject,  temps="all", chans="all", showfit=True, lgcsave=False, savepath="", savename=""):
    """
    Function to plot the IV, resistance, and power curves for the data in an IV object.
    
    Parameters
    ----------
        IVobject : class
            The IV class object that the data is stored in.
        temps : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        chans : string, array_like, int, optional
            Which bath temperatures to plot. Setting to "all" plots all of them. Can also set
            to a subset of bath temperatures, or just one
        showfit : boolean, optional
            Boolean flag to also plot the linear fit to the normal data
        lgcsave : boolean, optional
            Boolean flag to save the plot
        savepath : string, optional
            Path to save the plot to, saves it to the current directory by default
        savename : string, optional
            Name to append to the plot file name, if saving
    """
    
    plot_iv(IVobject,  temps=temps, chans=chans, showfit=showfit, lgcsave=lgcsave, savepath=savepath, savename=savename)
    plot_rv(IVobject,  temps=temps, chans=chans, lgcsave=lgcsave, savepath=savepath, savename=savename)
    plot_pv(IVobject,  temps=temps, chans=chans, lgcsave=lgcsave, savepath=savepath, savename=savename)