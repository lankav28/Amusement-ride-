from collections import deque

class Group:
    def __init__(self, group_id, members, max_wait_time):
        self.group_id = group_id
        self.members = members
        self.max_wait_time = max_wait_time
        self.waited_time = 0
    
    def __repr__(self):
        return f"Group {self.group_id} (Members: {self.members}, Max Wait: {self.max_wait_time})"

# Function to simulate pure round robin ride scheduling
def pure_round_robin_ride_scheduling(groups, rides):
    # Create a queue for the groups
    group_queue = deque(groups)
    
    # Track total rounds and the ride allocation log
    total_rounds = 0
    ride_log = []

    # Continue until all queues are empty or all groups leave due to wait times
    while group_queue:
        for ride in rides:
            current_ride_capacity = ride['capacity']
            current_ride_time = ride['ride_time']
            remaining_groups = deque()
            
            for group in group_queue:
                # Check if the group has waited too long
                if group.waited_time > group.max_wait_time:
                    ride_log.append(f"Group {group.group_id} left due to excessive wait time.")
                    continue  # Skip this group as they leave the queue
                
                # Process the ride for the group
                if group.members <= current_ride_capacity:
                    # All members can ride
                    ride_members = group.members
                    group.members = 0  # Group is done
                else:
                    # Partial group rides
                    ride_members = current_ride_capacity
                    group.members -= current_ride_capacity
                
                total_rounds += 1
                ride_log.append(f"Round {total_rounds}: Group {group.group_id} with {ride_members} members rode on {ride['name']}.")

                # If the group still has members, they wait for the next round
                if group.members > 0:
                    group.waited_time += current_ride_time  # Increase wait time for the group
                    remaining_groups.append(group)
                else:
                    ride_log.append(f"Group {group.group_id} finished their ride.")
            
            group_queue = remaining_groups  # Update the queue with remaining groups
    
    return total_rounds, ride_log

# Main program with user input
if __name__ == "__main__":
    # Get the number of groups
    num_groups = int(input("Enter the number of groups: "))
    
    # Define a list of groups with dynamic members and wait times
    groups = []
    for i in range(num_groups):
        members = int(input(f"Enter the number of members in Group {i+1}: "))
        max_wait_time = int(input(f"Enter the maximum wait time (in minutes) for Group {i+1}: "))
        groups.append(Group(i + 1, members, max_wait_time))
    
    # Define multiple rides with dynamic capacities and ride times
    rides = [
        {'name': 'Roller Coaster', 'capacity': 4, 'ride_time': 5},
        {'name': 'Ferris Wheel', 'capacity': 6, 'ride_time': 8},
        {'name': 'Bumper Cars', 'capacity': 3, 'ride_time': 4}
    ]
    
    # Perform the pure Round Robin Ride Scheduling
    total_rounds, log = pure_round_robin_ride_scheduling(groups, rides)
    
    # Output the results
    print(f"\nTotal Rounds: {total_rounds}")
    for entry in log:
        print(entry)
