"""
Programing by J.acek S.krzypacz

Main

----
It is starting place for view data and all operations

"""
from core.settings.initialcheck import runchecks
runchecks()

from quart import Quart
from quart import render_template
from quart import url_for

from core.views.articles import bp_articles
from core.views.channels import bp_channels
from core.views.categories import bp_categories
from core.data.manipulation import data_info

VER = "0.3.1A.5"

app = Quart(__name__,
            template_folder="templates",
            )

app.register_blueprint(bp_articles)
app.register_blueprint(bp_channels)
app.register_blueprint(bp_categories)


@app.route('/')
async def index():
    art_path = url_for("articles.articles_index")
    source_info = data_info()
    return await render_template("views/startpage/startpage.html",
                                 ver=VER,
                                 source_created=source_info['created_data'],
                                 debug_mode=source_info['is_debug'],
                                 )

app.run()


