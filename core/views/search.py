from quart import Blueprint, render_template
from core.database.operations import dbo
from core.database.results_manipulations import fill_with_headlines
bp_articles = Blueprint('search', __name__)
# bp.add_app_template_filter(filter)


@bp_articles.route('/search/')
async def search_index():
    # last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(100))
    # return await render_template('skeleton/base.html', articles_data=last)
    return "Search main"


@bp_articles.route('/search/agents')
async def agents():
    # last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(100))
    # return await render_template('skeleton/base.html', articles_data=last)
    return "Awasu Search Agents"


@bp_articles.route('/search/awasu')
async def awasu_db_search(query):
    # last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(100))
    # return await render_template('skeleton/base.html', articles_data=last)
    return f"Awasu Search by API Call Q:{query}"


@bp_articles.route('/search/agents')
async def by_keywords(phrase):
    # last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(100))
    # return await render_template('skeleton/base.html', articles_data=last)
    return f"Search by phrase {phrase}"
