"""
Interactive Bubble Sort Visualizer
===================================
This program implements the Bubble Sort algorithm with step-by-step visualization.
Users can see every comparison and swap operation as the algorithm sorts numbers.

Course: CISC 121 - Introduction to Computing Science
Algorithm: Bubble Sort
UI Framework: Gradio (for web-based interface)
Python Version: 3.12.11

AI Disclaimer: This code was developed with assistance from Claude AI.
The implementation follows computational thinking principles including:
- Decomposition: Breaking down the sorting process into individual steps
- Pattern Recognition: Identifying the repeating compare-and-swap pattern
- Abstraction: Hiding implementation details while showing relevant information
- Algorithm Design: Structured input, processing, and output flow
"""

import gradio as gr


class BubbleSortVisualizer:
    """
    Manages the state and generation of bubble sort visualization steps.
    
    This class encapsulates all the logic for:
    - Generating sorting steps
    - Storing the complete sorting history
    - Tracking the current position in the sorting process
    
    Attributes:
        steps (list): List of dictionaries, each representing one step in the sorting process
        current_step (int): Index of the current step being displayed
    """
    
    def __init__(self):
        """Initialize the visualizer with empty state."""
        self.steps = []  # Will store all sorting steps
        self.current_step = 0  # Tracks which step we're currently viewing
    
    def generate_steps(self, numbers):
        """
        Generate all sorting steps for the bubble sort algorithm.
        
        This is the core bubble sort implementation that records every action:
        - Every comparison between adjacent elements
        - Every swap operation performed
        - The array state after each operation
        
        Args:
            numbers (list): List of numbers to be sorted
            
        Process:
            1. Start with unsorted array
            2. Compare adjacent pairs
            3. Swap if left > right
            4. Repeat until no swaps needed (array is sorted)
        """
        # Reset state for new sorting session
        self.steps = []
        self.current_step = 0
        arr = numbers.copy()  # Create copy to avoid modifying original input
        n = len(arr)
        
        # STEP 0: Record the initial unsorted state
        # This allows users to see the starting point before any sorting begins
        self.steps.append({
            'num': 0,  # Step number
            'arr': arr.copy(),  # Current state of array
            'cmp': [],  # Indices being compared (empty for initial state)
            'swap': False,  # Whether a swap occurred
            'msg': f"Initial array: {arr}"  # Human-readable description
        })
        
        step_num = 1  # Counter for tracking step numbers
        
        # OUTER LOOP: Controls the number of passes through the array
        # We need at most (n-1) passes because:
        # - Each pass moves at least one element to its correct position
        # - After (n-1) passes, all elements except the first must be sorted
        # - If all others are sorted, the first element must also be in place
        for i in range(n - 1):
            had_swap = False  # Flag to detect if any swaps occurred in this pass
            
            # INNER LOOP: Compare and potentially swap adjacent elements
            # Range decreases by i each time because:
            # - After pass 1: largest element is at the end (position n-1)
            # - After pass 2: two largest elements are at the end (n-2, n-1)
            # - After pass i: i largest elements are in their final positions
            # So we don't need to compare them again
            for j in range(n - i - 1):
                # COMPARISON STEP
                # Record the comparison before we decide whether to swap
                # This shows users which two elements are being evaluated
                self.steps.append({
                    'num': step_num,
                    'arr': arr.copy(),
                    'cmp': [j, j + 1],  # Indices of elements being compared
                    'swap': False,  # Not swapping yet, just comparing
                    'msg': f"Pass {i+1}: Compare arr[{j}]={arr[j]} with arr[{j+1}]={arr[j+1]}"
                })
                step_num += 1
                
                # DECISION: Should we swap these elements?
                # Swap if left element is greater than right element
                # This moves larger values toward the end of the array
                if arr[j] > arr[j + 1]:
                    # PERFORM THE SWAP
                    # Python allows elegant tuple unpacking for swapping
                    # This is equivalent to: temp = arr[j]; arr[j] = arr[j+1]; arr[j+1] = temp
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    had_swap = True  # Mark that we made at least one swap this pass
                    
                    # SWAP STEP
                    # Record the state after the swap so users can see the change
                    self.steps.append({
                        'num': step_num,
                        'arr': arr.copy(),
                        'cmp': [j, j + 1],  # Same indices, but now swapped
                        'swap': True,  # Indicate this was a swap operation
                        'msg': f"Pass {i+1}: SWAPPED! Now: {arr}"
                    })
                    step_num += 1
                else:
                    # NO SWAP NEEDED
                    # Elements are already in correct order (left <= right)
                    # Still record this step to show the decision-making process
                    self.steps.append({
                        'num': step_num,
                        'arr': arr.copy(),
                        'cmp': [j, j + 1],
                        'swap': False,
                        'msg': f"Pass {i+1}: No swap"
                    })
                    step_num += 1
            
            # END OF PASS CHECK
            # If we made no swaps during this entire pass, the array is sorted!
            # This is an optimization that allows early termination
            if not had_swap:
                self.steps.append({
                    'num': step_num,
                    'arr': arr.copy(),
                    'cmp': [],
                    'swap': False,
                    'msg': f"Pass {i+1}: Sorted!"
                })
                step_num += 1
                break  # Exit early, no need for more passes
        
        # FINAL STEP
        # Record the completion state with the fully sorted array
        self.steps.append({
            'num': step_num,
            'arr': arr.copy(),
            'cmp': [],
            'swap': False,
            'msg': f"COMPLETE: {arr}"
        })
    
    def get_step(self, step_index):
        """
        Retrieve a specific step from the sorting history.
        
        Args:
            step_index (int): Index of the step to retrieve
            
        Returns:
            dict: Step information, or None if index is invalid
        """
        # Validate that the index is within bounds
        if not self.steps or step_index < 0 or step_index >= len(self.steps):
            return None
        return self.steps[step_index]
    
    def total_steps(self):
        """
        Get the total number of steps in the current sorting process.
        
        Returns:
            int: Total number of steps recorded
        """
        return len(self.steps)


