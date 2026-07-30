def is_ignored(title, ignored):

    title = title.lower()

    return any(word in title for word in ignored)


def is_matching(job, keywords, banks):

    title = job.get("title", "").lower()

    company = job.get("company", "").lower()

    tags = " ".join(job.get("tags", [])).lower()

    return (
        any(word in title for word in keywords)
        or any(word in tags for word in keywords)
        or any(bank["name"].lower() in company for bank in banks)
    )
