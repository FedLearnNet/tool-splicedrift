from pathlib import Path
from typing import Optional

import pandas as pd
from typing_extensions import override
from pyfedappwrap.learning.app_types import BaseSelfLearnedApp
from splicedrift.model import fit
from splicedrift.plotting import plot_scatter

from config import MyAppConfig, MyAppInputConfig, MyAppOutputConfig


class SpliceDriftApp(
    BaseSelfLearnedApp[MyAppConfig, MyAppInputConfig, MyAppOutputConfig]
):
    def __init__(self):
        super().__init__()

    def run_algorithm(self, data: MyAppInputConfig) -> MyAppOutputConfig:
        df = data.junction_counts

        self.logger.info(
            f"SpliceDrift: {df.shape[0]} rows, "
            f"{df['event_id'].nunique()} events, "
            f"draws={self.config.draws}, tune={self.config.tune}, chains={self.config.chains}"
        )

        # ---- Run the Bayesian model ----
        results = fit(
            df,
            draws=self.config.draws,
            tune=self.config.tune,
            chains=self.config.chains,
            cores=1,
            target_accept=self.config.target_accept,
            min_total=self.config.min_total,
            max_refits=self.config.max_refits,
            quiet=True,
        )

        # ---- Send progress metrics ----
        n_events = int(results["event_id"].nunique())
        n_groups = int(results["group"].nunique())
        self.send_metric("events_fitted", n_events, 0)
        self.send_metric("groups", n_groups, 0)
        self.send_metric("total_fits", len(results), 0)
        self.send_metric(
            "diagnostics_ok_pct",
            round(100 * results["diagnostics_ok"].mean(), 1),
            0,
        )

        # ---- Save results table ----
        results_path = Path("results.tsv")
        results.to_csv(results_path, sep="\t", index=False)

        # ---- Generate scatter plot ----
        scatter_path = Path("scatter.png")
        plot_scatter(results, save=str(scatter_path), ncols=2)

        # ---- Build ECharts visualisation for the platform UI ----
        vis = self._build_scatter_chart(results)

        return MyAppOutputConfig(
            results=results,
            scatter_plot=scatter_path,
            visualisations=vis,
        )

    def _build_scatter_chart(self, results: pd.DataFrame) -> list:
        """Build an ECharts scatter config from the results."""
        groups = results["group"].unique().tolist()
        series = []
        for grp in groups:
            sub = results[results["group"] == grp]
            data_points = [
                [round(float(r["alpha_prime_mean"]), 4),
                 round(float(r["beta_prime_mean"]), 4)]
                for _, r in sub.iterrows()
            ]
            series.append({
                "name": grp,
                "type": "scatter",
                "symbolSize": 10,
                "data": data_points,
            })

        chart = {
            "name": "α' vs β' scatter",
            "description": (
                "Each point is one splicing event. "
                "α' = age effect on mean PSI; "
                "β' = age effect on variability (precision). "
                "Points in the lower-left quadrant show aging decay."
            ),
            "visualisation": {
                "title": {"text": "SpliceDrift: α' vs β'"},
                "tooltip": {"trigger": "item"},
                "legend": {"type": "scroll"},
                "grid": {"containLabel": True},
                "xAxis": {
                    "type": "value",
                    "name": "α' (mean PSI effect)",
                },
                "yAxis": {
                    "type": "value",
                    "name": "β' (precision effect)",
                },
                "series": series,
            },
        }
        return [chart]

    @override
    def get_test_data(self) -> Optional[dict[str, Path]]:
        return {"junction_counts": Path("data/example_input.tsv")}
