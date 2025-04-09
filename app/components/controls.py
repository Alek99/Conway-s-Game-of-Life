import reflex as rx
from app.states.game_state import GameState

button_base_style = "px-5 py-2 border-2 border-black font-bold shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] active:shadow-[1px_1px_0px_0px_rgba(0,0,0,1)] transition-shadow duration-100"
button_disabled_style = "px-5 py-2 border-2 border-gray-400 text-gray-500 bg-gray-300 cursor-not-allowed"


def controls() -> rx.Component:
    """Renders the control buttons and generation counter in neo-brutalist style."""
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.cond(
                    GameState.is_running, "Stop", "Start"
                ),
                on_click=GameState.start_stop,
                class_name=rx.cond(
                    GameState.is_running,
                    f"{button_base_style} bg-red-500 text-white hover:bg-red-600",
                    f"{button_base_style} bg-green-500 text-white hover:bg-green-600",
                ),
            ),
            rx.el.button(
                "Clear",
                on_click=GameState.clear_grid,
                disabled=GameState.is_running,
                class_name=rx.cond(
                    GameState.is_running,
                    button_disabled_style,
                    f"{button_base_style} bg-yellow-400 text-black hover:bg-yellow-500",
                ),
            ),
            rx.el.button(
                "Randomize",
                on_click=GameState.randomize_grid,
                disabled=GameState.is_running,
                class_name=rx.cond(
                    GameState.is_running,
                    button_disabled_style,
                    f"{button_base_style} bg-blue-500 text-white hover:bg-blue-600",
                ),
            ),
            class_name="flex gap-5 mb-6 justify-center",
        ),
        rx.el.div(
            rx.el.label(
                "Speed (ms): ",
                class_name="text-black font-bold mr-2",
            ),
            rx.el.input(
                type="number",
                min=50,
                max=2000,
                step=50,
                default_value=GameState.interval.to_string(),
                key=GameState.interval.to_string(),
                on_blur=GameState.set_interval,
                disabled=GameState.is_running,
                class_name=rx.cond(
                    GameState.is_running,
                    "border-2 border-gray-400 px-2 py-1 w-24 bg-gray-300 text-gray-500 cursor-not-allowed",
                    "border-2 border-black px-2 py-1 w-24 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-400",
                ),
            ),
            class_name="flex items-center justify-center mb-6",
        ),
        rx.el.div(
            rx.el.p(
                "Generation: ",
                rx.el.span(
                    GameState.generation,
                    class_name="font-black text-2xl",
                ),
                class_name="text-lg text-black font-semibold",
            ),
            class_name="text-center",
        ),
        class_name="flex flex-col items-center p-6",
    )