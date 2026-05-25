from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

# ==========================================
# PART A: GRAPH CREATION (Building Layout)
# ==========================================

# Ismein 3 Rooms, 3 Corridors/Hallways, 1 Staircase aur 1 Exit hai.
building_layout = {
    "Room101": ["HallwayA"],
    "Room102": ["HallwayA"],
    "Room103": ["CorridorB"],
    "HallwayA": ["Room101", "Room102", "CorridorB"],
    "CorridorB": ["HallwayA", "Room103", "CorridorC"],
    "CorridorC": ["CorridorB", "Staircase"],
    "Staircase": ["CorridorC", "ExitA"],
    "ExitA": ["Staircase"]
}

# Hamein pata hona chahiye ki safe zone (exits) kaun si hain
exits = ["ExitA"]


# ==========================================
# PART B: PATHFINDING (BFS Algorithm)
# ==========================================
def find_evacuation_route(graph, start, fire_node, exit_nodes):
    
    if start not in graph:
        print(f"\n[Error] Location '{start}' building ke map mein nahi hai!")
        return None
        
   
    if start == fire_node:
        print("\n[Danger] Aap jahan khade hain, wahin aag lagi hai! Cannot evacuate safely.")
        return None

   
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current in visited:
            continue
        visited.add(current)

       
        if current in exit_nodes:
            return path

        
        for neighbor in graph[current]:
            
            if neighbor == fire_node:
                continue
                
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None  


# ==========================================
# PART C: USER INPUT & EXECUTION
# ==========================================
print("--- BUILDING EVACUATION SYSTEM ---")
print("Available Nodes:", ", ".join(building_layout.keys()))
print("-" * 34)


user_start = input("Enter Current Location (e.g., Room101): ").strip()
user_fire = input("Enter Fire/Blocked Location (e.g., CorridorB): ").strip()

# Path find karna
safe_route = find_evacuation_route(building_layout, user_start, user_fire, exits)


# Output Display
print("\n" + "="*10 + " EVACUATION REPORT " + "="*10)
print(f"Current Location : {user_start}")
print(f"Blocked Location : {user_fire}")
print("-" * 39)

if safe_route:
    print("Safe Route:")
    print(" -> ".join(safe_route))
    print(f"\nTotal Distance   : {len(safe_route) - 1} steps/units")
else:
    print("ALERT: No Safe Route Found! All paths to the exit are blocked by fire.")
print("=" * 39)


# ==========================================
# BONUS: GRAPH VISUALIZATION
# ==========================================
if safe_route or user_fire in building_layout:
    print("\nGenerating building map visualization...")
    
    # NetworkX graph object banana
    G = nx.Graph()
    for node, neighbors in building_layout.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Nodes ko color dena according to requirements
    node_colors = []
    for node in G.nodes():
        if node == user_fire:
            node_colors.append("red")        # Fire Node
        elif node in exits:
            node_colors.append("green")      # Exit Node
        elif safe_route and node in safe_route:
            node_colors.append("blue")       # Safe Path Nodes
        else:
            node_colors.append("lightgray")  # Normal Nodes

    # Graph plot karna
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)  # Seed taaki layout har baar clean aur same dikhe
    
    nx.draw(
        G, pos, 
        with_labels=True, 
        node_color=node_colors, 
        node_size=2500, 
        font_size=10, 
        font_weight="bold",
        edge_color="gray"
    )
    
    plt.title("Building Emergency Evacuation Map", fontsize=14, fontweight="bold")
    plt.show()