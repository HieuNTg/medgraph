# FAERS Auto-Refresh Pipeline Design

**Phase 5.1 Design Document**
**Status**: Design Phase
**Target Release**: v0.3.0 (Q3 2026)

---

## Executive Summary

Design for automated OpenFDA FAERS adverse event data refresh pipeline. Provides incremental updates to interaction evidence counts without manual intervention. Core challenge: balancing data freshness (risk of stale adverse event records) with API rate limiting and infrastructure cost.

---

## Problem Statement

**Current State**:
- `openfda.py`: Synchronous, blocking API client with file-based cache
- `refresh_pipeline.py`: Manual refresh orchestrator supporting "weekly" schedule
- Freshness threshold: 7 days (hard-coded)
- No deduplication or quality validation
- No incremental queries — fetches full dataset each time

**Gaps**:
1. Manual refresh trigger required; no autonomous daemon
2. Identical queries repeated; cache key collision risk
3. FAERS data quality untested (duplicates, malformed reactions)
4. Weekly schedule may miss critical safety signals
5. No monitoring/alerting for stale data

---

## Proposed Architecture

### High-Level Flow

```
┌─ Scheduler (APScheduler / systemd timer) ─┐
│                                            │
├─> Incremental FAERS Query                  │
│   ├─ Fetch events added since last_run     │
│   └─ Parse + dedup reactions               │
│                                            │
├─> Data Quality Pipeline                    │
│   ├─ Reject malformed reactions            │
│   ├─ Novelty check (is_new_reaction)       │
│   └─ Quality score (normalized_count)      │
│                                            │
├─> Upsert + Evidence Aggregation            │
│   ├─ Update interaction record (count)     │
│   └─ Log refresh metadata                  │
│                                            │
└─> Failure Handling                         │
    ├─ Retry logic (exponential backoff)     │
    ├─ Partial commit (don't rollback)       │
    └─ Sentry alert on 3 consecutive fails   │
```

### Architecture Decision: Task Queue vs Daemon

**Option A: APScheduler In-Process (Chosen for v0.3.0)**
- Pros: No external service dependency; works in containerized deployment
- Cons: Process restart = missed jobs; single-threaded scheduling
- Use case: MVP with <5 min latency tolerance

**Option B: Celery + Redis/RabbitMQ (v0.4.0 upgrade path)**
- Pros: Horizontal scaling; decoupled job processing; worker resilience
- Cons: Operational complexity; extra infra
- Use case: Multi-instance production deployment

**Chosen**: Option A for v0.3.0, with abstracted job interface to support Option B later.

---

## Data Requirements

### FAERS Query Strategy

**Incremental Query**:
```sql
SELECT event_id, primary_id, meddra_term, count
FROM openfda/drug/event.json
WHERE receivedate >= last_refresh_timestamp
  AND patient.drug IN (known_drug_list)
LIMIT 1000
```

**Parameters**:
- `receivedate`: Date FAERS server received report (more stable than reactiondate)
- `limit`: Tune via load tests; 1000-10000 range typical
- Pagination: Use OpenFDA's `skip` parameter for large result sets

### Deduplication Strategy

**Problem**: Identical reactions reported multiple times for same drug pair.

**Solution**: Hash-based dedup
```python
def dedupe_key(event):
    return hashlib.md5(
        f"{drug_a}:{drug_b}:{reaction}".encode()
    ).hexdigest()
```

Store in memory during refresh; check before upsert.

### Quality Scoring

**Reaction Quality Metrics**:
1. **Normalized Count**: `count / max_count_in_batch` (0–1)
2. **MedDRA Hierarchy**: Prefer Preferred Terms (PT) over High-Level Terms (HLT); penalize non-coded reactions
3. **Temporal Signal**: Reactions with sharp increase (3x+ month-over-month) = higher signal score

**Formula**:
```
quality_score = (normalized_count * 0.5) + (meddra_level * 0.3) + (signal_trend * 0.2)
```

Discard reactions with quality_score < 0.1.

---

## API Design

### New Endpoints

#### 1. Trigger Manual Refresh
```http
POST /api/admin/refresh
Content-Type: application/json
X-API-Key: <admin_key>

{
  "sources": ["openfda"],
  "force": false
}

Response: 200 OK
{
  "job_id": "refresh_20260324_1705",
  "status": "queued",
  "scheduled_at": "2026-03-24T17:05:00Z"
}
```

