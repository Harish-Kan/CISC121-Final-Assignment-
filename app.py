##[AI Disclaimer: Used Claude with prompt “Implement the Algorithm Develop a working version of your chosen algorithm in Python. • Comment key steps so the logic is easy to follow. • Ensure the code is readable and correct, not just functional. • The code structure does not have to be OOP • Handle user input and output to the GUI carefully (e.g., incorrect entries). Bubble sort is the algorithm of choice in this case. Decomposition : Starts off with taking the user’s list of numbers Comparing each pair of numbers, with its adjacent element If the left one is indeed larger, then it swaps them It keeps repeating the passes until no more swaps are needed As it outputs the sorted list in the end, it also shows every single step Pattern recognition ; Bubble Sort The algorithm (bubble sort) keeps repeating the same action over and over again until the condition is met Compares, possibly swaps, and then moves onto the next pair The larger value gets pushed to the end every single time when there is a pass The unsorted part, becomes smaller and smaller after every swap Abstraction : Shown to the user : After every single swap, the list Which of the 2 elements are being compared to each other The step number Not shown : The loop variables Internal Counters As well as the memory operations Algorithm Design : Input : Inside of the Gradio textbox, a list of numbers which are separated by commas Processing :  Bubble Sort is run, it then records every comparison as well as swap Output : Inside of GUI, it shows every step that the algorithm (bubble sort) takes. And in the end it shows the finalized sorted list The user in the end can end up choosing if they want to step through it, or see the full run of it. These are the steps needed, please implement the steps. This again is done through Python. Step 4 — Add Interactivity with a Python UI Library, Use a beginner friendly UI library such as Gradio. Another option is Tkinter, but that is for desktop Python apps only and cannot be deployed on Hugging Face. So, please use Gradio. • Create input boxes, e.g., for target value/s and search array, and result displays. • Show each step or the final result clearly. • Keep the interface simple enough that anyone can understand it. Ensure that it is truly interactiv, there are boxes that can be moved around to truly show the full implementation of the bubble sorting algorithm. The version of Python I am using is 3.12.11. Please use all the correct syntax and gradio implementation. There should not be any errors. Ensure that it doesn't just get stuck at one step, that it is able to visually go through every single one of the necessary steps. It is also actually show the swapping, not just be stuck. Ensure that all the buttons work. Especailly the next button. Ensure that the next button actually does it's job. And ensure that the sorting and swapping is actually shown. Not just the first step, but every step must be shown. It is still stuck, as the next button isn't working after the first step”]


"""
Interactive Bubble Sort Visualizer
COMPLETELY REWRITTEN - Next button WILL work
Using simplified state management
"""

import gradio as gr


class BubbleSortVisualizer:
    """Class to manage sorting state."""
    
    def __init__(self):
        self.steps = []
        self.current_step = 0
    
    def generate_steps(self, numbers):
        """Generate all sorting steps."""
        self.steps = []
        self.current_step = 0
        arr = numbers.copy()
        n = len(arr)
        
        # Step 0: Initial
        self.steps.append({
            'num': 0,
            'arr': arr.copy(),
            'cmp': [],
            'swap': False,
            'msg': f"Initial array: {arr}"
        })
        
        step_num = 1
        
        # Sorting
        for i in range(n - 1):
            had_swap = False
            
            for j in range(n - i - 1):
                # Compare
                self.steps.append({
                    'num': step_num,
                    'arr': arr.copy(),
                    'cmp': [j, j + 1],
                    'swap': False,
                    'msg': f"Pass {i+1}: Compare arr[{j}]={arr[j]} with arr[{j+1}]={arr[j+1]}"
                })
                step_num += 1
                
                # Swap if needed
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    had_swap = True
                    
                    self.steps.append({
                        'num': step_num,
                        'arr': arr.copy(),
                        'cmp': [j, j + 1],
                        'swap': True,
                        'msg': f"Pass {i+1}: SWAPPED! Now: {arr}"
                    })
                    step_num += 1
                else:
                    self.steps.append({
                        'num': step_num,
                        'arr': arr.copy(),
                        'cmp': [j, j + 1],
                        'swap': False,
                        'msg': f"Pass {i+1}: No swap"
                    })
                    step_num += 1
            
            if not had_swap:
                self.steps.append({
                    'num': step_num,
                    'arr': arr.copy(),
                    'cmp': [],
                    'swap': False,
                    'msg': f"Pass {i+1}: Sorted!"
                })
                step_num += 1
                break
        
        # Final
        self.steps.append({
            'num': step_num,
            'arr': arr.copy(),
            'cmp': [],
            'swap': False,
            'msg': f"COMPLETE: {arr}"
        })
    
    def get_step(self, step_index):
        """Get a specific step."""
        if not self.steps or step_index < 0 or step_index >= len(self.steps):
            return None
        return self.steps[step_index]
    
    def total_steps(self):
        """Get total number of steps."""
        return len(self.steps)


