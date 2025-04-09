import reflex as rx
import random
import asyncio
from typing import List

GRID_SIZE = 30
INITIAL_INTERVAL = 500


class GameState(rx.State):
    grid: List[List[int]] = [
        [0] * GRID_SIZE for _ in range(GRID_SIZE)
    ]
    is_running: bool = False
    interval: int = INITIAL_INTERVAL
    generation: int = 0

    def _count_live_neighbors(
        self, row: int, col: int
    ) -> int:
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                r, c = (row + i, col + j)
                if (
                    0 <= r < GRID_SIZE
                    and 0 <= c < GRID_SIZE
                    and (self.grid[r][c] == 1)
                ):
                    count += 1
        return count

    def _next_generation(self):
        new_grid = [
            [0] * GRID_SIZE for _ in range(GRID_SIZE)
        ]
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                live_neighbors = self._count_live_neighbors(
                    r, c
                )
                if (
                    self.grid[r][c] == 1
                    and live_neighbors < 2
                ):
                    new_grid[r][c] = 0
                elif self.grid[r][c] == 1 and (
                    live_neighbors == 2
                    or live_neighbors == 3
                ):
                    new_grid[r][c] = 1
                elif (
                    self.grid[r][c] == 1
                    and live_neighbors > 3
                ):
                    new_grid[r][c] = 0
                elif (
                    self.grid[r][c] == 0
                    and live_neighbors == 3
                ):
                    new_grid[r][c] = 1
                else:
                    new_grid[r][c] = self.grid[r][c]
        self.grid = new_grid

    @rx.event
    def toggle_cell(self, row: int, col: int):
        """Toggles the state of a cell if the simulation is not running."""
        if not self.is_running:
            new_grid = [list(row) for row in self.grid]
            new_grid[row][col] = 1 - new_grid[row][col]
            self.grid = new_grid

    @rx.event
    def start_stop(self):
        """Starts or stops the simulation."""
        self.is_running = not self.is_running
        if self.is_running:
            return GameState.simulation_step

    @rx.event
    def clear_grid(self):
        """Clears the grid and stops the simulation."""
        self.grid = [
            [0] * GRID_SIZE for _ in range(GRID_SIZE)
        ]
        self.is_running = False
        self.generation = 0

    @rx.event
    def randomize_grid(self):
        """Randomizes the grid and stops the simulation."""
        self.grid = [
            [
                random.choice([0, 1])
                for _ in range(GRID_SIZE)
            ]
            for _ in range(GRID_SIZE)
        ]
        self.is_running = False
        self.generation = 0

    @rx.event(background=True)
    async def simulation_step(self):
        """Performs one step of the simulation and schedules the next."""
        while True:
            async with self:
                if not self.is_running:
                    return
                self._next_generation()
                self.generation += 1
            yield
            current_interval = 0.0
            is_still_running = False
            async with self:
                current_interval = self.interval / 1000.0
                is_still_running = self.is_running
            if not is_still_running:
                return
            await asyncio.sleep(current_interval)

    @rx.event
    def set_interval(self, value: str):
        """Sets the simulation interval."""
        try:
            new_interval = int(value)
            if 50 <= new_interval <= 2000:
                self.interval = new_interval
            else:
                print(
                    f"Interval {new_interval} out of range (50-2000)"
                )
        except ValueError:
            print(f"Invalid interval value: {value}")
            pass