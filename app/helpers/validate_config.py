def validate_config(config):
    missing_keys = []

    if config.get("campus_id") is None:
        missing_keys.append("campus_id")
    if config.get("inactive_duration_in_months") is None:
        missing_keys.append("inactive_duration_in_months")
    if (
        config.get(
            "intra",
            {},
        ).get("client")
        is None
    ):
        missing_keys.append("intra client")
    if (
        config.get(
            "intra",
            {},
        ).get("secret")
        is None
    ):
        missing_keys.append("intra secret")
    if (
        config.get(
            "intra",
            {},
        ).get("uri")
        is None
    ):
        missing_keys.append("intra uri")
    if (
        config.get(
            "intra",
            {},
        ).get("endpoint_base_url")
        is None
    ):
        missing_keys.append("intra endpoint_base_url")
    if (
        config.get(
            "homemaker",
            {},
        ).get("admin-token")
        is None
    ):
        missing_keys.append("homeamker admin-token")
    if (
        config.get(
            "homemaker",
            {},
        ).get("base-url")
        is None
    ):
        missing_keys.append("homeamker base-url")

    if missing_keys:
        print(
            f"Missing required configuration keys: {", ".join(missing_keys)}. Exiting program."
        )
        exit(1)