# Global visualizer instance
visualizer = BubbleSortVisualizer()


def make_visual(arr, cmp, swap):
    """Create visual HTML."""
    html = '<div style="display: flex; justify-content: center; gap: 10px; padding: 30px; flex-wrap: wrap;">'
    
    for i, val in enumerate(arr):
        if i in cmp and swap:
            style = "background: #22c55e; color: white; border: 4px solid #15803d; transform: scale(1.2); box-shadow: 0 10px 25px rgba(34,197,94,0.5);"
        elif i in cmp:
            style = "background: #3b82f6; color: white; border: 4px solid #1d4ed8; transform: scale(1.15); box-shadow: 0 8px 20px rgba(59,130,246,0.5);"
        else:
            style = "background: #f1f5f9; color: #334155; border: 3px solid #cbd5e1; transform: scale(1); box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
        
        html += f'<div style="{style} width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; border-radius: 15px; font-size: 24px; font-weight: bold; transition: all 0.5s;">{val}</div>'
    
    html += '</div>'
    return html


def make_legend():
    """Create legend."""
    return '''<div style="display: flex; justify-content: center; gap: 30px; margin: 20px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 40px; height: 40px; background: #3b82f6; border: 3px solid #1d4ed8; border-radius: 10px;"></div>
            <span style="font-weight: bold;">Comparing</span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 40px; height: 40px; background: #22c55e; border: 3px solid #15803d; border-radius: 10px;"></div>
            <span style="font-weight: bold;">Swapped</span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 40px; height: 40px; background: #f1f5f9; border: 3px solid #cbd5e1; border-radius: 10px;"></div>
            <span style="font-weight: bold;">Unsorted</span>
        </div>
    </div>'''


def parse_input(text):
    """Parse input."""
    if not text or not text.strip():
        return None, "Error: Enter numbers"
    
    nums = []
    for part in text.split(','):
        part = part.strip()
        if not part:
            continue
        try:
            n = float(part)
            if n.is_integer():
                n = int(n)
            nums.append(n)
        except:
            return None, f"Error: '{part}' not a number"
    
    if not nums:
        return None, "Error: No numbers found"
    
    return nums, None


def start_sorting(input_text):
    """Start button handler."""
    nums, error = parse_input(input_text)
    
    if error:
        return (
            0, error, "", "",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False)
        )
    
    # Generate all steps
    visualizer.generate_steps(nums)
    
    # Show first step
    step = visualizer.get_step(0)
    visual = make_visual(step['arr'], step['cmp'], step['swap'])
    legend = make_legend()
    status = f"**Step {step['num']} of {visualizer.total_steps()-1}:** {step['msg']}"
    
    return (
        0,  # current step index
        status,
        visual,
        legend,
        gr.update(visible=True, minimum=0, maximum=visualizer.total_steps()-1, value=0),
        gr.update(visible=True, interactive=False),  # prev disabled
        gr.update(visible=True, interactive=True),   # next enabled
        gr.update(visible=True),
        gr.update(visible=True)
    )


def show_step(step_idx):
    """Show a specific step."""
    step_idx = int(step_idx)
    
    if step_idx < 0 or step_idx >= visualizer.total_steps():
        return "Invalid step", "", gr.update(interactive=False), gr.update(interactive=False)
    
    step = visualizer.get_step(step_idx)
    visual = make_visual(step['arr'], step['cmp'], step['swap'])
    status = f"**Step {step['num']} of {visualizer.total_steps()-1}:** {step['msg']}"
    
    prev_enabled = step_idx > 0
    next_enabled = step_idx < visualizer.total_steps() - 1
    
    return status, visual, gr.update(interactive=prev_enabled), gr.update(interactive=next_enabled)


