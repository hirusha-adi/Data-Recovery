import sys
import click


from config import Constant
from config import Messages

from modules import (
    ChromiumRecovery, WebHistoryRecovery, WebBookmarksRecovery,  # Browser
    NetworkInfoRecovery, WifiPasswordRecovery,  # Network
    SystemInfoRecovery,  # System
    DiscordRecovery  # Applications
)


@click.group()
@click.option("--silent", "-s", is_flag=True, help="Silent Mode - No Console Output")
@click.option("--verbose", "-v", is_flag=True, help="Verbose - Display all operations")
@click.option("--log", "-l", is_flag=True, help="Enable logging to a file")
@click.pass_context
def cli(ctx: click.Context, silent: bool, verbose: bool, log: bool):
    """Data Recovery | Built by @hirusha-adi"""
    ctx.ensure_object(dict)

    # Global settings
    Constant.Args.silent = silent
    Constant.Args.verbose = verbose
    Constant.Args.log = log

    # Default to verbose mode if no flags are provided
    if not (silent or verbose or log):
        Constant.Args.silent = False
        Constant.Args.verbose = True
        Constant.Args.log = True


@cli.command(name="all", help="Recover everything")
@click.pass_context
def recover_all(ctx: click.Context):
    """Recover all available data"""
    ctx.invoke(recover_browser, passwords=True, history=True, bookmarks=True)
    ctx.invoke(recover_network, wifi=True, info=True)
    ctx.invoke(recover_system)
    ctx.invoke(recover_discord, discord=True)


@cli.command(name="browser", help="Recover browser data")
@click.option("--passwords", "-p", is_flag=True, help="Recover browser passwords")
@click.option("--history", "-h", is_flag=True, help="Recover browser history")
@click.option("--bookmarks", "-b", is_flag=True, help="Recover browser bookmarks")
@click.pass_context
def recover_browser(ctx: click.Context, passwords: bool, history: bool, bookmarks: bool):
    """Recover browser-related data"""
    if not (passwords or history or bookmarks):
        click.echo("No browser recovery options specified. Use --help for more info.")
        sys.exit()

    if passwords:
        ChromiumRecovery().run()
    if history:
        WebHistoryRecovery().run()
    if bookmarks:
        WebBookmarksRecovery().run()


@cli.command(name="network", help="Recover network data")
@click.option("--wifi", "-nw", is_flag=True, help="Recover saved WiFi passwords")
@click.option("--info", "-ni", is_flag=True, help="Recover network information")
@click.pass_context
def recover_network(ctx: click.Context, wifi: bool, info: bool):
    """Recover network-related data"""
    if not (wifi or info):
        click.echo("No network recovery options specified. Use --help for more info.")
        sys.exit()

    if wifi:
        WifiPasswordRecovery().run()
    if info:
        NetworkInfoRecovery().run()


@cli.command(name="system", help="Recover system information")
@click.pass_context
def recover_system(ctx: click.Context):
    """Recover system information"""
    SystemInfoRecovery().run()


@cli.command(name="apps", help="Recover application data")
@click.option("--discord", "-ad", is_flag=True, help="Recover Discord tokens")
@click.pass_context
def recover_discord(ctx: click.Context, discord: bool):
    """Recover application-related data"""
    if discord:
        DiscordRecovery().run()
    else:
        click.echo("No application recovery options specified. Use --help for more info.")
        sys.exit()


if __name__ == "__main__":
    cli()
    Messages.cexit()
