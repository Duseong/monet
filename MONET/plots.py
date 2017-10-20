import matplotlib.pyplot as plt
import seaborn as sns
import mystats
import taylordiagram as td
from colorbars import colorbar_index
#colors = ['#1e90ff','#045C5C','#00A847','#DB4291','#BB7E5D']
colors = ['#DA70D6', '#228B22', '#FA8072', '#FF1493']
sns.set_palette(sns.color_palette(colors))

sns.set_context('poster')

# CMAQ Spatial Plots
def make_spatial_plot(cmaqvar, gridobj, date, m, dpi=None, savename='', vmin=0, vmax=150, ncolors=15, cmap='YlGnBu'):
    fig = plt.figure(figsize=(11, 6), frameon=False)
    lat = gridobj.variables['LAT'][0, 0, :, :].squeeze()
    lon = gridobj.variables['LON'][0, 0, :, :].squeeze()
    # define map and draw boundries
    m.drawstates()
    m.drawcoastlines(linewidth=.3)
    m.drawcountries()
    x, y = m(lon, lat)
    plt.axis('off')
    c, cmap = colorbar_index(ncolors, cmap, minval=vmin, maxval=vmax)
    m.pcolormesh(x, y, cmaqvar, vmin=vmin, vmax=vmax, cmap=cmap)
    titstring = date.strftime('%B %d %Y %H')
    plt.title(titstring)

    plt.tight_layout()
    if savename != '':
        plt.savefig(savename + date.strftime('%Y%m%d_%H.jpg'), dpi=dpi)
        plt.close()
    return c

def make_spatial_plot2(cmaqvar, m, dpi=None, plotargs={}, ncolors=15, discrete=False):
    #create figure
    f,ax = plt.subplots(1,1,figsize=(11, 6), frameon=False)
    #determine colorbar 
    if 'cmap' not in plotargs:
        plotargs['cmap'] = 'viridis'
    if discrete and 'vmin' in plotargs and 'vmax' in plotargs:
        c, cmap = colorbar_index(ncolors, plotargs['cmap'], minval=plotargs['vmin'], maxval=plotargs['vmax'],basemap=m)
        plotargs['cmap'] = cmap
        m.imshow(cmaqvar,**plotargs)
        vmin,vmax = plotargs['vmin'],plotargs['vmax']
    elif discrete:
        temp = m.imshow(cmaqvar,**plotargs)
        vmin,vmax = temp.get_clim()
        c, cmap = colorbar_index(ncolors, plotargs['cmap'], minval=vmin,maxval=vmax,basemap=m)
        plotargs['cmap'] = cmap
        m.imshow(cmaqvar,vmin=vmin,vmax=vmax,**plotargs)
    else:
        temp = m.imshow(cmaqvar,**plotargs)
        c = m.colorbar()
        vmin,vmax = temp.get_clim()
        cmap = plotargs['cmap']
    #draw borders
    m.drawstates()
    m.drawcoastlines(linewidth=.3)
    m.drawcountries()
    return f,ax,c,cmap,vmin,vmax    
    

def make_spatial_plot_no_obs(cmaqvar, gridobj, date, m, dpi=None, savename='', vmin=0, vmax=150, ncolors=15, cmap='viridis'):
    fig = plt.figure(figsize=(11, 6), frameon=False)
    lat = gridobj.variables['LAT'][0, 0, :, :].squeeze()
    lon = gridobj.variables['LON'][0, 0, :, :].squeeze()
    # define map and draw boundries
    m.drawstates()
    m.drawcoastlines(linewidth=.3)
    m.drawcountries()
    x, y = m(lon, lat)
    plt.axis('off')

    c, cmap = colorbar_index(ncolors, cmap, minval=vmin, maxval=vmax)
    m.pcolormesh(x, y, cmaqvar, vmin=vmin, vmax=vmax, cmap=cmap)

    plt.tight_layout()

    return c


def make_spatial_contours(cmaqvar, gridobj, date, m, dpi=None, savename='', discrete=True,ncolors=None, dtype='int',**kwargs):
    fig = plt.figure(figsize=(11, 6), frameon=False)
    lat = gridobj.variables['LAT'][0, 0, :, :].squeeze()
    lon = gridobj.variables['LON'][0, 0, :, :].squeeze()
    # define map and draw boundries
    m.drawstates()
    m.drawcoastlines(linewidth=.3)
    m.drawcountries()
    x, y = m(lon, lat)
    plt.axis('off')
    m.contourf(x, y, cmaqvar, **kwargs)
    cmap = kwargs['cmap']
    levels=kwargs['levels']
    if discrete:
        c, cmap = colorbar_index(ncolors,cmap,minval=levels[0],maxval=levels[-1],basemap=m,dtype=dtype)
