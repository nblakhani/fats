from flask import Flask
from config import config
from app.extensions import db, migrate, cors, scheduler

def create_app(env="default"):
    app = Flask(__name__)
    app.config.from_object(config[env])

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Register blueprints
    from app.routes.staff import bp as staff_bp
    from app.routes.clients import bp as clients_bp
    from app.routes.visits import bp as visits_bp
    from app.routes.action_items import bp as action_bp
    from app.routes.follow_ups import bp as followup_bp
    from app.routes.reports import bp as reports_bp

    app.register_blueprint(staff_bp,     url_prefix="/api/staff")
    app.register_blueprint(clients_bp,   url_prefix="/api/clients")
    app.register_blueprint(visits_bp,    url_prefix="/api/visits")
    app.register_blueprint(action_bp,    url_prefix="/api/action-items")
    app.register_blueprint(followup_bp,  url_prefix="/api/follow-ups")
    app.register_blueprint(reports_bp,   url_prefix="/api/reports")

    import os
    from flask import send_from_directory

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @app.route("/api/health")
    def health():
        return {"status": "ok", "service": "fieldforce-api"}

    @app.route("/")
    @app.route("/dashboard")
    def dashboard():
        return send_from_directory(root_dir, "dashboard.html")

    @app.route("/pwa/")
    @app.route("/pwa/index.html")
    def pwa_index():
        return send_from_directory(os.path.join(root_dir, "pwa"), "index.html")

    @app.route("/pwa/<path:filename>")
    def pwa_static(filename):
        return send_from_directory(os.path.join(root_dir, "pwa"), filename)

    # Start scheduler
    from app.services.scheduler import register_jobs
    with app.app_context():
        register_jobs(app)
    if not scheduler.running:
        scheduler.start()

    return app
