from quart import Blueprint, render_template
from core.database.operations import dbo
from core.database.results_manipulations import fill_with_headlines
from core.settings.config import LATEST_ARTICLES_NUMBER

bp_articles = Blueprint('articles', __name__)
# bp.add_app_template_filter(filter)


@bp_articles.route('/articles/')
async def articles_index():
    last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(LATEST_ARTICLES_NUMBER))
    return await render_template('views/articles/articles.html', articles_data=last)
