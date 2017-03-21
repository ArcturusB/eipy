#!/usr/bin/env python

import inspect
import traceback
import sys

from IPython.terminal.embed import InteractiveShellEmbed
from IPython.terminal.prompts import Prompts, Token
from IPython.core import ultratb
from traitlets.config.loader import Config

# Drop ANSI formatting if ansi_codes is not found
try:
    from ansi_codes import format as ansi_format
except (SyntaxError, ImportError):
    def ansi_format(string, **kwargs):
        return string

def create_shell():
    ''' Create an embedded ipython shell.
    '''
    # Messages displayed when entering and exiting the shell
    msg_colour = 'yellow'
    banner_title = '** Entering embedded shell:'
    banner_content = (
        'Hit Ctrl-D to exit this shell and resume execution.',
        'Use %kill_embedded to deactivate future shells.',
        )
    exit_msg = '** Leaving embedded shell.'
    # format these messages
    banner_content = '\n'.join(banner_content)
    banner_title = ansi_format(banner_title, fg=msg_colour, style='bold')
    banner_content = ansi_format(banner_content, fg=msg_colour)
    exit_msg = ansi_format(exit_msg, fg=msg_colour, style='bold')
    banner_msg = '\n{}\n{}'.format(banner_title, banner_content)

    # Configure the prompt
    class CustomPrompt(Prompts):

        def in_prompt_tokens(self, cli=None):
            return [
                (Token.Prompt, 'In <'),
                (Token.PromptNum, str(self.shell.execution_count)),
                (Token.Prompt, '>: '),
                ]

        def out_prompt_tokens(self):
            return [
                (Token.OutPrompt, 'Out<'),
                (Token.OutPromptNum, str(self.shell.execution_count)),
                (Token.OutPrompt, '>: '),
                ]

    # Register configuration
    c = Config()
    c.TerminalInteractiveShell.prompts_class = CustomPrompt

    # Mirror configuration in IPython_config.py
    # FIXME: this should really load config file
    c.InteractiveShellApp.matplotlib = 'auto'
    c.InteractiveShell.colors = 'Linux'
    c.TerminalInteractiveShell.editing_mode = 'vi'

    # Create embedded shell
    ipshell = InteractiveShellEmbed(
        config=c,
        banner1=banner_msg,
        exit_msg=exit_msg,
        )

    return ipshell

def open_shell(ipshell):
    ''' Open an embedded ipython shell, displaying info message and traceback.
    '''

    # Display traceback info. If some exception has been raised, show nicely
    # format traceback using ultratb. If no exception has been raised, show
    # stack trace.
    frame = inspect.currentframe().f_back
    msg = 'Stopped at {0.f_code.co_filename} at line {0.f_lineno}'.format(frame)
    msg += '\n'
    etype, evalue, tb = sys.exc_info()
    if tb:
        vt = ultratb.VerboseTB()
        msg += vt.text(etype, evalue, tb)
    else:
        stack = traceback.format_stack()
        stack = stack[:-1]
        msg += '\n'
        msg += '\n'.join(stack)

    # Open shell going back to the level where ipsh() was called
    ipshell(msg, stack_depth=2)
