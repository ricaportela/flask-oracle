# define our states and transitions
states = ['clientqty', 'clientids', 'cameraqty', 'cameraids']
transitions = [
    {
        'trigger': 'advance',
        'source': 'clientqty',
        'dest': 'clientids',
        'conditions': 'user_agrees'
    },
    {
        'trigger': 'advance',
        'source': 'clientids',
        'dest': 'cameraqty',
        'conditions': 'validate_demographics',
        'before': 'save_demographics'
    },
    {
        'trigger': 'advance',
        'source': 'cameraqty',
        'dest': 'cameraids',
        'conditions': 'no_more_items',
        'before': 'save_items'
    }
]

# # Initialize the state machine with the above states and transitions, and start out life in the solid state.
# machine = Machine(states=states, transitions=transitions, initial='consent')
#
# # Let's see how it works...
# machine.state
# > 'consent'
# machine.advance()  # Trigger methods are magically added for us!
# machine.state
# > 'demographics'