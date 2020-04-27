def fill_with_headlines(query_results):
    """Add extra line for result. It is to avoid Jinja2 mess with namespaces"""

    last_channel = ""
    modified_results = []

    for item in query_results:
        if last_channel != item.channel:
            modified_results.append({'title': item.channel,
                                     'channel': '##',
                                     'published': '',
                                     'url': '',
                                     'id': ''})
        modified_results.append(item)
        last_channel = item.channel
    return modified_results

