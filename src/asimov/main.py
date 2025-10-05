from .models.asimovian import Asimovian 

if __name__ == "__main__":
    # Example run
    sim = Asimovian(width=10, 
                    height=10,
                    num_bondholders=10,
                    num_robots=1,
                    num_enterprises=1,
                    seed=42)
    for _ in range(5):
        sim.step()
    print("Simulation complete!")