# GLOBAL INSTANCE
# Create a single instance that persists across function calls
# This maintains state between user interactions in the Gradio interface
visualizer = BubbleSortVisualizer()


def make_visual(arr, cmp, swap):
    """
    Create an HTML visualization of the array with color-coded elements.
    
    This function generates styled HTML boxes to represent array elements.
    Different colors indicate different states in the sorting process.
    
    Args:
        arr (list): Current state of the array
        cmp (list): Indices of elements being compared [left_index, right_index]
        swap (bool): Whether a swap just occurred
        
    Returns:
        str: HTML string with styled div elements
        
    Color Coding:
        - Green: Elements that were just swapped
        - Blue: Elements currently being compared
        - Light gray: Regular unsorted elements
    """
    # Container div with flexbox for horizontal layout
    html = '<div style="display: flex; justify-content: center; gap: 10px; padding: 30px; flex-wrap: wrap;">'
    
    # Create a box for each element in the array
    for i, val in enumerate(arr):
        # DETERMINE STYLING based on element's current role
        if i in cmp and swap:
            # GREEN: This element was just swapped
            # Scale up slightly to draw attention to the swap
            style = "background: #22c55e; color: white; border: 4px solid #15803d; transform: scale(1.2); box-shadow: 0 10px 25px rgba(34,197,94,0.5);"
        elif i in cmp:
            # BLUE: This element is being compared (but not swapped)
            style = "background: #3b82f6; color: white; border: 4px solid #1d4ed8; transform: scale(1.15); box-shadow: 0 8px 20px rgba(59,130,246,0.5);"
        else:
            # GRAY: Regular element, not currently involved in any operation
            style = "background: #f1f5f9; color: #334155; border: 3px solid #cbd5e1; transform: scale(1); box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
        
        # Create individual box for this array element
        # CSS transition provides smooth animation when styles change
        html += f'<div style="{style} width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; border-radius: 15px; font-size: 24px; font-weight: bold; transition: all 0.5s;">{val}</div>'
    
    html += '</div>'
    return html


