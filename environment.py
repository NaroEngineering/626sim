import numpy as np
import random
from entities import Predator, Prey, Food


class Environment:
    def __init__(self, size, n_predators, n_prey, n_food, pred_hunger, prey_hunger, food_rate):
        self.size = size
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]
        self.entity_counts = {"Predator": [], "Prey": [], "Food": []}
        self.time_steps = []

        self.pred_hunger = pred_hunger
        self.prey_hunger = prey_hunger
        self.food_rate = food_rate

        for _ in range(n_predators):
            self.add_entity(Predator, self.pred_hunger)

        for _ in range(n_prey):
            self.add_entity(Prey, self.prey_hunger)

        for _ in range(n_food):
            self.add_entity(Food)

    def add_entity(self, entity_type, hunger=None):
        x, y = np.random.randint(0, self.size, 2)
        entity = entity_type(x, y, hunger) if hunger is not None else entity_type(x, y)
        self.cells[x][y].entities.append(entity)

    def get_nearby_entities(self, x, y):
        nearby_entities = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new_x, new_y = (x + dx) % self.size, (y + dy) % self.size
                nearby_entities.extend(self.cells[new_x][new_y].entities)
        return nearby_entities

    def update(self):
        new_cells = [[Cell() for _ in range(self.size)] for _ in range(self.size)]  # Prepare empty new cells

        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                for entity in cell.entities:
                    if not entity.alive:
                        continue

                    # Get movement directions
                    dx, dy = entity.move()

                    # Calculate new cell coordinates
                    new_x, new_y = (i + dx) % self.size, (j + dy) % self.size

                    if isinstance(entity, Predator):
                        for prey in self.cells[new_x][new_y].entities:
                            if isinstance(prey, Prey):
                                prey.kill()  # The predator eats the prey
                                offspring = entity.eat()  # The predator's hunger increases and might reproduce
                                if offspring is not None:
                                    new_cells[new_x][new_y].entities.append(offspring)
                                break
                    elif isinstance(entity, Prey):
                        for food in self.cells[new_x][new_y].entities:
                            if isinstance(food, Food):
                                food.kill()  # The prey eats the food
                                offspring = entity.eat()  # The prey's hunger increases and might reproduce
                                if offspring is not None:
                                    new_cells[new_x][new_y].entities.append(offspring)
                                break

                    # Move the entity to the new cell
                    new_cells[new_x][new_y].entities.append(entity)

                    # Kill the entity if its hunger reaches 0
                    if isinstance(entity, (Predator, Prey)):  # Only decrement hunger for Predator and Prey
                        entity.hunger -= 1
                        if entity.hunger <= 0:
                            entity.kill()

        self.cells = new_cells

        n_food = int(10 * self.food_rate)  # Adjust the number of food based on the food rate
        self.add_food(n_food)
        
        for entity_type in self.entity_counts.keys():
            if entity_type == "Food":
                self.entity_counts[entity_type].append(sum(isinstance(e, eval(entity_type)) for row in self.cells for cell in row for e in cell.entities))
            else:
                self.entity_counts[entity_type].append(sum(isinstance(e, eval(entity_type)) and e.alive for row in self.cells for cell in row for e in cell.entities))

        self.time_steps.append(self.time_steps[-1] + 1 if self.time_steps else 0)

        for entity in cell.entities:
            old_position = entity.position
            entity.update(cell)
            new_position = entity.position

            # If the entity has moved, remove it from the current cell's entities
            if old_position != new_position:
                cell.entities.remove(entity)


    def add_food(self, n_food):
        spawn_square_radius = self.size // 4  # Half the side length of the spawn square
        spawn_random_radius = spawn_square_radius // 10  # Randomness radius is 10% of the square's side length
        mid_point = self.size // 2  # The center of the environment

        # Four corners of the spawn square
        spawn_points = [
            (mid_point - spawn_square_radius, mid_point - spawn_square_radius),
            (mid_point + spawn_square_radius, mid_point - spawn_square_radius),
            (mid_point + spawn_square_radius, mid_point + spawn_square_radius),
            (mid_point - spawn_square_radius, mid_point + spawn_square_radius),
        ]

        for _ in range(int(n_food * 0.1)):  # 90% of the food is around the square
            # Choose a random corner for each food entity
            spawn_x, spawn_y = random.choice(spawn_points)
            # Add randomness to the spawn location
            x = np.random.randint(spawn_x - spawn_random_radius, spawn_x + spawn_random_radius) % self.size
            y = np.random.randint(spawn_y - spawn_random_radius, spawn_y + spawn_random_radius) % self.size

            self.cells[x][y].entities.append(Food(0, 0))  # Food is added at position (0, 0) relative to the cell

        for _ in range(int(n_food * 0.9)):  # Remaining 10% of the food is random within the box
            x, y = np.random.randint(0, self.size, 2)
            self.cells[x][y].entities.append(Food(0, 0))  # Food is added at position (0, 0) relative to the cell


    def entities(self):
        """Return a single list of all entities in all cells."""
        return [entity for row in self.cells for cell in row for entity in cell.entities]


class Cell:
    def __init__(self):
        self.entities = []
