def google_search_result_formatter(search_response):
    return '\n'.join([
        f'{search_result.get("title")}: {search_result.get("link")}' for search_result in search_response
    ])