#        m.contourf(x, y, cmaqvar, **kwargs,cmap=cmap)
    # c, cmap = colorbar_index(ncolors, cmap, minval=vmin, maxval=vmax)
    else:
        c = m.colorbar()
    titstring = date.strftime('%B %d %Y %H')
    plt.title(titstring)

    plt.tight_layout()
    if savename != '':
        plt.savefig(savename + date.strftime('%Y%m%d_%H.jpg'), dpi=dpi)
        plt.close()
    return c

def wind_quiver(ws,wdir,gridobj,m, **kwargs):
    import tools
    lat = gridobj.variables['LAT'][0, 0, :, :].squeeze()
    lon = gridobj.variables['LON'][0, 0, :, :].squeeze()
    # define map and draw boundries
    x, y = m(lon, lat)
    u, v = tools.wsdir2uv(ws, wdir)
    quiv = m.quiver(x[::15, ::15], y[::15, ::15], u[::15, ::15], v[::15, ::15], **kwargs)
    return quiv

def wind_barbs(ws, wdir, gridobj, m, **kwargs):
    import tools
    lat = gridobj.variables['LAT'][0, 0, :, :].squeeze()
    lon = gridobj.variables['LON'][0, 0, :, :].squeeze()
    # define map and draw boundries
    x, y = m(lon, lat)
    u, v = tools.wsdir2uv(ws, wdir)
    m.barbs(x[::15, ::15], y[::15, ::15], u[::15, ::15], v[::15, ::15], **kwargs)


def normval(vmin, vmax, cmap):
    from numpy import arange
    from matplotlib.colors import BoundaryNorm
    bounds = arange(vmin, vmax + 5., 5.)
    norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N)
    return norm


def spatial_scatter(df, m, discrete=False,plotargs={},create_cbar=True):
    x, y = m(df.Longitude.values, df.Latitude.values)
    s = 20
    if create_cbar:
        if discrete:
            cmap = cmap_discretize(cmap, ncolors)
            # s = 20
            if (type(plotargs(vmin)) == None) | (type(plotargs(vmax)) == None):
                plt.scatter(x, y, c=df['Obs'].values, **plotargs)
            else:
                plt.scatter(x, y, c=df['Obs'].values, **plotargs)
        else:
            plt.scatter(x, y, c=df['Obs'].values, **plotargs)
    else:
        plt.scatter(x,y,c=df['Obs'].values,**plotargs)


def spatial_stat_scatter(df,m,date, stat=mystats.MB,ncolors=15,fact=1.5,cmap='RdYlBu_r'):
    new = df[df.datetime == date]
    x, y = m(new.Longitude.values, new.Latitude.values)
    cmap = cmap_discretize(cmap, ncolors)
    colors = new.CMAQ - new.Obs
    ss = (new.Obs - new.CMAQ).abs() * fact

def spatial_bias_scatter(df, m, date, vmin=None, vmax=None, savename='', ncolors=15, fact=1.5, cmap='RdBu_r'):
    from scipy.stats import scoreatpercentile as score
    from numpy import around
#    plt.figure(figsize=(11, 6), frameon=False)
    f,ax = plt.subplots(figsize=(11,6),frameon=False)
    ax.set_facecolor('white')
    diff = (df.CMAQ - df.Obs)
    top = around(score(diff.abs(), per=95))
    new = df[df.datetime == date]
    x, y = m(new.Longitude.values, new.Latitude.values)
    c, cmap = colorbar_index(ncolors, cmap, minval=top*-1, maxval=top,basemap=m)
    c.ax.tick_params(labelsize=13)
#    cmap = cmap_discretize(cmap, ncolors)
    colors = new.CMAQ - new.Obs
    ss = (new.CMAQ - new.Obs).abs() /top * 100.
    ss[ss> 300] = 300.
    plt.scatter(x, y, c=colors, s=ss, vmin=-1.*top, vmax=top, cmap=cmap, edgecolors='k', linewidths=.25,alpha=.7)
    if savename != '':
        plt.savefig(savename + date + '.jpg', dpi=75.)
        plt.close()
    return f,ax,c

def eight_hr_spatial_scatter(df, m, date, savename=''):
    fig = plt.figure(figsize=(11, 6), frameon=False)
    m.drawcoastlines(linewidth=.3)
    m.drawstates()
    m.drawcountries()

    plt.axis('off')
    new = df[df.datetime_local == date]
    x, y = m(new.Longitude.values, new.Latitude.values)
    cmap = plt.cm.get_cmap('plasma')
    norm = normval(-40, 40., cmap)
    ss = (new.Obs - new.CMAQ).abs()/top*100.
    colors = new.Obs - new.CMAQ
    m.scatter(x, y, s=ss, c=colors, norm=norm, cmap=cmap)
    if savename != '':
        plt.savefig(savename + date + '.jpg', dpi=75.)
        plt.close()

