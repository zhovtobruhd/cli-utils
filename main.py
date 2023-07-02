import click
import curses

from HexViewApp import HexViewApp

@click.group(chain=True)
@click.pass_context
def cli(ctx):
    pass
    

@cli.command('hexview', help='HEX viewer')
@click.option('-p', '--path', type=click.Path(), required=True, help='Path to file')
@click.pass_context
def cmd_hexview(ctx, path):
    app = HexViewApp()
    curses.wrapper(app.run, path=path)


if __name__ == '__main__':
    cli()
