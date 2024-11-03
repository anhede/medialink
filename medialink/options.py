class Options:
    """Command line options"""

    def __init__(self, verbose: bool, dry_run: bool):
        self.verbose = verbose or dry_run  # verbose is implied by dry_run
        self.dry_run = dry_run
        self.require_film_year = True  # TODO: make this an option