def timeseries_param_new(df, col='Obs',ax=None, sample='H', plotargs={},fillargs={}):
    import pandas as pd

    if ax is None:
        f,ax = plt.subplots(figsize=(11,6),frameon=False)

    sns.set_palette(sns.color_palette(colors))
    sns.set_style('ticks')
    df.index = df.datetime
    m = df.groupby(pd.TimeGrouper(sample)).mean()
    e = df.groupby(pd.TimeGrouper(sample)).std()
    species = df.Species[0]
    unit = df.Units[0]
    upper = (m[col] + e[col]).values
    lower = m[col] - e[col]
    lower.loc[lower < 0] = 0
    lower = lower.values
    if col=='Obs': plotargs['color'] = 'darkslategrey'
    if col=='Obs': fillargs['color'] = 'darkslategrey'
    if col!='Obs' and 'color' not in plotargs: plotargs['color'] = None

    ax.plot(m[col], **plotargs)
#    print m[col].shape,lower.shape,upper,shape
    ax.fill_between(m[col].index,lower,upper,**fillargs)
    plt.gcf().autofmt_xdate()
    ax.set_ylabel(species + ' (' + unit + ')')
    plt.legend()
    return ax

def timeseries_param(df, title='', fig=None, label=None, color=None, footer=True, sample='H'):
    """                                                                                                                                                                                                                          
                                                                                                                                                                                                                                 
    :param df: pandas dataframe from a monet verification object                                                                                                                                                                 
    :param title:                                                                                                                                                                                                                
    :param fig:                                                                                                                                                                                                                  
    :param label:                                                                                                                                                                                                                
    :param color:                                                                                                                                                                                                                
    :param footer:                                                                                                                                                                                                               
    :param sample:                                                                                                                                                                                                               
    """
    import matplotlib.dates as mdates
    from numpy import isnan,NaN,nanmax,nanmin
    sns.set_style('ticks')
    df.index = df.datetime
    if fig is None:

        f = plt.figure(figsize=(16, 8))
        if label is None:
            label = 'CMAQ'
        obs = df.Obs.values
        obs[(obs < 0) | (obs > 1000)] = NaN
        df.Obs = obs
        species = df.Species.unique().astype('|S8')[0]
        units = df.Units.unique().astype('|S8')[0]
        obs = df.Obs.resample(sample).mean()
        if df.SCS.unique().shape[0] == 1:
            obserr = 0.
            cmaqerr = 0.
        else:
            obserr = df.Obs.resample(sample).std()
            cmaqerr = df.CMAQ.resample(sample).std()

        cmaq = df.CMAQ.resample(sample).mean()
        cmaqerr = df.CMAQ.resample(sample).std()
        plt.plot(obs, color='darkslategrey')
        plt.plot(cmaq, color='dodgerblue', label=label)
        plt.legend(loc='best')

        mask = ~isnan(obs) & ~isnan(obserr)
        plt.fill_between(obs.index[mask], (obs - obserr)[mask], (obs + obserr)[mask], alpha=.2, color='darkslategrey')
        mask = ~isnan(cmaq) & ~isnan(cmaqerr)
        plt.fill_between(cmaq.index[mask], (cmaq - cmaqerr)[mask], (cmaq + cmaqerr)[mask], alpha=.2, color='dodgerblue')

        ax = plt.gca().axes
        ax.set_xlabel('UTC Time (mm/dd HH)')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H'))
        plt.title(title)
        minval = nanmin([(obs - obserr).min(), (cmaq - cmaqerr).min()])
        minval = nanmax([minval, 0])
        maxval = nanmax([(cmaq + cmaqerr).max() * 1.1, (obs + obserr).max() * 1.1])
        maxval = nanmax([maxval,(obs + obserr).max() * 1.1])
        plt.gca().set_ylim(bottom=minval)
        plt.gca().set_ylim(top=maxval)
        ylabel = species + ' (' + units + ')'
        plt.gca().axes.set_ylabel(ylabel)
        if footer:
            footer_text(df)
        plt.tight_layout()
        plt.grid(alpha=.5)
    else:
        ax = fig.get_axes()[0]
        cmaq = df.CMAQ.resample(sample).mean()
        cmaqerr = df.CMAQ.resample(sample).std()
        lin, = ax.plot(cmaq, label=label)
        mask = ~isnan(cmaq) & ~isnan(cmaqerr)
        plt.fill_between(cmaq.index[mask], (cmaq - cmaqerr)[mask], (cmaq + cmaqerr)[mask], alpha=.2,
                         color=lin.get_color())
        plt.legend(loc='best')


