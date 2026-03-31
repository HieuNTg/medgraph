"""
PubMed literature enrichment agent for MEDGRAPH.

Uses NCBI E-utilities API (free, no key required for <3 req/sec) to search
for peer-reviewed evidence on drug-drug interactions.

NCBI E-utilities docs: https://www.ncbi.nlm.nih.gov/books/NBK25499/
"""

from __future__ import annotations

import logging
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from urllib.parse import urlencode
from urllib.request import urlopen

if TYPE_CHECKING:
    from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

# NCBI E-utilities base URL
_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Rate limit: max 3 requests/second without API key
_REQUEST_INTERVAL = 0.34  # seconds between requests (~3/sec)

# Interaction-related keywords for relevance scoring
_RELEVANCE_KEYWORDS = [
    "interaction",
    "interactions",
    "drug-drug",
    "adverse",
    "toxicity",
    "effect",
    "contraindication",
    "pharmacokinetic",
    "metabolism",
    "inhibit",
    "induc",
    "substrate",
    "cyp450",
    "enzyme",
]


@dataclass
class PubMedArticle:
    """Structured PubMed article result."""

    pmid: str
    title: str
    abstract: str
    pub_date: str
    journal: str
    relevance_score: float = 0.0

    def to_dict(self) -> dict:
        return {
            "pmid": self.pmid,
            "title": self.title,
            "abstract": self.abstract,
            "pub_date": self.pub_date,
            "journal": self.journal,
            "relevance_score": self.relevance_score,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{self.pmid}/",
        }


def _score_relevance(title: str, abstract: str) -> float:
    """
    Score relevance of an article based on keyword presence in title/abstract.

    Returns a float in [0.0, 1.0].
    """
    text = (title + " " + abstract).lower()
    hits = sum(1 for kw in _RELEVANCE_KEYWORDS if kw in text)
    # Title matches are worth double
    title_hits = sum(1 for kw in _RELEVANCE_KEYWORDS if kw in title.lower())
    total_hits = hits + title_hits
    max_possible = len(_RELEVANCE_KEYWORDS) * 2
    return min(round(total_hits / max_possible, 3), 1.0)


def _fetch_url(url: str, params: dict, timeout: int = 10) -> str:
    """Perform a simple GET request using urllib (no extra deps required)."""
    full_url = f"{url}?{urlencode(params)}"
    with urlopen(full_url, timeout=timeout) as resp:  # noqa: S310
        return resp.read().decode("utf-8")