def make_legend():
    """
    Create a color legend to explain the visualization.
    
    Returns:
        str: HTML string showing what each color means
    """
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
    """
    Parse and validate user input from the text box.
    
    This function handles the INPUT phase of the algorithm:
    - Accepts comma-separated numbers
    - Validates each entry is a valid number
    - Handles errors gracefully with clear messages
    
    Args:
        text (str): Raw input string from user
        
    Returns:
        tuple: (list of numbers, error message)
               Returns (list, None) if successful
               Returns (None, error_string) if validation fails
    """
    # Check for empty input
    if not text or not text.strip():
        return None, "Error: Enter numbers"
    
    nums = []
    # Split by comma and process each part
    for part in text.split(','):
        part = part.strip()  # Remove leading/trailing whitespace
        if not part:
            continue  # Skip empty entries (e.g., from trailing commas)
        
        try:
            # Try to convert to number (float first to handle decimals)
            n = float(part)
            # Convert to int if it's a whole number for cleaner display
            if n.is_integer():
                n = int(n)
            nums.append(n)
        except:
            # Catch any conversion errors and return descriptive message
            return None, f"Error: '{part}' not a number"
    
    # Ensure we got at least one valid number
    if not nums:
        return None, "Error: No numbers found"
    
    return nums, None


def start_sorting(input_text):
    """
    Handle the Start button click event.
    
    This function orchestrates the beginning of the sorting visualization:
    1. Validate user input
    2. Generate all sorting steps
    3. Display the initial state
    4. Enable navigation controls
    
    Args:
        input_text (str): User's input from the textbox
        
    Returns:
        tuple: Updates for all UI components (10 values)
    """
    # STEP 1: Validate input
    nums, error = parse_input(input_text)
    
    if error:
        # If validation failed, show error and hide controls
        return (
            0,  # step_index
            error,  # status message
            "",  # visual (empty)
            "",  # legend (empty)
            gr.update(visible=False),  # slider (hidden)
            gr.update(visible=False),  # prev button (hidden)
            gr.update(visible=False),  # next button (hidden)
            gr.update(visible=False),  # show all button (hidden)
            gr.update(visible=False)   # reset button (hidden)
        )
    
    # STEP 2: Generate all sorting steps
    # This runs the complete bubble sort algorithm and stores every step
    visualizer.generate_steps(nums)
    
    # STEP 3: Display the first step (initial unsorted array)
    step = visualizer.get_step(0)
    visual = make_visual(step['arr'], step['cmp'], step['swap'])
    legend = make_legend()
    status = f"**Step {step['num']} of {visualizer.total_steps()-1}:** {step['msg']}"
    
    # STEP 4: Return updates for all UI components
    return (
        0,  # Set step_index to 0 (start at beginning)
        status,  # Update status message
        visual,  # Update visual display
        legend,  # Show color legend
        gr.update(visible=True, minimum=0, maximum=visualizer.total_steps()-1, value=0),  # Show slider
        gr.update(visible=True, interactive=False),  # Show prev button (disabled at start)
        gr.update(visible=True, interactive=True),   # Show next button (enabled)
        gr.update(visible=True),  # Show "all steps" button
        gr.update(visible=True)   # Show reset button
    )