def timeseries_error_param(df, title='', fig=None, label=None, footer=True, sample='H'):
    """

    :param df:
    :param title:
    :param fig:
    :param label:
    :param footer:
    :param sample:
    """
    import matplotlib.dates as mdates
    from numpy import sqrt
    sns.set_style('ticks')

    df.index = df.datetime
    if fig is None:
        plt.figure(figsize=(13, 8))

        species = df.Species.unique().astype('|S8')[0]
        units = df.Units.unique().astype('|S8')[0]

        mb = (df.CMAQ - df.Obs).resample(sample).mean()
        rmse = sqrt((df.CMAQ - df.Obs) ** 2).resample(sample).mean()

        a = plt.plot(mb, label='Mean Bias', color='dodgerblue')
        ax = plt.gca().axes
        ax2 = ax.twinx()
        b = ax2.plot(rmse, label='RMSE', color='tomato')
        lns = a + b
        labs = [l.get_label() for l in lns]
        plt.legend(lns, labs, loc='best')

        ax.set_xlabel('UTC Time (mm/dd HH)')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H'))
        plt.title(title)
        ylabel = species + ' (' + units + ')'
        ax.set_ylabel('MB ' + ylabel, color='dodgerblue')
        ax2.set_ylabel('RMSE ' + ylabel, color='tomato')
        if footer:
            footer_text(df)
        plt.tight_layout()
        plt.grid(alpha=.5)
    else:
        ax1 = fig.get_axes()[0]
        ax2 = fig.get_axes()[1]
        mb = (df.CMAQ - df.Obs).resample(sample).mean()
        rmse = sqrt((df.CMAQ - df.Obs) ** 2).resample(sample).mean()
        ax1.plot(mb, label=label + ' MB')
        ax2.plot(rmse, label=label + ' RMSE')
        lns = ax1.get_lines()[:] + ax2.get_lines()[1:]
        labs = [l.get_label() for l in lns]
        plt.legend(lns, labs, loc='best')


def timeseries_rmse_param(df, title='', fig=None, label=None, footer=True, sample='H'):
    """

    :param df:
    :param title:
    :param fig:
    :param label:
    :param footer:
    :param sample:
    """
    import matplotlib.dates as mdates
    from numpy import sqrt
    sns.set_style('ticks')
    df.index = df.datetime
    if fig is None:
        plt.figure(figsize=(13, 8))
        species = df.Species.unique().astype('|S8')[0]
        units = df.Units.unique().astype('|S8')[0]
        rmse = sqrt((df.CMAQ - df.Obs) ** 2).resample(sample).mean()
        plt.plot(rmse, color='dodgerblue', label=label)
        ylabel = species + ' (' + units + ')'
        plt.gca().axes.set_ylabel('RMSE ' + ylabel)
        if footer:
            footer_text(df)
        ax = plt.gca().axes
        ax.set_xlabel('UTC Time (mm/dd HH)')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H'))
        plt.tight_layout()
        plt.grid(alpha=.5)
    else:
        ax = fig.get_axes()[0]
        rmse = sqrt((df.CMAQ - df.Obs) ** 2).resample(sample).mean()
        ax.plot(rmse, label=label)
        plt.legend(loc='best')


def timeseries_mb_param(df, title='', fig=None, label=None, footer=True, sample='H'):
    """

    :param df:
    :param title:
    :param fig:
    :param label:
    :param footer:
    :param sample:
    """
    import matplotlib.dates as mdates
    sns.set_style('ticks')
    df.index = df.datetime
    if fig == None:
        plt.figure(figsize=(13, 8))
        species = df.Species.unique().astype('|S8')[0]
        units = df.Units.unique().astype('|S8')[0]
        mb = (df.CMAQ - df.Obs).resample(sample).mean()
        plt.plot(mb, color='dodgerblue', label=label)
        ylabel = species + ' (' + units + ')'
        plt.gca().axes.set_ylabel('MB ' + ylabel)
        plt.gca().axes.set_xlabel('UTC Time (mm/dd HH)')
        plt.gca().axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H'))
        if footer:
            footer_text(df)
        plt.tight_layout()
        plt.grid(alpha=.5)
    else:
        ax = fig.get_axes()[0]
        rmse = (df.CMAQ - df.Obs).resample(sample).mean()
        ax.plot(rmse, label=label)
        plt.legend(loc='best')


def kdeplots_param(df, title=None, fig=None, label=None, footer=True, cumulative=False):
    from scipy.stats import scoreatpercentile as score
    sns.set_style('ticks')

    if fig is None:

        if cumulative:
            plt.figure(figsize=(13, 8))
            sns.kdeplot(df.Obs, color='darkslategrey', cumulative=True, label='Obs')
            sns.kdeplot(df.CMAQ, color='dodgerblue', cumulative=True, label=label)
        else:
            maxval1 = score(df.CMAQ.values, per=99.5)
            maxval2 = score(df.Obs.values, per=99.5)
            maxval = max([maxval1, maxval2])
            plt.figure(figsize=(13, 8))
            sns.kdeplot(df.Obs, color='darkslategrey')
            sns.kdeplot(df.CMAQ, color='dodgerblue', label=label)

        sns.despine()
        if not cumulative:
            plt.xlim([0, maxval])
        plt.xlabel(df.Species.unique()[0] + '  (' + df.Units.unique()[0] + ')')
        plt.title(title)
        plt.gca().axes.set_ylabel('P(' + df.Species.unique()[0] + ')')
        if footer:
            footer_text(df)
        plt.tight_layout()
        plt.grid(alpha=.5)
    else:
        ax = fig.get_axes()[0]
        sns.kdeplot(df.CMAQ, ax=ax, label=label, cumulative=cumulative)


