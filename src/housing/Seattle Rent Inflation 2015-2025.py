import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Seattle Area House Price Increases vs. Time
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    # Import zillow data
    import itertools
    import requests
    import pandas as pd
    import datetime
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import numpy as np
    from brokenaxes import brokenaxes

    URL_ZILLOW_BASE = "https://files.zillowstatic.com/research/public_csvs/zori/"
    REGION_NAME_HEAD_GET = 'Seattle'

    # Geographies you requested
    geos = ["City", "Metro"]

    # Smoothing options
    smooth = {
        "sm": "sm",
        "raw": "raw",
    }

    # Product types you requested (these suffixes are the part that varies most in Zillow filenames)
    # We'll try a few common conventions.
    product_suffixes = {
        "all_homes": [
            "uc_sfrcondomfr",      # commonly used for "all homes" in ZORI
            "uc_sfrcondo",         # sometimes used elsewhere
        ],
        "multifamily": [
            "uc_mfr",              # common shorthand
            "uc_mf",
            "uc_multifamily",
        ],
        "single_family": [
            "uc_sfr",
            "uc_singlefamily",
            "uc_single_family",
        ],
    }

    def head_ok(url: str) -> bool:
        r = requests.head(url, allow_redirects=True, timeout=20)
        return r.status_code == 200

    def is_datetime_convertible(series):
        try:
            pd.to_datetime(series.dropna(), errors='raise')
            return True
        except:
            return False

    df_all = []
    for geo, sm_key in itertools.product(geos, smooth):
        for series, suffix_list in product_suffixes.items():
            for suffix in suffix_list:
                fn = f"{geo}_zori_{suffix}_{smooth[sm_key]}_month.csv"
                url = URL_ZILLOW_BASE + fn
                if head_ok(url):
                    if sm_key != 'sm':
                        raise ValueError(f'unexpected {sm_key=}')
                    print(f"Found: {geo}, {series}, {sm_key}, {url}")

                    df = pd.read_csv(url)

                    is_region_row = df.RegionName.str.startswith(REGION_NAME_HEAD_GET)
                    if (num_region_rows := sum(is_region_row)) != 1:
                        raise ValueError(f'{num_region_rows=} != 1')

                    is_date_col = (df.columns.to_series()
                                     .apply(lambda x: pd.to_datetime(x,errors='coerce') 
                                                      == pd.to_datetime(x, errors='coerce'))
                                   ).values

                    df = df.loc[is_region_row,is_date_col].T

                    df.columns = ['price'] + list(df.columns[1:])
                    df['geo']=geo
                    df['smooth']=sm_key
                    df['series']=series
                    df['suffix']=suffix
                    df['Rental Type'] = f'{geo}_{series}'
                    df_all.append(df.reset_index(names='date'))

    df_all = pd.concat(df_all)
    return brokenaxes, df_all, mdates, np, pd, plt


@app.cell
def _(df_all, pd):
    df_plot = df_all[['date','price','Rental Type']].pivot(index='date', columns='Rental Type', values='price')
    df_plot.index = pd.to_datetime(df_plot.index)

    # Time stamps are at different days for the same month across years.
    # Keep lags by a year by assigning the most common day for each month to the timestamp
    df_plot['year'] = df_plot.index.year
    df_plot['month'] = df_plot.index.month
    df_plot['day'] = df_plot.index.day

    mode_day = df_plot.groupby('month')['day'].agg(lambda x: x.mode() if len(x.mode()) > 0 else None).to_dict()
    df_plot.index = pd.to_datetime(dict(year=df_plot.year, month=df_plot.month, day=[mode_day[m] for m in df_plot.month]))
    df_plot = df_plot.drop(['year','month', 'day'], axis=1)
    return (df_plot,)


@app.cell
def _(df_plot):
    df_plot
    return


@app.cell
def _(df_plot, plt):
    df_plot.plot(ylabel='Monthly Rent ($)', xlabel='Date')
    plt.legend(title='Rental Type', alignment='left')
    return


@app.cell
def _(df_plot, pd, plt):
    df_prev = df_plot.shift(freq=pd.DateOffset(years=1))
    df_diff = df_plot - df_prev
    df_diff.plot(ylabel='Monthly Rent Change ($, year over year)', xlabel='Date')
    plt.legend(title='Rental Type', alignment='left')
    return df_diff, df_prev


@app.cell
def _(df_diff, df_prev, plt):
    df_diff_pct = 100 * df_diff/df_prev
    df_diff_pct.plot(ylabel='Year-to-Year Percent Change in Monthly Rent', xlabel='Date')
    plt.legend(title='Rental Type', alignment='left')
    return (df_diff_pct,)


@app.cell
def _(df_plot, plt, pltnames):
    df_plot[pltnames].plot(ylabel='Monthly Rent ($)', xlabel='Date')
    plt.title('Rent vs. Time in Seattle Metro Area')
    plt.legend(title='Rental Type', alignment='left')
    return


@app.cell
def _(df_diff_pct, plt):
    pltnames=['Metro_multifamily','Metro_single_family']
    df_diff_pct[pltnames].plot(ylabel='Year-to-Year Percent Change in Monthly Rent', xlabel='Date')
    plt.axhline(y=0, color='black', linewidth=1)
    plt.title('Year-to-Year Rent Increases in Seattle Metro Area')
    plt.legend(title='Rental Type', alignment='left')
    return (pltnames,)


@app.cell
def _(brokenaxes, df_diff_pct, mdates, plt):
    # shrinking out COVID w/ discontinuity marker
    start_date1 = df_diff_pct.index[0]
    end_date1 = df_diff_pct.index[df_diff_pct.index.year >= 2020][0]
    start_date2 = df_diff_pct.index[df_diff_pct.index.year >= 2024][0]
    end_date2 = df_diff_pct.index[-1]

    bax = brokenaxes(xlims=((start_date1, end_date1), (start_date2, end_date2)),
                    wspace=0.05, ylims=((0, 11),),
                     despine=False) # so standard box around plot is displayed
    for col in ["Metro_multifamily", "Metro_single_family"]:
        bax.plot(df_diff_pct.index, df_diff_pct[col], label=col)

    for ax in bax.axs:
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    # loc='upper right' puts it in the corner.
    # bbox_to_anchor allows fine-tuning (x, y). 
    # (1.0, 1.0) is the top-right corner of the axes.
    bax.legend(title='Rental Type', alignment='left', loc='upper right',
               bbox_to_anchor=(1, 0.96))

    bax.set_xlabel('Date')
    bax.set_ylabel('Year-to-Year Percent Change in Monthly Rent')
    plt.title('Year-to-Year Rent Increases in Seattle Metro Area (COVID era removed)', y=1.03)
    return


@app.cell
def _(df_diff_pct, np, pltnames):
    # setting COVID time to blank
    dfp = df_diff_pct
    dfp.loc[(dfp.index.year >= 2020) & (dfp.index.year < 2024)] = np.nan
    dfp[pltnames].plot()
    return


if __name__ == "__main__":
    app.run()
