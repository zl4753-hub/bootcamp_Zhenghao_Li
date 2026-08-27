# Deployment and handoff plan

- Risk Analytics owns feature definitions, model evaluation, quarterly retraining, and `reports/model_metrics.json`.
- Data Engineering owns the daily Yahoo ingestion, schema validation, freshness, and replay from `data/raw/`.
- Platform on-call owns the Flask service, latency/error dashboards, deployment, and rollback.
- The portfolio risk manager owns the 50% review threshold and approves any business-policy change.
- Start locally with `python -m src.pipeline` through the notebook or `python app.py` after a model exists.
- Check `/health` and `/metadata`, then run the API example documented in `README.md`.
- Follow `docs/monitoring_plan.md` for thresholds and first-response actions.
- Follow `docs/orchestration_plan.md` for task dependencies, checkpoints, and retries.
- Record incidents and model changes in repository issues; attach metrics, model date, decision, and owner.
- Roll back by restoring the prior versioned `model/model.pkl` and last valid processed snapshot.