def show_step(step_idx):
    """
    Display a specific step in the sorting process.
    
    This function is called when:
    - The slider is moved
    - The next/previous buttons are clicked
    
    Args:
        step_idx (int): Index of the step to display
        
    Returns:
        tuple: (status message, visual HTML, prev button state, next button state)
    """
    step_idx = int(step_idx)  # Ensure it's an integer
    
    # Validate step index
    if step_idx < 0 or step_idx >= visualizer.total_steps():
        return "Invalid step", "", gr.update(interactive=False), gr.update(interactive=False)
    
    # Get the step data
    step = visualizer.get_step(step_idx)
    
    # Generate visual representation
    visual = make_visual(step['arr'], step['cmp'], step['swap'])
    
    # Create status message showing current position
    status = f"**Step {step['num']} of {visualizer.total_steps()-1}:** {step['msg']}"
    
    # Enable/disable navigation buttons based on position
    prev_enabled = step_idx > 0  # Can go back if not at start
    next_enabled = step_idx < visualizer.total_steps() - 1  # Can go forward if not at end
    
    return status, visual, gr.update(interactive=prev_enabled), gr.update(interactive=next_enabled)


def next_clicked(current_idx):
    """
    Handle the Next button click.
    
    This is a critical function that allows users to step through
    the sorting process one operation at a time.
    
    Args:
        current_idx (int): Current step index
        
    Returns:
        tuple: (new index, status, visual, prev button state, next button state)
    """
    # Calculate the next step index
    new_idx = int(current_idx) + 1
    
    # Don't go past the last step
    if new_idx >= visualizer.total_steps():
        new_idx = visualizer.total_steps() - 1
    
    # Debug output to console (helpful for troubleshooting)
    print(f"Next: {current_idx} -> {new_idx}")
    
    # Get display updates for the new step
    status, visual, prev_btn, next_btn = show_step(new_idx)
    
    # Return new index along with display updates
    # The new_idx updates the step_index State, triggering proper synchronization
    return new_idx, status, visual, prev_btn, next_btn


def prev_clicked(current_idx):
    """
    Handle the Previous button click.
    
    Allows users to go back and review earlier steps in the sorting process.
    
    Args:
        current_idx (int): Current step index
        
    Returns:
        tuple: (new index, status, visual, prev button state, next button state)
    """
    # Calculate the previous step index
    new_idx = int(current_idx) - 1
    
    # Don't go before the first step
    if new_idx < 0:
        new_idx = 0
    
    # Debug output
    print(f"Prev: {current_idx} -> {new_idx}")
    
    # Get display updates for the new step
    status, visual, prev_btn, next_btn = show_step(new_idx)
    
    return new_idx, status, visual, prev_btn, next_btn


def show_all():
    """
    Display all sorting steps in text format.
    
    This provides a complete log of the entire sorting process,
    useful for:
    - Understanding the full algorithm flow
    - Verifying correctness
    - Documenting the sorting process
    
    Returns:
        str: Formatted text with all steps
    """
    # Check if sorting has been performed
    if not visualizer.steps:
        return "No sorting in progress"
    
    # Build formatted output
    output = "=" * 80 + "\n"
    output += "COMPLETE BUBBLE SORT PROCESS\n"
    output += "=" * 80 + "\n\n"
    
    # Iterate through all steps and format each one
    for step in visualizer.steps:
        output += f"STEP {step['num']}: {step['msg']}\n"
        output += f"Array: {step['arr']}\n"
        
        # Show comparison details if applicable
        if step['cmp']:
            output += f"Comparing: {step['cmp']}\n"
        
        # Highlight swap operations
        if step['swap']:
            output += ">>> SWAP <<<\n"
        
        output += "-" * 80 + "\n"
    
    return output


def reset():
    """
    Reset the visualizer to initial state.
    
    This clears all sorting data and hides controls,
    allowing the user to start over with new input.
    
    Returns:
        tuple: Updates to reset all UI components
    """
    # Clear the visualizer's internal state
    visualizer.steps = []
    visualizer.current_step = 0
    
    # Return updates to reset all UI components
    return (
        0,  # Reset step_index to 0
        "Enter numbers and click Start",  # Reset status message
        "",  # Clear visual display
        "",  # Clear legend
        gr.update(visible=False, value=0),  # Hide and reset slider
        gr.update(visible=False),  # Hide prev button
        gr.update(visible=False),  # Hide next button
        gr.update(visible=False),  # Hide show all button
        gr.update(visible=False),  # Hide reset button
        "",  # Clear input box
        ""   # Clear all steps log
    )


