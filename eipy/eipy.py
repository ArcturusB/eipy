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

def _frameinfo_to_record(frameinfo):
    ''' Convert a inspect.FrameInfo object to a record tuple, as expected by
    ultratb printers.
    '''
    frame = frameinfo.frame
    file = frameinfo.filename
    lnum = frameinfo.lineno
    func = frameinfo.function
    lines = frameinfo.code_context
    if lines is None:
        lines = []
    context = len(lines)
    if context > 1:
        index = 1
    else:
        index = 0
    return frame, file, lnum, func, lines, index

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

def open_shell(ipshell, stack_depth=2, context=3):
    ''' Open an embedded ipython shell, displaying info message and traceback.

    Parameters
    ==========
    ipshell : IPython.terminal.embed.InteractiveShellEmbed
        The embedded IPython shell to open.
    stack_depth : int (default: 2)
        How far to go back in the depth. This should be set so that we go back
        to the point where the user prompts the shell opening.
        The default value is 2 because it is the one that should be used when
        the user accesses directly this function through
        `eipy.eipy.open_shell(ipshell)`.
    context : int (default: 3)
        Number of lines of context to display when entering the shell.
    '''

    # get the stack and current frame
    stack = inspect.stack(context=context)
    stack = stack[stack_depth - 1:] # stack up to before the user called eipy
    frameinfo = stack[0] # frame where the user called eipy

    vt = ultratb.VerboseTB(include_vars=False)

    # display where the user called eipy, as well as a the context
    msg = 'Stopped at '
    msg += vt.format_record(*_frameinfo_to_record(frameinfo))

    # Open shell going back to the level where ipsh() was called
    ipshell(msg, stack_depth=stack_depth)
