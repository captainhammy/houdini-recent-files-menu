"""Initialize package callbacks."""

# Third Party
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniSessionEvent

# Houdini Recent Files Menu
from houdini_recent_files_menu import callbacks

# Register callback function.
CallbackManager().add_callback(
    HoudiniSessionEvent.SceneLoaded, callbacks.add_current_hip_to_recent_files, skip_no_ui=True
)
CallbackManager().add_callback(
    HoudiniSessionEvent.AfterSceneSave, callbacks.add_current_hip_to_recent_files, skip_no_ui=True
)
