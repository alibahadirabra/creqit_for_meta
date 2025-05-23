#!/usr/bin/env python3
import os
import fileinput
import sys

def replace_in_file(filepath):
    try:
        with fileinput.FileInput(filepath, inplace=True, backup='.bak') as file:
            for line in file:
                # Replace various cases while preserving the original case
                line = line.replace('Frappe', 'Creqit')
                line = line.replace('frappe', 'creqit')
                line = line.replace('FRAPPE', 'CREQIT')
                print(line, end='')
        print(f"Updated {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                replace_in_file(filepath)

if __name__ == "__main__":
    bench_path = "/Users/alibahadirkus/Desktop/creqit_for_meta/creqit_for_meta/creqit-env-3.12/lib/python3.12/site-packages/bench"
    process_directory(bench_path) 