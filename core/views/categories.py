from typing import List

from quart import Blueprint, render_template
from core.database.operations import dbo
from core.database.results_manipulations import fill_with_headlines

bp_categories = Blueprint('categories', __name__)
# bp.add_app_template_filter(filter)
main_folders: List[str] = sorted(dbo.main_folders())


@bp_categories.route('/categories')
async def categories_index():
    last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(100))
    return await render_template('views/categories/articles_in_categories.html',
                                 articles_data=last,
                                 main_folders=main_folders,
                                 folder_names='Latest news')


@bp_categories.route('/categories/folders/names/<names>')
async def articles_from_folders_names(names):
    articles = dbo.from_folder_names(names)
    return await render_template('views/categories/articles_in_categories.html',
                                 articles_data=articles,
                                 folders_names=names,
                                 main_folders=main_folders)