# ============================================================================
# BUILD THE GRADIO USER INTERFACE
# ============================================================================

with gr.Blocks(title="Bubble Sort") as app:
    """
    Main Gradio application interface.
    
    Layout:
    - Left column: Input and controls
    - Right column: Visualization and output
    
    Components are organized hierarchically and connected through event handlers.
    """
    
    # STATE MANAGEMENT
    # This State component persists the current step index across interactions
    step_index = gr.State(0)
    
    # HEADER
    gr.Markdown("# 🔄 Bubble Sort Visualizer\n### Click Next to see each step")
    
    # MAIN LAYOUT: Two columns
    with gr.Row():
        # ==================== LEFT COLUMN ====================
        with gr.Column(scale=1):
            gr.Markdown("### Input")
            
            # Input textbox for comma-separated numbers
            input_box = gr.Textbox(
                label="Numbers (comma-separated)", 
                placeholder="1, 2, 3, 4", 
                lines=2
            )
            
            # Start button to begin sorting
            start_btn = gr.Button("▶ Start", variant="primary", size="lg")
            
            gr.Markdown("### Controls")
            
            # Slider for manual navigation through steps
            # Initially hidden, shown after sorting starts
            slider = gr.Slider(0, 10, 0, step=1, label="Step", visible=False)
            
            # Navigation buttons
            with gr.Row():
                prev_btn = gr.Button("⬅ Prev", visible=False)
                next_btn = gr.Button("Next ➡", visible=False, variant="primary")
            
            # Additional controls
            with gr.Row():
                all_btn = gr.Button("📜 All Steps", visible=False)
                reset_btn = gr.Button("🔄 Reset", visible=False)
            
            # Example inputs for quick testing
            gr.Examples([["1, 2, 3, 4"], ["5, 2, 8, 1"]], input_box)
        
        # ==================== RIGHT COLUMN ====================
        with gr.Column(scale=2):
            gr.Markdown("### Visualization")
            
            # Status display showing current step information
            status_box = gr.Markdown("Enter numbers and click Start")
            
            # Visual array representation (HTML boxes)
            visual_box = gr.HTML("")
            
            # Color legend
            legend_box = gr.HTML("")
            
            # Expandable section for complete step log
            with gr.Accordion("All Steps", open=False):
                all_box = gr.Textbox(label="Log", lines=20)
    
    # ============================================================================
    # EVENT HANDLERS - Connect UI components to functions
    # ============================================================================
    
    # START BUTTON: Initialize sorting process
    start_btn.click(
        start_sorting,
        inputs=[input_box],
        outputs=[step_index, status_box, visual_box, legend_box, slider, prev_btn, next_btn, all_btn, reset_btn]
    )
    
    # SLIDER: Manual step navigation
    slider.change(
        show_step,
        inputs=[slider],
        outputs=[status_box, visual_box, prev_btn, next_btn]
    )
    
    # NEXT BUTTON: Advance to next step
    # This is the primary navigation method for step-by-step viewing
    next_btn.click(
        next_clicked,
        inputs=[step_index],
        outputs=[step_index, status_box, visual_box, prev_btn, next_btn]
    )
    
    # PREVIOUS BUTTON: Go back to previous step
    prev_btn.click(
        prev_clicked,
        inputs=[step_index],
        outputs=[step_index, status_box, visual_box, prev_btn, next_btn]
    )
    
    # SHOW ALL BUTTON: Display complete text log
    all_btn.click(show_all, outputs=[all_box])
    
    # RESET BUTTON: Clear everything and start over
    reset_btn.click(
        reset,
        outputs=[step_index, status_box, visual_box, legend_box, slider, prev_btn, next_btn, all_btn, reset_btn, input_box, all_box]
    )


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Launch the Gradio application.
    
    The app will start a local web server and open in the default browser.
    For Hugging Face deployment, the server configuration is automatic.
    """
    app.launch()
