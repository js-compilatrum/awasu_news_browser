from quart import Blueprint, render_template
from core.database.operations import dbo
from core.database.results_manipulations import fill_with_headlines
bp_selected = Blueprint('selected', __name__)
# bp.add_app_template_filter(filter)


@bp_selected.route('/selected/')
async def selected_index():
    # last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(100))
    # return await render_template('skeleton/base.html', articles_data=last)
    return "Selected main"


