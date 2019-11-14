from flask import Flask
from ..config import FLASK_CONFIG
app = Flask(__name__)
app.config.from_mapping(**FLASK_CONFIG)
# from_object(FLASK_CONFIG)

# from .routes import task

from .routes.api_stat import main as api_stat_routes
app.register_blueprint(api_stat_routes,url_prefix='/api/stat')

from .routes.api_up import main as api_up_routes
app.register_blueprint(api_up_routes,url_prefix='/api/up')

from .routes.api_video import main as api_video_routes
app.register_blueprint(api_video_routes,url_prefix='/api/video')

from .routes.api_login import main as api_login_routes
app.register_blueprint(api_login_routes,url_prefix='/api/login')

from .routes.api_task import main as api_task_routes
app.register_blueprint(api_task_routes,url_prefix='/api/task')

from .routes.api_online import main as api_online_routes
app.register_blueprint(api_online_routes,url_prefix='/api/online')

from .routes.api_activity import main as api_activity_routes
app.register_blueprint(api_activity_routes,url_prefix='/api/activity')

from .routes.api_scraper import main as api_scraper_routes
app.register_blueprint(api_scraper_routes,url_prefix='/s')