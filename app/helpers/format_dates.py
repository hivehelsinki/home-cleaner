from datetime import datetime
from dateutil.relativedelta import relativedelta


def make_range(config):
    end_at = datetime.now().strftime("%Y-%m-%d")
    begin_at = (
        datetime.now() - relativedelta(months=config["inactive_duration_in_months"])
    ).strftime("%Y-%m-%d")
    return f"{begin_at},{end_at}"


def make_date_payload(config):
    inactive_duration_in_months = config["inactive_duration_in_months"]
    today = datetime.now()
    end_at = today.strftime("%Y-%m-%d")
    begin_at = (today - relativedelta(months=inactive_duration_in_months)).strftime(
        "%Y-%m-%d"
    )

    return {"begin_at": begin_at, "end_at": end_at}