def diffpdfs_param(df, title=None, fig=None, label=None, footer=True):
    from scipy.stats import scoreatpercentile as score
    sns.set_style('ticks')

    maxval = score(df.CMAQ.values - df.Obs.values, per=99.9)
    minval = score(df.CMAQ.values - df.Obs.values, per=.1)
    if fig == None:
        plt.figure(figsize=(10, 7))
        if label == 'None':
            label = 'CMAQ - Obs'
        sns.kdeplot(df.CMAQ.values - df.Obs.values, color='darkslategrey', label=label)
        sns.despine()
        plt.xlim([minval, maxval])
        plt.xlabel(df.Species.unique()[0] + ' Difference (' + df.Units.unique()[0] + ')')
        plt.title(title)
        plt.gca().axes.set_ylabel('P( Model - Obs )')
        if footer:
            footer_text(df)
        plt.tight_layout()
    else:
        ax = fig.get_axes()[0]
        sns.kdeplot(df.CMAQ.values - df.Obs.values, ax=ax, label=label)


def scatter_param(df, title=None, fig=None, label=None, footer=True):
    from numpy import max, arange, linspace, isnan
    from scipy.stats import scoreatpercentile as score
    from scipy.stats import linregress
    sns.set_style('ticks')

    species, units = df.Species.unique()[0], df.Units.unique()[0]
    mask = ~isnan(df.Obs.values) & ~isnan(df.CMAQ.values)
    maxval1 = score(df.CMAQ.values[mask], per=99.5)
    maxval2 = score(df.Obs.values[mask], per=99.5)
    maxval = max([maxval1, maxval2])
    print maxval
    if fig == None:
        plt.figure(figsize=(10, 7))

        plt.scatter(df.Obs, df.CMAQ, c='cornflowerblue', marker='o', edgecolors='w', alpha=.3, label=label)
        x = arange(0, maxval + 1)
        if maxval <= 10.:
            x = linspace(0, maxval, 25)
        plt.plot(x, x, '--', color='slategrey')
        tt = linregress(df.Obs.values[mask], df.CMAQ.values[mask])
        plt.plot(x, tt[0] * x + tt[1], color='tomato')

        plt.xlim([0, maxval])
        plt.ylim([0, maxval])
        plt.xlabel('Obs ' + species + ' (' + units + ')')
        plt.title(title)
        plt.gca().axes.set_ylabel('Model ' + species + ' (' + units + ')')
        if footer:
            footer_text(df)
        plt.tight_layout()
        plt.grid(alpha=.5)
    else:
        ax = fig.get_axes()[0]
        l, = ax.scatter(df.Obs, df.CMAQ, marker='o', edgecolors='w', alpha=.3, label=label)
        tt = linregress(df.Obs.values, df.CMAQ.values)
        ax.plot(df.Obs.unique(), tt[0] * df.Obs.unique() + tt[1], color=l.get_color())
        plt.legend(loc='Best')


def diffscatter_param(df, title=None, fig=None, label=None, footer=True):
    from scipy.stats import scoreatpercentile as score
    from numpy import isnan
    sns.set_style('ticks')
    df = df.dropna()
    mask = ~isnan(df.Obs.values) & ~isnan(df.CMAQ.values)
    if fig == None:
        species, units = df.Species.unique()[0], df.Units.unique()[0]
        maxval = score(df.Obs.values[mask], per=99.9)
        minvaly = score(df.CMAQ.values[mask] - df.Obs.values[mask], per=.1)
        maxvaly = score(df.CMAQ.values[mask] - df.Obs.values[mask], per=99.9)
        plt.figure(figsize=(10, 7))

        plt.scatter(df.Obs.values[mask], df.CMAQ.values[mask] - df.Obs.values[mask], c='cornflowerblue', marker='o',
                    edgecolors='w', alpha=.3, label=label)
        plt.plot((0, maxval), (0, 0), '--', color='darkslategrey')

        plt.xlim([0, maxval])
        plt.ylim([minvaly, maxvaly])
        plt.xlabel('Obs ' + species + ' (' + units + ')')
        plt.title(title)
        plt.gca().axes.set_ylabel('Model - Obs ' + species + ' (' + units + ')')
        if footer:
            footer_text(df)
        plt.tight_layout()
    else:
        ax = fig.get_axes()[0]
        mask = ~isnan(df.Obs.values) & ~isnan(df.CMAQ.values)
        ax.scatter(df.Obs.values[mask], df.CMAQ.values[mask] - df.Obs.values[mask], marker='o', edgecolors='w',
                   alpha=.3, label=label)
        plt.legend(loc='best')