#### 2. Refresh Status & History
```http
GET /api/admin/refresh/jobs?limit=10

Response: 200 OK
[
  {
    "job_id": "refresh_20260324_1705",
    "status": "completed",
    "sources_attempted": ["openfda"],
    "sources_succeeded": ["openfda"],
    "records_updated": 247,
    "timestamp": "2026-03-24T17:05:00Z",
    "errors": {}
  },
  ...
]
```

#### 3. Freshness Status (Public)
```http
GET /api/health/freshness

Response: 200 OK
{
  "last_refresh": "2026-03-24T10:00:00Z",
  "last_successful_source": "openfda",
  "days_since_refresh": 0.29,
  "is_fresh": true,
  "next_scheduled_refresh": "2026-03-25T02:00:00Z",
  "data_version": "42"
}
```

### CLI Commands

```bash
# Trigger refresh manually
python -m medgraph.cli refresh --source openfda --force

# View scheduled jobs
python -m medgraph.cli refresh --list-jobs

# Cancel pending job
python -m medgraph.cli refresh --cancel <job_id>

# View refresh history
python -m medgraph.cli refresh --history --limit 20
```

---

## Implementation Details

### 1. Scheduling Service

**File**: `medgraph/data/refresh_service.py`

```python
class RefreshService:
    def __init__(self, store: GraphStore, config: RefreshConfig):
        self.scheduler = APScheduler()
        self.store = store
        self.config = config
        self._jobs_history: deque = deque(maxlen=100)

    def start(self):
        """Initialize scheduler and add jobs."""
        self.scheduler.add_job(
            self._refresh_openfda,
            'cron',
            hour=2,  # 2 AM UTC daily
            minute=0,
            id='refresh_openfda_daily'
        )
        self.scheduler.start()

    async def _refresh_openfda(self):
        """Execute FAERS refresh job."""
        job_id = f"refresh_{datetime.now().isoformat()[:10]}_{uuid4().hex[:8]}"
        try:
            result = self.pipeline.refresh_batch_openfda_incremental()
            self._jobs_history.append({
                'job_id': job_id,
                'status': 'completed',
                'records_updated': result.records_updated,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            sentry_sdk.capture_message(
                f"FAERS refresh completed: {result.records_updated} records",
                level="info"
            )
        except Exception as e:
            self._jobs_history.append({
                'job_id': job_id,
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            sentry_sdk.capture_exception(e)
```

### 2. Incremental Query Client

**File**: `medgraph/data/openfda.py` (extend)

```python
class OpenFDAClient:
    def search_adverse_events_incremental(
        self,
        drug_names: list[str],
        since: datetime,
        limit: int = 5000,
    ) -> list[AdverseEvent]:
        """
        Query FAERS for events added since timestamp.
        Uses receivedate >= timestamp filter.
        """
        query_parts = [
            f'patient.drug.openfda.generic_name:"{name}"'
            for name in drug_names
        ]
        query = "+AND+".join(query_parts)
        query += f' AND receivedate:[{since.isoformat()} TO *]'

        params = {
            "search": query,
            "count": "patient.reaction.reactionmeddrapt.exact",
            "limit": limit,
        }

        data = self._get(f"{OPENFDA_BASE}/event.json", params)
        return self._parse_and_validate_events(data, drug_names)

    def _parse_and_validate_events(
        self,
        data: dict,
        drug_names: list[str]
    ) -> list[AdverseEvent]:
        """Parse + quality-score reactions."""
        results = data.get("results", [])
        max_count = max((r.get("count", 0) for r in results), default=1)
        events = []
        seen_hashes = set()

        for item in results:
            term = item.get("term", "Unknown")
            count = item.get("count", 0)

            # Quality filtering
            if not self._is_valid_reaction(term):
                continue

            quality_score = (count / max_count) * 0.5
            quality_score += self._meddra_score(term) * 0.3
            if quality_score < 0.1:
                continue

            # Deduplication
            key_hash = hashlib.md5(
                f"{':'.join(sorted(drug_names))}:{term}".encode()
            ).hexdigest()
            if key_hash in seen_hashes:
                continue
            seen_hashes.add(key_hash)

            events.append(AdverseEvent(
                id=f"FAERS-{key_hash[:12]}",
                drug_ids=drug_names,
                reaction=term,
                count=count,
                quality_score=quality_score,
                seriousness="unknown",
                source_url="https://api.fda.gov/drug/event.json"
            ))

        return events
```

