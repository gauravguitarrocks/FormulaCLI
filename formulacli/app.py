"""
    formulacli.app
    ~~~~~~~~~~~~~~

    Controls the context objects and main loop.

"""

from sys import exit
from typing import Dict, Any

from colorama import Style

from formulacli import contexts
from formulacli.exceptions import ExitException
from formulacli.helpers import clear_screen


class FormulaCLI:
    def __init__(self) -> None:
        """
        Context Manager.
        Changes context based on state change of Context type objects.
        :rtype: None
        """
        self.state: Dict[str, Any] = {
            "ctx": contexts.MainContext,
            "args": {}
        }

    def run(self) -> None:
        try:
            while True:
                try:
                    ctx = self.state["ctx"]
                    if hasattr(ctx, '__call__'):
                        ctx = ctx(**self.state["args"])
                        ctx.add_to_history()
                    clear_screen()
                    ctx.render()
                    if ctx.state['next_ctx']:
                        self.state["ctx"] = ctx.state['next_ctx']
                        self.state["args"] = ctx.state['next_ctx_args']
                except KeyboardInterrupt:
                    ctx = self.state["ctx"]
                    if ctx.block_render:
                        self.close()
                    else:
                        ctx.block_render = True
                        print(Style.RESET_ALL)
                        self.state["ctx"] = ctx

        except ExitException:
            self.close("Graciously exiting.")
        except EOFError:
            self.close()

    @staticmethod
    def close(msg: str = "Graciously exiting.") -> None:
        print(msg)
        exit()
