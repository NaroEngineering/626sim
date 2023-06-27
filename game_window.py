import pygame
from entities import Predator, Prey, Food

class GameWindow:
    def __init__(self, size, entity_size):
        pygame.init()
        self.screen = pygame.display.set_mode((size * entity_size, size * entity_size))
        self.entity_colors = {
            "Predator": (255, 0, 0),
            "Prey": (0, 255, 0),
            "Food": (255, 255, 255),
        }
        self.entity_size = entity_size  # Store the entity size

    def draw(self, cells):
        self.screen.fill((0, 0, 0))
        for i, row in enumerate(cells):
            for j, cell in enumerate(row):
                for entity in cell.entities:
                    color = self.entity_colors[type(entity).__name__]
                    # Adjust the rectangle coordinates to bound the entities
                    pygame.draw.rect(self.screen, color, (entity.position[0] * self.entity_size, entity.position[1] * self.entity_size, self.entity_size, self.entity_size))
        pygame.display.flip()
