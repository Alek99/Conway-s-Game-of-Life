import reflex as rx
from app.components.grid_display import grid_display
from app.components.controls import controls


def index() -> rx.Component:
    """The main page for Conway's Game of Life."""
    return rx.el.div(
        rx.el.h1(
            "Conway's Game of Life",
            class_name="text-5xl font-extrabold text-center my-10 text-black",
        ),
        controls(),
        rx.el.div(
            grid_display(),
            class_name="flex justify-center items-center mt-8",
        ),
        class_name="min-h-screen bg-lime-300 flex flex-col items-center pt-10 px-4",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index, route="/")