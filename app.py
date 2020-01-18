from quart import Quart

app = Quart(__name__,
            template_folder="templates",
            )
VER = "0.3.1A.2"


@app.route('/')
async def index():
    return f"Awasu News Browser {VER}"

app.run()


