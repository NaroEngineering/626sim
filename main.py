import os
import pygame
import matplotlib.pyplot as plt
from datetime import datetime
from environment import Environment
from game_window import GameWindow
from user_input import get_user_input
import time


def main():
    num_preds, num_prey, size, pred_hunger, prey_hunger, food_rate, initial_food = get_user_input()
    entity_size = 5  # Size of each entity square
    window_size = size * entity_size  # Calculate the desired window size

    env = Environment(size, num_preds, num_prey, size, pred_hunger, prey_hunger, food_rate)
    game_window = GameWindow(size, entity_size)  # Pass the entity size to the GameWindow constructor
    running = True
    step = 0

    while running:
        start_time = time.time()  # Start the timer

        env.update()
        game_window.draw(env.cells)
        
        # End simulation if number of predators and prey is 0
        if env.entity_counts["Predator"][-1] == 0 and env.entity_counts["Prey"][-1] == 0:
            running = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate elapsed time
        
        print(f"Step {step} completed in {elapsed_time} seconds.")
        
        step += 1  # Increment the step counter

    # Create directory for data if it doesn't exist
    if not os.path.exists('lot626data'):
        os.makedirs('lot626data')
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")  # Generate a timestamp
    plt.figure()
    for entity_type, counts in env.entity_counts.items():
        plt.plot(env.time_steps, counts, label=entity_type)
    plt.xlabel('Time steps')
    plt.ylabel('Number')
    plt.legend()
    plt.title(f"#Pred={num_preds}_#prey={num_prey}")
    
    # Save the figure
    filename = f"lot626data/num_preds={num_preds}_num_prey={num_prey}_{timestamp}.png"
    plt.savefig(filename)
    
    plt.show()

    pygame.quit()

if __name__ == "__main__":
    main()