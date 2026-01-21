REQUIRED_FIELDS = {"id", "cv_text", "jd_text", "label", "language", "source", "meta"}


def validate_canonical_record(record: dict) -> list[str]:
    missing = sorted(REQUIRED_FIELDS - set(record.keys()))
    errors = []
    if missing:
        errors.append(f"missing_fields:{','.join(missing)}")
    if record.get("label") not in {None, "strong_match", "partial_match", "mismatch"}:
        errors.append("invalid_label")
    if record.get("language") not in {"en", "de", "unknown"}:
        errors.append("invalid_language")
    return errors
