from prometheus_client import Counter, Histogram

tickets_total = Counter(
    "resolve_tickets_total",
    "Total tickets processed"
)

auto_approved_total = Counter(
    "resolve_auto_approved_total",
    "Total auto approved tickets"
)

human_review_total = Counter(
    "resolve_human_review_total",
    "Total tickets sent to human review"
)

rejected_total = Counter(
    "resolve_rejected_total",
    "Total rejected tickets"
)

no_relevant_info_total = Counter(
    "resolve_no_relevant_info_total",
    "Total tickets with no relevant information"
)

response_time_seconds = Histogram(
    "resolve_response_time_seconds",
    "Ticket processing time"
)