### 3. Refresh Pipeline Extension

**File**: `medgraph/data/refresh_pipeline.py` (extend)

```python
def refresh_batch_openfda_incremental(self) -> RefreshResult:
    """
    Incremental refresh: query for events added since last_refresh.
    Smarter than full re-fetch.
    """
    last_refresh = self._get_metadata("last_refresh_timestamp")
    if not last_refresh:
        # First run — query last 30 days
        since = datetime.now(timezone.utc) - timedelta(days=30)
    else:
        since = datetime.fromisoformat(last_refresh)

    result = RefreshResult(
        sources_attempted=["openfda"],
        timestamp=datetime.now(timezone.utc).isoformat()
    )

    # Get list of known drug pairs from current DB
    all_drugs = [d.name for d in self._store.get_all_drugs()]

    try:
        client = OpenFDAClient()
        # Batch drugs into groups to avoid query size limits
        for batch in self._batch_drugs(all_drugs, batch_size=5):
            events = client.search_adverse_events_incremental(
                batch,
                since=since,
                limit=5000
            )
            for event in events:
                self._store.upsert_adverse_event(event)
            result.records_updated += len(events)

        result.sources_succeeded.append("openfda")
        self._persist_refresh_metadata(result)
        logger.info(f"Incremental FAERS refresh: {result.records_updated} records")

    except Exception as e:
        result.sources_failed.append("openfda")
        result.errors["openfda"] = str(e)
        logger.exception("Incremental FAERS refresh failed")

    return result
```

---

## Estimated Effort

| Component | Effort | Notes |
|-----------|--------|-------|
| Incremental query logic | 8h | FAERS API query refinement + testing |
| Dedup + quality scoring | 6h | Hash-based dedup; quality metrics |
| APScheduler integration | 4h | Cron job setup; graceful shutdown |
| Job history/status endpoints | 4h | Admin API; job state tracking |
| Tests (unit + integration) | 8h | Mock FAERS API; edge cases |
| **Total** | **30h** | ~3–4 days dev + 1 day review |

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Rate limiting from OpenFDA (240 req/min) | High | Implement exponential backoff; batch queries; cache aggressively |
| Data quality issues (malformed reactions) | Medium | Quality scoring; reject reactions with term length > 200 chars |
| Missed safety signals (weekly stale window) | High | Move to 2x/week after v0.3.0; configure Sentry alert if no refresh > 10 days |
| Process restart loses scheduled jobs | Medium | Use APScheduler + persistent job store (SQLAlchemy backend); fallback to manual trigger |
| Database write contention | Low | Batch inserts; use `PRAGMA journal_mode=WAL` (already in SQLite config) |

---

## Testing Strategy

### Unit Tests
- Reaction quality scoring with edge cases (empty reactions, nulls)
- Deduplication hash collisions
- Incremental timestamp filtering

### Integration Tests
- Mock OpenFDA API responses; verify incremental query construction
- Test graceful degradation if API unavailable
- Refresh job history persistence

### Load Tests
- Run incremental refresh on full drug DB (500+ drugs); measure API calls
- Measure refresh latency; target < 2 minutes for 500 drug batch

---

## Future Work (v0.4.0+)

1. **Celery Queue Migration**: Move to distributed task queue for multi-instance deployments
2. **Advanced Signal Detection**: Statistical anomaly detection (SPRT, CUSUM) for safety signal emergence
3. **Feedback Loop**: User-reported adverse events → confidence score adjustment
4. **Caching Strategy**: Redis-backed cache for frequently-queried drug pairs

---

## References

- OpenFDA FAERS API: https://open.fda.gov/data/faers/
- FAERS Quarterly Update Schedule: https://open.fda.gov/data/
- APScheduler Docs: https://apscheduler.readthedocs.io/
- MedDRA Hierarchy: https://www.meddra.org/
