from happypanda.common import constants, message, exceptions, utils
from happypanda.core.services import Service

def get_error(code: int, id: int, ctx=None):
    """
    Get error

    Args:
        code: error code, refer to ...
        id:

    Returns:
        an error message object
    """
    return message.Message("works")


def get_version():
    """
    Get version of components: 'core', 'db' and 'torrent'

    Returns:
        a dict of component: list of major, minor, patch
    """
    vs = dict(
        core=list(constants.version),
        db=list(constants.version_db),
        torrent=(0, 0, 0)
    )
    return message.Identity("version", vs)


def install_plugin(plugin_id: str, ctx=None):
    """
    Install a plugin

    Args:
        plugin_id: UUID of plugin

    Returns:
        an error message object
    """
    return message.Message("works")


def uninstall_plugin(plugin_id: str, ctx=None):
    """
    Uninstall a plugin

    Args:
        plugin_id: UUID of plugin

    Returns:
        an error message object
    """
    return message.Message("works")


def list_plugins(ctx=None):
    """
    Get a list of available plugin information

    Args:
        an error message object
    """
    return message.Message("works")

def _command_msg(ids):
    for x in ids:
        if not Service.get_command(x):
            raise exceptions.APIError(utils.this_function(), "Command with ID '{}' does not exist".format(x))

def get_command_state(command_ids: list):
    """
    Get state of command

    Args:
        command_ids: list of command ids

    Returns:
        { command_id : state }

    """

    _command_msg(command_ids)

    states = {}

    for i in command_ids:
        states[i] = Service.get_command(i).state.name

    return message.Identity('command_state', states)

def get_command_progress(command_ids: list):
    """
    Get progress of command in percent

    Args:
        command_ids: list of command ids

    Returns:
        { command_id : progress }

    """
    return message.Message("works")

def stop_command(command_ids: list):
    """
    Stop command from running

    Args:
        command_ids: list of command ids

    Returns:
        { command_id : state }

    """
    _command_msg(command_ids)

    states = {}

    for i in command_ids:
        cmd = Service.get_command(i)
        cmd.stop()
        states[i] = cmd.state.name

    return message.Identity('command_state', states)

def start_command(command_ids: list):
    """
    Start running a command

    Args:
        command_ids: list of command ids

    Returns:
        { command_id : state }

    """
    _command_msg(command_ids)

    states = {}

    for i in command_ids:
        cmd = Service.get_command(i)
        cmd.start()
        states[i] = cmd.state.name

    return message.Identity('command_state', states)

def get_command_error(command_ids: list):
    """
    Get error raised during command runtime

    Args:
        command_ids: list of command ids

    Returns:
        { command_id : error }

    """
    return message.Message("works")

def undo_command(command_ids: list):
    """
    Undo a command

    .. Note:
        Only select commands are undoable

    Args:
        command_ids: list of command ids

    Returns:
        { command_id : state }

    """
    return message.Message("works")