def timeseries(df, title=''):
    # this is the average for N sites if more than one site exists
    from numpy import sqrt, linspace
    import matplotlib.dates as mdates
    sns.set_style('ticks')
    df.index = df.datetime
    g = df.groupby('Species')
    f, ax = plt.subplots(3, 1, figsize=(15, 8), sharex=True)
    ax[0].plot(g.get_group('NOX').resample('H').mean().dropna().Obs, color='darkslategrey', label='Obs NOx', marker='o')
    ax[0].plot(g.get_group('NOX').resample('H').mean().dropna().CMAQ, color='darkorange', label='CMAQ NOx')
    ax[0].legend(loc=9)
    ####################################################################################################################
    ax[1].plot(g.get_group('OZONE').resample('H').mean().dropna().Obs, color='darkslategrey', label='Obs', marker='o')
    ax[1].plot(g.get_group('OZONE').resample('H').mean().dropna().CMAQ, color='cornflowerblue', label='CMAQ Ozone',
               lw=2)
    ax[1].legend(loc=0)
    ####################################################################################################################
    mbnox = (g.get_group('NOX').CMAQ - g.get_group('NOX').Obs).resample('H').mean()
    rmses = sqrt((g.get_group('NOX').Obs - g.get_group('NOX').CMAQ) ** 2).resample('H').mean()
    dt = g.get_group('NOX').resample('H').mean().index
    ax[2].plot(dt, mbnox, color='darkorange')
    ax3 = ax[2].twinx()
    ax3.plot(dt, rmses, color='darkorange', ls='--')
    mbnox = (g.get_group('OZONE').CMAQ - g.get_group('OZONE').Obs).resample('H').mean()
    rmses = sqrt((g.get_group('OZONE').Obs - g.get_group('OZONE').CMAQ) ** 2).resample('H').mean()
    ax[2].plot(dt, mbnox, color='cornflowerblue')
    ax3.plot(dt, rmses, color='cornflowerblue', ls='--')
    ####################################################################################################################
    ax[0].set_ylabel('NOx (pbb)', color='darkorange')
    ax[1].set_ylabel('Ozone (pbb)', color='cornflowerblue')
    ax[2].set_ylabel('Bias (Solid)')
    ax3.set_ylabel('RMSE (Dashed)')
    ax[0].set_title(title)
    ax3.set_yticks(linspace(ax3.get_ybound()[0], ax3.get_ybound()[1], 6))
    ax[2].set_yticks(linspace(ax[2].get_ybound()[0], ax[2].get_ybound()[1], 6))
    ax[2].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H'))
    ax[2].set_xlabel('Time (mm/dd HH)')
    plt.tight_layout()

    f, ax = plt.subplots(3, 1, figsize=(15, 8), sharex=True)
    ax[0].set_title(title)

    ####################################################################################################################
    ax[0].plot(g.get_group('CO').resample('H').mean().dropna().Obs, color='darkslategrey',
               label='Obs CO', marker='o')  # this is the average for N sites
    ax[0].plot(g.get_group('CO').resample('H').mean().dropna().CMAQ, color='seagreen',
               label='CMAQ CO', lw=2)  # this is the average for N sites
    ax[0].legend(loc=0)
    ####################################################################################################################
    ax[1].plot(g.get_group('SO2').resample('H').mean().dropna().Obs, color='darkslategrey', label='Obs SO2', marker='o')
    ax[1].plot(g.get_group('SO2').resample('H').mean().dropna().CMAQ, color='slateblue', label='CMAQ SO2', ls='-', lw=2)
    ax[1].legend(loc=0)
    ####################################################################################################################
    mbnox = (g.get_group('CO').CMAQ - g.get_group('CO').Obs).resample('H').mean()
    rmses = sqrt((g.get_group('CO').Obs - g.get_group('CO').CMAQ) ** 2).resample('H').mean()
    dt = g.get_group('CO').resample('H').mean().index
    ax3 = ax[2].twinx()
    ax[2].plot(dt, mbnox, color='seagreen')
    ax3.plot(dt, rmses, color='seagreen', ls='--')
    mbnox = (g.get_group('SO2').CMAQ - g.get_group('SO2').Obs).resample('H').mean()
    rmses = sqrt((g.get_group('SO2').Obs - g.get_group('SO2').CMAQ) ** 2).resample('H').mean()
    ax[2].plot(dt, mbnox, color='slateblue')
    ax3.plot(dt, rmses, color='slateblue', ls='--')
    ####################################################################################################################

    ax[0].set_ylabel('CO (pbb)', color='seagreen')
    ax[1].set_ylabel('SO2 (pbb)', color='slateblue')
    ax[2].set_ylabel('Bias (Solid)')
    ax3.set_ylabel('RMSE (Dashed)')
    ax3.set_yticks(linspace(ax3.get_ybound()[0], ax3.get_ybound()[1], 6))
    ax[2].set_yticks(linspace(ax[2].get_ybound()[0], ax[2].get_ybound()[1], 6))
    ax[2].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H'))
    ax[2].set_xlabel('Time (mm/dd HH)')
    plt.tight_layout()


