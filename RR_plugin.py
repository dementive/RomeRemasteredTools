import sublime
import sublime_plugin
import re
from .Utilities.game_data import GameData


GameData = GameData()


def show_hover_docs(view, point, scope, collection):
    style = ""
    color = ""
    if scope == "keyword.command":
        color = "128, 26, 0"
    elif scope == "string.condition":
        color = "123, 123, 0"
    elif scope == "storage.type.event":
        color = "0, 122, 153"
    elif scope == "entity.name.console.command":
        color = "80, 135, 44"

    style = f"""
        body {{
            font-family: system;
            margin: 0;
            padding: 0.35rem;
            border: 0.15rem solid rgb({color});
            background-color: rgb(10, 10, 10);
        }}
        p {{
            font-size: 1.0rem;
            margin: 0;
        }}
    """

    item = view.substr(view.word(point))
    if item in collection:
        desc = collection[item]
        hoverBody = """
            <body id="rr-body">
                <style>%s</style>
                <p>%s</p>
            </body>
        """ % (
            style,
            desc,
        )

        view.show_popup(
            hoverBody,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=1024,
        )
        return


class RomeRemasteredScriptHoverListener(sublime_plugin.EventListener):
    def on_hover(self, view, point, hover_zone):
        if not view:
            return

        try:
            if view.syntax().name == "Rome Total War":
                pass
            else:
                return
        except AttributeError:
            return

        if view.match_selector(point, "keyword.command"):
            show_hover_docs(view, point, "keyword.command", GameData.command_dict)

        if view.match_selector(point, "string.condition"):
            show_hover_docs(view, point, "string.condition", GameData.conditions_dict)

        if view.match_selector(point, "storage.type.event"):
            show_hover_docs(view, point, "storage.type.event", GameData.event_dict)

        if view.match_selector(point, "entity.name.console.command"):
            show_hover_docs(view, point, "entity.name.console.command", GameData.console_command_dict)


class RomeRemasteredCompletionsEventListener(sublime_plugin.EventListener):
    def __init__(self):
        self.show_events = False
        self.show_events_views = []
        self.show_conditions = False
        self.show_conditions_views = []
        self.show_commands = False
        self.show_commands_views = []

    def reset_shown(self):
        self.show_events = False
        self.show_conditions = False
        self.show_commands = False

    def on_deactivated_async(self, view):
        """
        Remove field states when view loses focus
        if cursor was in a field in the old view but not the new view the completions will still be accurate
        save the id of the view so it can be readded when it regains focus
        """
        vid = view.id()
        if self.show_events:
            self.show_events = False
            self.show_events_views.append(vid)
        if self.show_conditions:
            self.show_conditions = False
            self.show_conditions_views.append(vid)
        if self.show_commands:
            self.show_commands = False
            self.show_commands_views.append(vid)

    def on_activated_async(self, view):
        vid = view.id()
        if vid in self.show_events_views:
            self.show_events = True
            self.show_events_views.remove(vid)
        if vid in self.show_conditions_views:
            self.show_conditions = True
            self.show_conditions_views.remove(vid)
        if vid in self.show_commands_views:
            self.show_commands = True
            self.show_commands_views.remove(vid)

    def on_query_completions(self, view, prefix, locations):
        if not view:
            return None

        try:
            if view.syntax().name != "Rome Total War":
                return None
        except AttributeError:
            return None

        if self.show_conditions:
            conditions = GameData.conditions_dict
            conditions = sorted(conditions)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "C", "Condition"),
                        details=GameData.conditions_dict[key].split("Description:")[1].split("<br>")[0],
                    )
                    for key in sorted(conditions)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )

        if self.show_commands:
            commands = GameData.console_command_dict
            commands = sorted(commands)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "C", "Console Command"),
                        details=GameData.console_command_dict[key].split("Description:")[1].split("<br>")[0],
                    )
                    for key in sorted(commands)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )

        if self.show_events:
            events = GameData.event_dict
            events = sorted(events)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "E", "Event"),
                        details=GameData.event_dict[key].split("Event:")[1].split("<br>")[0],
                    )
                    for key in sorted(events)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
            )

    def check_for_simple_completions(self, view, point):
        self.reset_shown()

        if view.substr(point) == "=":
            return

        line = view.substr(view.line(point))

        command = "console_command"
        r = re.search(command, line)
        if r:
            idx = line.index(command) + view.line(point).a + len(command) + 1
            if idx == point:
                self.show_commands = True
                view.run_command("auto_complete")

        command = "monitor_event"
        r = re.search(command, line)
        if r:
            idx = line.index(command) + view.line(point).a + len(command) + 1
            if idx == point:
                self.show_events = True
                view.run_command("auto_complete")

        command = "monitor_conditions"
        r = re.search(command, line)
        if r:
            idx = line.index(command) + view.line(point).a + len(command) + 1
            if idx == point:
                self.show_conditions = True
                view.run_command("auto_complete")

    def on_selection_modified_async(self, view):
        if not view:
            return

        try:
            if view.syntax().name != "Rome Total War":
                return
        except AttributeError:
            return

        if len(view.sel()) == 1:
            self.check_for_simple_completions(view, view.sel()[0].a)
