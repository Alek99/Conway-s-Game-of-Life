import reflex as rx
from typing import List
from app.states.game_state import GameState, GRID_SIZE


def cell(row: int, col: int) -> rx.Component:
    """Renders a single cell in the grid in neo-brutalist style."""
    return rx.el.div(
        on_click=lambda: GameState.toggle_cell(row, col),
        key=f"cell-{row}-{col}-{GameState.grid[row][col]}",
        class_name=rx.cond(
            GameState.grid[row][col] == 1,
            "w-4 h-4 border border-black bg-black cursor-pointer",
            "w-4 h-4 border border-black bg-white cursor-pointer",
        ),
    )


def grid_row(
    row_data: List[int], row_index: int
) -> rx.Component:
    """Renders a row of cells."""
    return rx.el.div(
        rx.foreach(
            rx.Var.range(GRID_SIZE),
            lambda col_index: cell(row_index, col_index),
        ),
        class_name="flex flex-row",
    )


def grid_display() -> rx.Component:
    """Renders the entire game grid with a neo-brutalist border."""
    return rx.el.div(
        rx.foreach(
            rx.Var.range(GRID_SIZE),
            lambda row_index: grid_row(
                GameState.grid[row_index], row_index
            ),
        ),
        class_name="flex flex-col border-2 border-black bg-gray-100",
    )