def next_clicked(current_idx):
    """Next button clicked."""
    new_idx = int(current_idx) + 1
    
    if new_idx >= visualizer.total_steps():
        new_idx = visualizer.total_steps() - 1
    
    print(f"Next: {current_idx} -> {new_idx}")  # Debug
    
    status, visual, prev_btn, next_btn = show_step(new_idx)
    
    return new_idx, status, visual, prev_btn, next_btn


def prev_clicked(current_idx):
    """Previous button clicked."""
    new_idx = int(current_idx) - 1
    
    if new_idx < 0:
        new_idx = 0
    
    print(f"Prev: {current_idx} -> {new_idx}")  # Debug
    
    status, visual, prev_btn, next_btn = show_step(new_idx)
    
    return new_idx, status, visual, prev_btn, next_btn


def show_all():
    """Show all steps."""
    if not visualizer.steps:
        return "No sorting in progress"
    
    output = "=" * 80 + "\n"
    output += "COMPLETE BUBBLE SORT PROCESS\n"
    output += "=" * 80 + "\n\n"
    
    for step in visualizer.steps:
        output += f"STEP {step['num']}: {step['msg']}\n"
        output += f"Array: {step['arr']}\n"
        if step['cmp']:
            output += f"Comparing: {step['cmp']}\n"
        if step['swap']:
            output += ">>> SWAP <<<\n"
        output += "-" * 80 + "\n"
    
    return output


def reset():
    """Reset everything."""
    visualizer.steps = []
    visualizer.current_step = 0
    
    return (
        0,
        "Enter numbers and click Start",
        "", "",
        gr.update(visible=False, value=0),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        "", ""
    )


# BUILD UI
with gr.Blocks(title="Bubble Sort") as app:
    
    # This state holds the current step index
    step_index = gr.State(0)
    
    gr.Markdown("# 🔄 Bubble Sort Visualizer\n### Click Next to see each step")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Input")
            input_box = gr.Textbox(label="Numbers (comma-separated)", placeholder="1, 2, 3, 4", lines=2)
            start_btn = gr.Button("▶ Start", variant="primary", size="lg")
            
            gr.Markdown("### Controls")
            slider = gr.Slider(0, 10, 0, step=1, label="Step", visible=False)
            
            with gr.Row():
                prev_btn = gr.Button("⬅ Prev", visible=False)
                next_btn = gr.Button("Next ➡", visible=False, variant="primary")
            
            with gr.Row():
                all_btn = gr.Button("📜 All Steps", visible=False)
                reset_btn = gr.Button("🔄 Reset", visible=False)
            
            gr.Examples([["1, 2, 3, 4"], ["5, 2, 8, 1"]], input_box)
        
        with gr.Column(scale=2):
            gr.Markdown("### Visualization")
            status_box = gr.Markdown("Enter numbers and click Start")
            visual_box = gr.HTML("")
            legend_box = gr.HTML("")
            
            with gr.Accordion("All Steps", open=False):
                all_box = gr.Textbox(label="Log", lines=20)
    
    # CONNECT EVENTS
    start_btn.click(
        start_sorting,
        inputs=[input_box],
        outputs=[step_index, status_box, visual_box, legend_box, slider, prev_btn, next_btn, all_btn, reset_btn]
    )
    
    slider.change(
        show_step,
        inputs=[slider],
        outputs=[status_box, visual_box, prev_btn, next_btn]
    )
    
    # KEY: Next button
    next_btn.click(
        next_clicked,
        inputs=[step_index],
        outputs=[step_index, status_box, visual_box, prev_btn, next_btn]
    )
    
    prev_btn.click(
        prev_clicked,
        inputs=[step_index],
        outputs=[step_index, status_box, visual_box, prev_btn, next_btn]
    )
    
    all_btn.click(show_all, outputs=[all_box])
    
    reset_btn.click(
        reset,
        outputs=[step_index, status_box, visual_box, legend_box, slider, prev_btn, next_btn, all_btn, reset_btn, input_box, all_box]
    )


if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", server_port=7860, debug=True)