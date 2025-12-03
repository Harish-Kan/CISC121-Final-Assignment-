# Algorithm Name

Bubble Sort 

## Demo video/gif/screenshot of test

https://github.com/user-attachments/assets/a56dc5c4-bc0f-4aca-9cc7-bb2c3ba546fa

## Problem Breakdown & Computational Thinking 

Decomposition : 

Starts off with taking the user’s list of numbers 
Comparing each pair of numbers, with its adjacent element 
If the left one is indeed larger, then it swaps them 
It keeps repeating the passes until no more swaps are needed 
As it outputs the sorted list in the end, it also shows every single step 

Pattern recognition ; 

Bubble Sort 
The algorithm (bubble sort) keeps repeating the same action over and over again until the condition is met 
Compares, possibly swaps, and then moves onto the next pair 
The larger value gets pushed to the end every single time when there is a pass 
The unsorted part, becomes smaller and smaller after every swap 

Abstraction : 

Shown to the user : 
After every single swap, the list 
Which of the 2 elements are being compared to each other 
The step number 
Not shown : 
The loop variables 
Internal Counters 
As well as the memory operations 
Algorithm Design : 

Input : Inside of the Gradio textbox, a list of numbers which are separated by commas 
Processing :  Bubble Sort is run, it then records every comparison as well as swap 
Output : Inside of GUI, it shows every step that the algorithm (bubble sort) takes. And in the end it shows the finalized sorted list 
The user in the end can end up choosing if they want to step through it, or see the full run of it

## Steps to Run

1. Vist the hugging face link, listed under "Hugging Face Link". This is where the application is depolyed
2. Enter the numbers you want to be sorted. These numbers should be seperated by commas. (Example : 1,2,5,-1)
3. Click the "Start" button to begin the sorting.
4. Click next to step through each comparison and swap.
5. Continue pressing stop (repeat step 4) until the list is sorted.
6. Click reset after the list is sorted, if the user wants to input another list. 

## Hugging Face Link

https://huggingface.co/spaces/IkeaHarish/BubbleSort

## Author & Acknowledgment

Karikaran Harish Kandavell 
harish.kandavell@queensu.ca 

AI Level 4 (Claude AI) was used inside of this project 

Python Version: 3.12.11
UI Framework: Gradio

Course information : CISC 121 
