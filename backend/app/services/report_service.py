from __future__ import annotations

from app.schemas.recruitment import EvaluationCriteria, RankedRecommendation, RecommendationReport


DISCLOSURE = (
    "These recommendations are AI-assisted decision support based on the supplied job criteria and candidate data. "
    "A recruiter must review and approve all recommendations before they are used in a hiring process."
)


class ReportService:
    def create_report(self, criteria: EvaluationCriteria, shortlist: list[RankedRecommendation]) -> RecommendationReport:
        if not shortlist:
            summary = f"No candidates were recommended for {criteria.title}. Add approved candidate data and rerun."
        else:
            lines = [
                f"Shortlist generated for {criteria.title} with {len(shortlist)} candidate(s).",
                "",
                "Top recommendations:",
            ]
            lines.extend(
                f"{item.rank}. {item.display_name} - {item.fit_label} fit ({item.overall_score}/100). "
                f"{item.recommendation_rationale}"
                for item in shortlist[:5]
            )
            summary = "\n".join(lines)

        return RecommendationReport(summary_markdown=summary, disclosure=DISCLOSURE)
