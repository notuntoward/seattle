import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import pandas as pd
    from pathlib import Path
    from tabulate import tabulate

    datdir = Path("~/tmp")
    dfr = pd.read_csv(datdir / "EdgeFeature-ChromeWorkaround-KeyExtensionTool Research.csv")

    dfg = pd.read_csv(datdir / "EdgeFeature-ChromeWorkaroundSolution Gemini.csv")
    df = pd.merge(dfr, dfg, on="Edge Feature", how='outer')

    #print(df.to_markdown(tablefmt="github"))
    df.to_csv(datdir / "merged.csv", encoding='utf-8-sig', index=False)
    return (df,)


@app.cell
def _(df):
    df
    return


if __name__ == "__main__":
    app.run()