def domain_bar(df):
    import mystats
    from pandas import DataFrame
    from numpy import array
    name, nmb, ioa, r2, rmse = [], [], [], [], []
    for n, g in df.groupby('Species'):
        name.append(n)
        nmb.append(mystats.NMB(g.Obs.values, g.CMAQ.values))
        ioa.append(mystats.IOA(g.Obs.values, g.CMAQ.values))
        r2.append(mystats.R2(g.Obs.values, g.CMAQ.values))
        rmse.append(mystats.RMSE(g.Obs.values, g.CMAQ.values))
        sns.set_style('white')
        df2 = DataFrame(array([nmb, rmse, r2, ioa]).T,
                        columns=['Normalized Mean Bias', 'RMSE', 'R2', 'Index of Agreement'])
    f, ax = plt.subplots(figsize=(8, 5))
    df2.plot.bar(alpha=.9, width=.9, ax=ax)
    ax.set_title('Domain Statistics')
    ax.xaxis.set_ticklabels(name, rotation=35)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_title('Domain Statistics')


def kdeplots(df):
    from numpy import max
    from scipy.stats import linregress
    from scipy.stats import scoreatpercentile as score
    from mystats import NMB, NME, MB
    sns.set_style('ticks')
    for n, g in df.groupby('Species'):
        g = g.copy().dropna()
        tt = linregress(g.Obs.values, g.CMAQ.values)
        plt.figure(figsize=(10, 7))
        sns.kdeplot(g.Obs)
        sns.kdeplot(g.CMAQ)
        sns.despine()

        maxval1 = score(g.CMAQ.values, per=99.5)
        maxval2 = score(g.Obs.values, per=99.5)
        maxval = max([maxval1, maxval2])
        nmb = NMB(g.Obs.values, g.CMAQ.values)
        nme = NME(g.Obs.values, g.CMAQ.values)
        mb = MB(g.Obs.values, g.CMAQ.values)
        footer_text(g)
        plt.xlim([0, maxval])
        plt.xlabel(n + '  (' + g.Units.unique()[0] + ')')
        plt.ylabel('P(' + n + ')')
        plt.tight_layout()


def scatter(df):
    from numpy import max, arange, linspace
    from scipy.stats import scoreatpercentile as score
    from scipy.stats import linregress
    from mystats import NMB, NME, MB
    sns.set_style('ticks')
    for n, g in df.groupby('Species'):
        plt.figure(figsize=(10, 7))
        g = g.copy().dropna()

        tt = linregress(g.Obs.values, g.CMAQ.values)

        maxval1 = score(g.CMAQ.values, per=99.9)
        maxval2 = score(g.Obs.values, per=99.9)
        maxval = max([maxval1, maxval2])
        nmb = NMB(g.Obs.values, g.CMAQ.values)
        nme = NME(g.Obs.values, g.CMAQ.values)
        mb = MB(g.Obs.values, g.CMAQ.values)
        textstr = '$R^2$    = $%.3f$\nNMB = $%.2f$\nNME = $%.2f$\nMB  = $%.2f$' % (tt[2], nmb, nme, mb)
        plt.scatter(g.Obs, g.CMAQ, c='cornflowerblue', marker='o', edgecolors='w', alpha=.3)
        x = arange(0, maxval)
        if maxval <= 10.:
            x = linspace(0, maxval, 25)
        plt.plot(x, x, '--', color='slategrey')
        plt.plot(x, tt[0] * x + tt[1], color='tomato')
        plt.xlim([0, maxval])
        plt.ylim([0, maxval])
        ax = plt.gca().axes
        footer_text(g)
        sns.despine()
        plt.xlabel('Obs')
        plt.ylabel('CMAQ')
        plt.title(n + '  (' + g.Units.unique()[0] + ')')
        plt.tight_layout()


