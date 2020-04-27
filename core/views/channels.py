from quart import Blueprint, render_template

from core.data.manipulation import timestamp_to_normal_date
from core.database.operations import dbo
from core.database.results_manipulations import fill_with_headlines

bp_channels = Blueprint('channels', __name__)
bp_channels.add_app_template_filter(timestamp_to_normal_date)


@bp_channels.route('/channels/')
async def all_channels():
    # last = fill_with_headlines(dbo.latest_n_articles_sort_by_channel(100))
    # return await render_template('skeleton/base.html', articles_data=last)
    return "All channels"


@bp_channels.route('/channels/show/<name>')
async def show(name):
    articles_in_channel = fill_with_headlines(dbo.from_channel(channel_name=name))
    channel_info = dbo.channel_description(channel_name=name)

    return await render_template('views/channels/show.html',
                                 articles_data=articles_in_channel,
                                 channel_description=channel_info)


@bp_channels.route('/channels/info/<name>')
async def info(name):
    # articles_in_channel = fill_with_headlines(dbo.from_channel(channel_name=name)
    # return await render_template('skeleton/base.html', articles_data=articles_in_channel)
    return f"Info about {name}"
