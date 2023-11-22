# Read automaton information from the txt file
def read_automaton_info(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    input_symbols = lines[0].split()
    stack_symbols = lines[1].split()
    starting_stack = lines[2].strip()
    accepting_state = lines[3].strip()
    starting_state = lines[4].strip()
    transitions = [tuple(line.strip().split()) for line in lines[5:]]
    return input_symbols, stack_symbols, starting_stack, accepting_state,starting_state, transitions
file = 'test.txt'
print(read_automaton_info(file))
# Validate HTML     using pushdown automaton rules
def validate_html(html_file, automaton_info_file):

    # Read automaton info
    input_symbols, stack_symbols, starting_stack, accepting_state,starting_state, transitions = read_automaton_info(automaton_info_file)

    # Initialize stack with starting symbol
    stack = [stack_symbols[0]]
    current_state = starting_state

    # Read HTML file
    with open(html_file, 'r') as file:
        html_content = file.read()

    # Split HTML content by tags
    tags = [tag.strip() for tag in html_content.replace('>', ' > ').split() if tag.strip()]

    # Check if each tag in the HTML content follows automaton rules
    for tag in tags:
        found_transition = False
        for transition in transitions:
            if current_state == transition[0] and tag in transition[1] and stack[-1] == transition[2]:
                stack.pop()
                stack.extend(transition[4:])
                current_state = transition[3]
                found_transition = True
                break

        if not found_transition:
            return False  # Tag doesn't follow automaton rules

    # Check if the stack is empty at the end and the final state is accepting
    return len(stack) == 0 and current_state == accepting_state

# Test the HTML file against the pushdown automaton rules
html_file_to_check = 'index.html'  # Replace with your HTML file name
automaton_info_file = 'test.txt'

result = validate_html(html_file_to_check, automaton_info_file)
if result:
    print("HTML file follows pushdown automaton rules.")
else:
    print("HTML file does not follow pushdown automaton rules.")
