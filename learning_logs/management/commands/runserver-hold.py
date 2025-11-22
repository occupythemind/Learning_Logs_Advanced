from django.core.management.base import BaseCommand
from django.utils import autoreload
from django.conf import settings
import os
from daphne.cli import CommandLineInterface


class Command(BaseCommand):
    help = "Run the Django ASGI server using Daphne with autoreload (disabled in production)."

    def add_arguments(self, parser):
        parser.add_argument(
            "addrport",
            nargs="?",
            default="127.0.0.1:8000",
            help="Optional address:port, default 127.0.0.1:8000",
        )

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_log.settings")  # The project name

        addrport = options["addrport"]
        if ":" in addrport:
            host, port = addrport.split(":")
        else:
            host, port = "127.0.0.1", addrport

        def run_daphne():
            argv = [
                "-b", host,
                "-p", port,
                "learning_log.asgi:application",    # The ASGI app
            ]
            self.stdout.write(self.style.SUCCESS(f"Starting Daphne on {host}:{port} …"))
            CommandLineInterface().run(argv)

        # Toggle autoreload based on DEBUG or env var
        if getattr(settings, "DEBUG", False):
            self.stdout.write(self.style.WARNING("Autoreload is ENABLED (Development Mode)"))
            autoreload.run_with_reloader(run_daphne)
        else:
            self.stdout.write(self.style.WARNING("Autoreload is DISABLED (Production Mode)"))
            run_daphne()
