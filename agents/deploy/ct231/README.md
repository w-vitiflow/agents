# CT 231 deployment snapshot

Canonical copies of the live Hermes stacks on pimox5 CT 231. Apply on the LXC:

```bash
# ERP stack
cp docker-compose.hermes.yml /root/hermes/docker-compose.yml
# Grok stack
cp docker-compose.hermes-grok.yml /root/hermes/docker-compose.grok.yml
```

## LXC bind mounts (pimox5 host)

```
mp0: /opt/homelab-agentic,mp=/opt/homelab-agentic
mp1: /mnt/seagate-storage/nextcloud/data/Hermes-agent/files/ai-brain,mp=/opt/ai-brain
```

## Paths inside CT 231

| Path | Purpose |
|------|---------|
| `/root/hermes/` | ERP compose + `.env` |
| `/root/.hermes` | ERP agent data volume |
| `/root/hermes/docker-compose.grok.yml` | Grok compose |
| `/root/.hermes-grok` | Grok agent data volume |
| `/opt/vitiflow` | Git clone of this repo |
| `/opt/ai-brain` | Obsidian vault (Nextcloud) |
| `/opt/homelab-agentic` | Homelab harness |

## Ports

| Container | Dashboard | API |
|-----------|-----------|-----|
| `hermes` (ERP) | 9119 | 8642 |
| `hermes-grok` | 9120 | 8643 |

## Healthcheck fix (2026-07-17)

ERP `hermes` was **unhealthy** while the gateway ran fine: the healthcheck used unquoted `grep -q Gateway is running`, so grep treated `is` and `running` as filenames. Fixed with `grep -Fq 'Gateway is running'`.