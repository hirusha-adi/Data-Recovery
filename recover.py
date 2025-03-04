import sys
import click


from config import Constant
from config import Messages

from modules import (
    ChromiumRecovery, WebHistoryRecovery, WebBookmarksRecovery,  # Browser
    NetworkInfoRecovery, WifiPasswordRecovery,  # Network
    SystemInfoRecovery,  # System
    DiscordRecovery, MinecraftRecovery, EpicGamesRecovery, UplayRecovery, PostgresSqlRecovery  # Applications
)


@click.group()
@click.option("--silent", "-s", is_flag=True, help="Silent Mode - No Console Output")
@click.option("--verbose", "-v", is_flag=True, help="Verbose - Display all operations")
@click.option("--log", "-l", is_flag=True, help="Enable logging to a file")
@click.pass_context
def cli(ctx: click.Context, silent: bool, verbose: bool, log: bool) -> None:
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
def recover_all(ctx: click.Context) -> None:
    """Recover all available data"""
    ctx.invoke(recover_browser, passwords=True, history=True, bookmarks=True)
    ctx.invoke(recover_network, wifi=True, info=True)
    ctx.invoke(recover_system)
    ctx.invoke(recover_apps, discord=True, minecraft=True, epicgames=True, uplay=True)

@cli.command(name="browser", help="Recover browser data")
@click.option("--passwords", "-p", is_flag=True, help="Recover browser passwords")
@click.option("--history", "-h", is_flag=True, help="Recover browser history")
@click.option("--bookmarks", "-b", is_flag=True, help="Recover browser bookmarks")
@click.pass_context
def recover_browser(ctx: click.Context, passwords: bool, history: bool, bookmarks: bool) -> None:
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
@click.option("--wifi", "-w", is_flag=True, help="Recover saved WiFi passwords")
@click.option("--info", "-i", is_flag=True, help="Recover network information")
@click.pass_context
def recover_network(ctx: click.Context, wifi: bool, info: bool) -> None:
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
def recover_system(ctx: click.Context) -> None:
    """Recover system information"""
    SystemInfoRecovery().run()

@cli.command(name="apps", help="Recover application data")
@click.option("--discord", "-d", is_flag=True, help="Recover Discord tokens")
@click.option("--minecraft", "-mc", is_flag=True, help="Recover Minecraft accounts")
@click.option("--epicgames", "-eg", is_flag=True, help="Recover Epic Games accounts")
@click.option("--uplay", "-up", is_flag=True, help="Recover Uplay accounts")
@click.option("--postgresql", "-psql", is_flag=True, help="Recover PostgresSQL accounts")
@click.pass_context
def recover_apps(ctx: click.Context, discord: bool, minecraft: bool, epicgames: bool, uplay: bool, postgresql: bool) -> None:
    """Recover application-related data"""
    if not (discord or minecraft or epicgames or uplay):
        click.echo("No application recovery options specified. Use --help for more info.")
        sys.exit()

    if discord:
        DiscordRecovery().run()
    if minecraft:
        MinecraftRecovery().run()
    if epicgames:
        EpicGamesRecovery().run()
    if uplay:
        UplayRecovery().run()
    if postgresql:
        PostgresSqlRecovery().run()

if __name__ == "__main__":
    cli()
    Messages.cexit()
