import numpy as np

class Entity:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._alive = True

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, value):
        self._alive = value

    @property
    def position(self):
        return self._x, self._y

    def kill(self):
        self._alive = False

    def move(self):
        dx, dy = np.random.randint(-1, 2, 2)  # Random move direction
        self._x += dx
        self._y += dy
        return dx, dy
    
    def reproduce(self, reproduction_rate):
        if np.random.random() < reproduction_rate:
            return type(self)(self._x, self._y, self.initial_hunger)
        return None


class Predator(Entity):
    def __init__(self, x, y, hunger):
        super().__init__(x, y)
        self.hunger = hunger
        self.initial_hunger = hunger 

    def eat(self):
        self.hunger += 1
        offspring = self.reproduce(0.5)  # Adjust this rate as necessary
        return offspring

    def update(self, cell):
        if not self.alive:
            return

        self.hunger -= 1
        if self.hunger <= 0:
            self.kill()

        dx, dy = self.move()
        new_pos = (self._x + dx, self._y + dy)

        new_entities = [entity for entity in cell.entities if entity.position != new_pos or not isinstance(entity, Prey)]

        if len(new_entities) < len(cell.entities):
            cell.entities = new_entities
            cell.entities.append(self)


class Prey(Entity):
    def __init__(self, x, y, hunger):
        super().__init__(x, y)
        self.hunger = hunger
        self.initial_hunger = hunger 

    def eat(self):
        self.hunger += 1
        offspring = self.reproduce(1)  # Adjust this rate as necessary
        return offspring

    def update(self, cell):
        if not self.alive:
            return

        self.hunger -= 1
        if self.hunger <= 0:
            self.kill()

        dx, dy = self.move()
        new_pos = (self._x + dx, self._y + dy)

        new_entities = [entity for entity in cell.entities if entity.position != new_pos or not isinstance(entity, Food)]

        if len(new_entities) < len(cell.entities):
            cell.entities = new_entities
            cell.entities.append(self)

class Food(Entity):
    def move(self):
        return 0, 0

    def __init__(self, x, y, spoil_date):
        super().__init__(x, y)
        self.spoil_date = spoil_date

    def update(self, environment):
        self.spoil_date -= 1
        if self.spoil_date <= 0:
            environment.remove_entity(self)