def footer_text(df):
    from numpy import unique, isnan
    from mystats import NMB, NME, MB, d1
    mask = ~isnan(df.Obs.values) & ~isnan(df.CMAQ.values)
    nmb = NMB(df.Obs.values[mask], df.CMAQ.values[mask])
    nme = NME(df.Obs.values[mask], df.CMAQ.values[mask])
    mb = MB(df.Obs.values[mask], df.CMAQ.values[mask])
    d1ioa = d1(df.Obs.values[mask], df.CMAQ.values[mask])
    plt.figtext(.03, .04, df.datetime.min().strftime('START DATE: %Y-%m-%d %H UTC'), fontsize=11, family='monospace')
    plt.figtext(.03, .02, df.datetime.max().strftime('END DATE  : %Y-%m-%d %H UTC'), fontsize=11, family='monospace')
    plt.figtext(0.8, .02, 'd1 = %.3f' % d1ioa, fontsize=11, family='monospace')
    plt.figtext(0.9, .02, 'NME = %.1f' % nme, fontsize=11, family='monospace')
    plt.figtext(0.8, .04, 'MB = %.1f' % mb, fontsize=11, family='monospace')
    plt.figtext(0.9, .04, 'NMB = %.1f' % nmb, fontsize=11, family='monospace')
    plt.figtext(.3, .04, 'SITES: ' + str(unique(df.SCS.values[mask]).shape[0]), fontsize=11, family='monospace')
    plt.figtext(.3, .02, 'MEASUREMENTS: ' + str(df.SCS.count()), fontsize=11, family='monospace')


# def colorbar_index(ncolors, cmap, minval=None, maxval=None):
#     import matplotlib.cm as cm
#     import numpy as np
#     cmap = cmap_discretize(cmap, ncolors)
#     mappable = cm.ScalarMappable(cmap=cmap)
#     mappable.set_array([])
#     mappable.set_clim(-0.5, ncolors + 0.5)
#     colorbar = plt.colorbar(mappable, format='%1.2g')
#     colorbar.set_ticks(np.linspace(0, ncolors, ncolors))
#     if (type(minval) == None) & (type(maxval) != None):
#         colorbar.set_ticklabels(np.around(np.linspace(0, maxval, ncolors).astype('float'), 2))
#     elif (type(minval) == None) & (type(maxval) == None):
#         colorbar.set_ticklabels(np.around(np.linspace(0, ncolors, ncolors).astype('float'), 2))
#     else:
#         colorbar.set_ticklabels(np.around(np.linspace(minval, maxval, ncolors).astype('float'), 2))

#     return colorbar, cmap


# def cmap_discretize(cmap, N):
#     """
#     Return a discrete colormap from the continuous colormap cmap.

#     cmap: colormap instance, eg. cm.jet.
#     N: number of colors.

#     Example
#         x = resize(arange(100), (5,100))
#         djet = cmap_discretize(cm.jet, 5)
#         imshow(x, cmap=djet)
#     """
#     import matplotlib.colors as mcolors
#     import numpy as np

#     if type(cmap) == str:
#         cmap = plt.get_cmap(cmap)
#     colors_i = np.concatenate((np.linspace(0, 1., N), (0., 0., 0., 0.)))
#     colors_rgba = cmap(colors_i)
#     indices = np.linspace(0, 1., N + 1)
#     cdict = {}
#     for ki, key in enumerate(('red', 'green', 'blue')):
#         cdict[key] = [(indices[i], colors_rgba[i - 1, ki], colors_rgba[i, ki])
#                       for i in xrange(N + 1)]
#     # Return colormap object.
#     return mcolors.LinearSegmentedColormap(cmap.name + "_%d" % N, cdict, 1024)


def taylordiagram(df, marker='o', label='CMAQ', addon=False, dia=None):
    from numpy import corrcoef

    df = df.drop_duplicates().dropna(subset=['Obs', 'CMAQ'])

    if not addon and dia is None:
        f = plt.figure(figsize=(12, 10))
        sns.set_style('ticks')
        obsstd = df.Obs.std()

        dia = td.TaylorDiagram(obsstd, fig=f, rect=111, label='Obs')
        plt.grid(linewidth=1, alpha=.5)

        cc = corrcoef(df.Obs.values, df.CMAQ.values)[0, 1]
        dia.add_sample(df.CMAQ.std(), cc, marker=marker, zorder=9, ls=None, label=label)
        contours = dia.add_contours(colors='0.5')
        plt.clabel(contours, inline=1, fontsize=10)
        plt.grid(alpha=.5)
        plt.legend(fontsize='small', loc='best')
        plt.tight_layout()

    elif not addon and dia is not None:
        print 'Do you want to add this on? if so please turn the addon keyword to True'
    elif addon and dia is None:
        print 'Please pass the previous Taylor Diagram Instance with dia keyword...'
    else:
        cc = corrcoef(df.Obs.values, df.CMAQ.values)[0, 1]
        dia.add_sample(df.CMAQ.std(), cc, marker=marker, zorder=9, ls=None, label=label)
        plt.legend(fontsize='small', loc='best')
        plt.tight_layout()
    return dia
