import argparse
class PDA:
    def __init__(self, symbols, stack_symbols, start_stack, start_state, transitions):
        self.symbols = symbols
        self.stack_symbols = stack_symbols
        self.start_stack = start_stack
        self.start_state = start_state
        self.transitions = transitions
        self.stack = [start_stack]
        self.current_state = start_state

    def checkingSnytax(self, input_string):
        tags = [tag.strip() for tag in input_string.replace('!--',' !-- ').replace('>', ' > ').replace('<',' < ').replace('/',' / ').replace('=',' = ').replace('"',' " ').split() if tag.strip()]
        merge_tags = []
        current_sting = []
        
        for tag in tags:
            if tag == '"' and not '"' in current_sting:
                current_sting += tag 
                merge_tags.append(tag)
            elif '"' in current_sting and tag != '"':
                current_sting += tag
            elif tag == '"' and '"' in current_sting:
                current_sting.pop(0)
                current_sting = "".join(current_sting)
                merge_tags.append(current_sting)
                current_sting = []
                merge_tags.append(tag)
            else:
                merge_tags.append(tag)
        
        tagprev = ""
        for tag in merge_tags:
            cek = False
            if tagprev == '>' and tag != '<':
                temp = tag
                tag = 'any-<'
                cek = True 
            elif tagprev == '!--' and tag != '>' :
                temp = tag
                tag = 'any->'
                cek = True
            elif tagprev == '"' and tag != '"' and tag not in self.symbols:
                temp = tag
                tag = 'any-"'
            elif tag not in self.symbols:
                return False , tag
            top_of_stack = self.stack[-1]
            
            if (self.current_state, tag, top_of_stack) in self.transitions:
                self.stack.pop()
                state_action = self.transitions[(self.current_state, tag, top_of_stack)]
    
                for i in range (len(state_action[1])-1,-1,-1):
                    if state_action[1][i] != 'e':
                        self.stack.append(state_action[1][i])
                self.current_state = state_action[0]
            else:
                if tag == 'any-"' or tag == 'any->' or tag == 'any-<':
                    tag = temp
                return False , tag
            if not cek:    
                tagprev = tag
        return len(self.stack) == 1 , ""

def bacaPDA(file_path):
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

def bacaHTML(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()
    return html_content

def main():
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('pda_file', type=str, help='The PDA file')
    parser.add_argument('html_file', type=str, help='The HTML file')

    args = parser.parse_args()

    pda_description = bacaPDA(args.pda_file)
    html_content = bacaHTML(args.html_file)
    pda = PDA(**pda_description)
    cek , tag = pda.checkingSnytax(html_content)
    if cek:
        print("Accepted")
    else:
        print("Syntax error")
        print(f"Terjadi kesalahan ekspresi: {tag}")

if __name__ == "__main__":
    main()