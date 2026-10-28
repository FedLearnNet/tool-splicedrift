# splicedrift

Fits Bayesian models of age-associated splicing changes with SpliceDrift and exports results and plots.

## Runtime inputs

Supply input files according to the schemas in `app.yml`.

## Inputs and outputs

### Inputs

| Name | Type | Description |
| --- | --- | --- |
| `junction_counts` | TSV | TSV with columns: event_id, sample_id, k, N, age, group (optional) |

### Outputs

| Name | Type | Description |
| --- | --- | --- |
| `results` | CSV | Summary table with alpha_prime and beta_prime per (event, group) |
| `scatter_plot` | IMAGE | Scatter plot of alpha_prime vs beta_prime |

## Configuration

| Name | Default | Description |
| --- | --- | --- |
| `draws` | `200` | Number of posterior draws per chain |
| `tune` | `200` | Number of tuning (warm-up) steps per chain |
| `chains` | `1` | Number of MCMC chains |
| `max_refits` | `0` | Number of automatic refits on convergence failure |
| `target_accept` | `0.9` | NUTS target acceptance probability |
| `min_total` | `5` | Minimum total reads N per sample |

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
# Set APP_ID and platform URLs before connecting.
python main.py
```

The Docker base image provides the FL-Net API. `requirements.txt` lists additional
runtime dependencies; `requirements-dev.txt` includes the API for local development.
Runtime datasets and trained models must be supplied separately; see `data/README.md`.

Build with `docker build -t tool-splicedrift .`.
