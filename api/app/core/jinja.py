from fastapi.templating import Jinja2Templates

from app.core.paths import TEMPLATES_DIR

email_templates = Jinja2Templates(
    directory=TEMPLATES_DIR / "email",
)

# Or use Jinja template engine (Environment) directly
# env = Environment(
#     loader=FileSystemLoader(TEMPLATES_DIR / "email"),
#     autoescape=select_autoescape(["html", "htm", "xml"]),
# )

# template = env.get_template("auth/password_reset.html")
