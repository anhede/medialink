"""
MESSAGES
Define UI/help messages as constants
"""

# Intent messages
INTENT_TARGET_FILMS = "Generating film library in {film_target}"
INTENT_TARGET_SHOWS = "Generating show library in {show_target}"
INTENT_GENERATE_FILM = "Generating link for film: {film}"

# Help messages
HELP_TARGET_FILMS = "Optional target for films"
HELP_TARGET_SHOWS = "Optional target for shows"
HELP_DRY_RUN = "Show what would be done without making any changes"
HELP_PURGE = "Remove any existing links present in SOURCE from TARGET"
HELP_VERBOSE = "Print verbose output"

# Error messages
ERROR_NO_TARGET = "Either TARGET or at least one of --target-films or \
--target-shows must be provided."
ERROR_TARGET_CONFLICT = (
    "TARGET and --target-films/--target-shows are mutually exclusive."
)
