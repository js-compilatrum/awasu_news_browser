from quart import Blueprint, render_template
from core.database.operations import dbo
from core.database.results_manipulations import fill_with_headlines
bp_analytics = Blueprint('analytics', __name__)
# bp.add_app_template_filter(filter)


@bp_analytics.route('/analytics/')
async def analytics_index():
    # last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(100))
    # return await render_template('skeleton/base.html', articles_data=last)
    return "Analytics index"


@bp_analytics.route('/analytics/trends')
async def trends_index():
    # last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(100))
    # return await render_template('skeleton/base.html', articles_data=last)
    return "Analytics list of available trend by categories"


@bp_analytics.route('/analytics/trends/topics')
async def analytics_index():
    # last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(100))
    # return await render_template('skeleton/base.html', articles_data=last)
    return "Analytics trend topics"


@bp_analytics.route('/analytics/categories')
async def analytics_index():
    # last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(100))
    # return await render_template('skeleton/base.html', articles_data=last)
    return "Analytics Spacy categories like GPE"

