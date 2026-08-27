"""Stakeholder-ready figures and report-table exports."""

from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


COLORS = {"primary": "#2457A7", "risk": "#D1495B", "neutral": "#6B7280", "positive": "#2A9D8F"}


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def create_figures(featured, scored, scenarios, subgroups, coefficients, reports_dir: Path) -> list[Path]:
    """Create consistent, self-contained charts for the risk manager."""
    sns.set_theme(style="whitegrid")
    image_dir = reports_dir / "images"
    paths = []

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(featured["date"], featured["adjusted_close"], color=COLORS["primary"], label="SPY adjusted close")
    ax1.set_ylabel("Adjusted close (USD)")
    ax1.set_xlabel("Date")
    ax2 = ax1.twinx()
    ax2.plot(featured["date"], featured["volatility_20"] * np.sqrt(252), color=COLORS["risk"], alpha=0.65, label="20-day annualized volatility")
    ax2.set_ylabel("Annualized volatility")
    ax1.set_title("SPY Price and Rolling Risk Regimes")
    lines = ax1.lines + ax2.lines
    ax1.legend(lines, [line.get_label() for line in lines], loc="upper left")
    path = image_dir / "price_and_volatility.png"; _save(fig, path); paths.append(path)

    cm = pd.crosstab(scored["target_high_vol_next"].astype(int), scored["predicted_class"].astype(int)).reindex(index=[0,1], columns=[0,1], fill_value=0)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax, xticklabels=["Normal", "High risk"], yticklabels=["Normal", "High risk"])
    ax.set_xlabel("Predicted next-day regime"); ax.set_ylabel("Actual next-day regime"); ax.set_title("Out-of-Sample Risk Classification")
    path = image_dir / "confusion_matrix.png"; _save(fig, path); paths.append(path)

    fig, ax = plt.subplots(figsize=(8, 5))
    melted = scenarios.melt("scenario", value_vars=["f1", "roc_auc"], var_name="metric", value_name="score")
    sns.barplot(data=melted, x="scenario", y="score", hue="metric", ax=ax, palette=[COLORS["primary"], COLORS["positive"]])
    ax.set_ylim(0, 1); ax.set_xlabel("Definition of high-volatility day"); ax.set_ylabel("Out-of-sample score"); ax.set_title("Sensitivity to the Risk-Threshold Assumption"); ax.tick_params(axis="x", rotation=10)
    path = image_dir / "scenario_sensitivity.png"; _save(fig, path); paths.append(path)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    sns.barplot(data=subgroups, x="market_regime", y="f1", ax=axes[0], color=COLORS["primary"])
    sns.barplot(data=subgroups, x="market_regime", y="roc_auc", ax=axes[1], color=COLORS["positive"])
    axes[0].set_title("F1 by trend regime"); axes[1].set_title("ROC-AUC by trend regime")
    for ax in axes: ax.set_ylim(0, 1); ax.tick_params(axis="x", rotation=10); ax.set_xlabel("")
    fig.suptitle("Subgroup Stability Check")
    path = image_dir / "subgroup_performance.png"; _save(fig, path); paths.append(path)

    top = coefficients.head(8).sort_values("standardized_coefficient")
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = [COLORS["risk"] if value > 0 else COLORS["primary"] for value in top["standardized_coefficient"]]
    ax.barh(top["feature"], top["standardized_coefficient"], color=colors)
    ax.axvline(0, color="black", linewidth=1); ax.set_xlabel("Standardized logistic coefficient"); ax.set_title("Features Associated with Next-Day High Volatility")
    path = image_dir / "feature_coefficients.png"; _save(fig, path); paths.append(path)
    return paths