class PubMedAgent:
    """
    Search PubMed for drug-drug interaction evidence using NCBI E-utilities.

    Rate-limited to <3 requests/second to stay within NCBI's free-tier limits.
    """

    def __init__(self, max_results: int = 10, timeout: int = 10) -> None:
        self.max_results = max_results
        self.timeout = timeout
        self._last_request: float = 0.0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def search_interactions(self, drug_a: str, drug_b: str) -> list[dict]:
        """
        Search PubMed for published evidence on a drug-drug interaction.

        Args:
            drug_a: First drug name.
            drug_b: Second drug name.

        Returns:
            List of dicts with keys: pmid, title, abstract, pub_date,
            journal, relevance_score, url.
        """
        pmids = self._esearch(drug_a, drug_b)
        if not pmids:
            return []

        articles = self._efetch(pmids)
        # Sort by relevance
        articles.sort(key=lambda a: a.relevance_score, reverse=True)
        return [a.to_dict() for a in articles]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _rate_limit(self) -> None:
        """Ensure we don't exceed 3 requests/second."""
        elapsed = time.monotonic() - self._last_request
        if elapsed < _REQUEST_INTERVAL:
            time.sleep(_REQUEST_INTERVAL - elapsed)
        self._last_request = time.monotonic()

    def _esearch(self, drug_a: str, drug_b: str) -> list[str]:
        """
        Use esearch to get PMIDs for drug-drug interaction articles.

        Query: "{drug_a}"[Title/Abstract] AND "{drug_b}"[Title/Abstract]
               AND "drug interaction"[MeSH Terms]
        """
        query = (
            f'"{drug_a}"[Title/Abstract] AND "{drug_b}"[Title/Abstract] '
            'AND "drug interaction"[MeSH Terms]'
        )
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": str(self.max_results),
            "retmode": "xml",
            "usehistory": "n",
        }
        try:
            self._rate_limit()
            xml_text = _fetch_url(_ESEARCH_URL, params, self.timeout)
            root = ET.fromstring(xml_text)
            pmids = [id_elem.text for id_elem in root.findall(".//Id") if id_elem.text]
            logger.debug("esearch %s+%s: %d PMIDs found", drug_a, drug_b, len(pmids))
            return pmids
        except Exception as exc:
            logger.warning("PubMed esearch failed for %s+%s: %s", drug_a, drug_b, exc)
            return []

    def _efetch(self, pmids: list[str]) -> list[PubMedArticle]:
        """
        Fetch full article metadata (title, abstract, date, journal) by PMIDs.
        """
        if not pmids:
            return []

        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "rettype": "abstract",
        }
        try:
            self._rate_limit()
            xml_text = _fetch_url(_EFETCH_URL, params, self.timeout)
            return self._parse_pubmed_xml(xml_text)
        except Exception as exc:
            logger.warning("PubMed efetch failed: %s", exc)
            return []

    def _parse_pubmed_xml(self, xml_text: str) -> list[PubMedArticle]:
        """Parse PubMed efetch XML into PubMedArticle objects.

        Uses defusedxml when available to prevent XML entity attacks.
        """
        articles: list[PubMedArticle] = []
        try:
            try:
                import defusedxml.ElementTree as SafeET

                root = SafeET.fromstring(xml_text)
            except ImportError:
                root = ET.fromstring(xml_text)
        except ET.ParseError as exc:
            logger.warning("Failed to parse PubMed XML: %s", exc)
            return []

        for article_elem in root.findall(".//PubmedArticle"):
            pmid_elem = article_elem.find(".//PMID")
            pmid = pmid_elem.text if pmid_elem is not None else "unknown"

            # Title
            title_elem = article_elem.find(".//ArticleTitle")
            title = title_elem.text or "" if title_elem is not None else ""
            # Strip XML tags from title (may contain <i>, <b> etc.)
            title = (
                ET.tostring(title_elem, encoding="unicode", method="text")
                if title_elem is not None
                else ""
            )

            # Abstract: concatenate all AbstractText sections
            abstract_parts = []
            for ab_elem in article_elem.findall(".//AbstractText"):
                label = ab_elem.get("Label", "")
                text = ET.tostring(ab_elem, encoding="unicode", method="text")
                if label:
                    abstract_parts.append(f"{label}: {text}")
                else:
                    abstract_parts.append(text)
            abstract = " ".join(abstract_parts).strip()

            # Journal
            journal_elem = article_elem.find(".//Journal/Title")
            journal = journal_elem.text or "" if journal_elem is not None else ""

            # Publication date — try Year/Month/Day then MedlineDate
            year = article_elem.findtext(".//PubDate/Year", default="")
            month = article_elem.findtext(".//PubDate/Month", default="")
            day = article_elem.findtext(".//PubDate/Day", default="")
            if year:
                pub_date = f"{year}-{month or '01'}-{day or '01'}"
            else:
                pub_date = article_elem.findtext(".//MedlineDate", default="unknown")

            score = _score_relevance(title, abstract)
            articles.append(
                PubMedArticle(
                    pmid=pmid,
                    title=title,
                    abstract=abstract,
                    pub_date=pub_date,
                    journal=journal,
                    relevance_score=score,
                )
            )

        return articles


def enrich_interaction(
    store: "GraphStore",
    drug_a_id: str,
    drug_b_id: str,
    agent: Optional[PubMedAgent] = None,
) -> list[dict]:
    """
    Fetch PubMed evidence for a drug pair and store as adverse events / evidence.

    Args:
        store: GraphStore instance.
        drug_a_id: ID of first drug.
        drug_b_id: ID of second drug.
        agent: Optional pre-configured PubMedAgent.

    Returns:
        List of PubMed article dicts that were found.
    """
    if agent is None:
        agent = PubMedAgent()

    # Resolve drug names from IDs
    with store._connect() as conn:
        row_a = conn.execute("SELECT name FROM drugs WHERE id=?", (drug_a_id,)).fetchone()
        row_b = conn.execute("SELECT name FROM drugs WHERE id=?", (drug_b_id,)).fetchone()

    if not row_a or not row_b:
        logger.warning("enrich_interaction: drug not found (%s, %s)", drug_a_id, drug_b_id)
        return []

    drug_a_name = row_a[0]
    drug_b_name = row_b[0]

    articles = agent.search_interactions(drug_a_name, drug_b_name)
    if not articles:
        return []

    # Store top results as evidence sources linked to the interaction
    for article in articles[:5]:
        try:
            from medgraph.graph.models import EvidenceSource

            ev = EvidenceSource(
                id=f"PUBMED-{article['pmid']}",
                interaction_id=f"{drug_a_id}-{drug_b_id}",
                source="pubmed",
                description=article["title"][:500],
                case_count=None,
                url=article["url"],
            )
            store.upsert_evidence_source(ev)
        except Exception as exc:
            logger.debug("Failed to store PubMed evidence %s: %s", article["pmid"], exc)

    logger.info(
        "PubMed enrichment: %d articles for %s+%s",
        len(articles),
        drug_a_name,
        drug_b_name,
    )
    return articles
