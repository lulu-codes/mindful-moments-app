# ascii_art.py

from rich_pyfiglet import RichFiglet
from rich.console import Console

console = Console()

# Use for welcome app banner and ASCII art

custom_welcome_banner = RichFiglet(
    "Welcome to Mindful Moments App", # Rendered text welcome message
    font="ansi_shadow",
    colors=["light_sky_blue1", "medium_purple", "light_steel_blue", "plum2"],
    animation="smooth_strobe",
    fps=5,
)

# FUNCTION TO DISPLAY CUSTOM WELCOME BANNER
def display_welcome_banner():
    console.print(custom_welcome_banner)


# display_welcome_banner()