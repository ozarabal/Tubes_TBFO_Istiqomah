class PDA:
    def __init__(self, symbols, stack_symbols, start_stack, start_state, transitions):
        self.symbols = symbols
        self.stack_symbols = stack_symbols
        self.start_stack = start_stack
        self.start_state = start_state
        self.transitions = transitions
        self.stack = [start_stack]
        self.current_state = start_state

    def simulate(self, input_string):
        tags = [tag.strip() for tag in input_string.replace('>', ' > ').replace('<',' < ').replace('/',' / ').replace('=',' = ').replace('"',' " ').split() if tag.strip()]
        # for tag in tags:
        #     baru = [ tag.] 
        #       tags = [tag.strip() for tag in input_string.replace('>', ' > ').split() if tag.strip()]
        print(tags)
        temp = tags[0]
        for tag in tags:
            print(self.current_state)
            if temp == '>' and tag != '<' and tag not in self.symbols:
                tag = 'any-<'
            elif temp == '"' and tag not in self.symbols and tag != '<':
                tag = 'any-"'
            elif tag not in self.symbols:
                return False  # Reject if symbol is not in the alphabet
            
            top_of_stack = self.stack[-1]
            
            if (self.current_state, tag, top_of_stack) in self.transitions:
                self.stack.pop()
                
                state_action = self.transitions[(self.current_state, tag, top_of_stack)]
    
                for i in range (len(state_action[1])-1,-1,-1):
                    if state_action[1][i] != 'e':
                        self.stack.append(state_action[1][i])
                # Transition to the next state
                # print(self.stack)
                self.current_state = state_action[0]
            else:
                print(self.current_state)
                return False  # Reject if no valid transition
            temp = tag
            print(self.stack)
        return len(self.stack) == 1 

def parse_pda_description(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    symbols = lines[0].strip().split()
    stack_symbols = lines[1].strip().split()
    start_stack = lines[2].strip()
    start_state = lines[3].strip()

    transitions = {}
    for line in lines[4:]:
        transition_data = line.strip().split()
        key = (transition_data[0], transition_data[1], transition_data[2])
        push = transition_data[4].strip().split(',')
        value = (transition_data[3],push)
        transitions[key] = value

    return {
        "symbols": symbols,
        "stack_symbols": stack_symbols,
        "start_stack": start_stack,
        "start_state": start_state,
        "transitions" : transitions
    }

def read_html_file(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()
    return html_content

def main():
    pda_file_path = 'pda.txt'
    html_file_path = 'gaa.html'

    pda_description = parse_pda_description(pda_file_path)
    html_content = read_html_file(html_file_path)
    pda = PDA(**pda_description)
    if pda.simulate(html_content):
        print("HTML file is correct according to the PDA.")
    else:
        print("HTML file is incorrect according to the PDA.")

if __name__ == "__main__":
    main()