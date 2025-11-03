#!/usr/bin/env python3
"""
Energy Data Collection System
Collects script-level and function-level energy metrics
"""

import psutil
import subprocess
import time
import os
import csv
import ast
import cProfile
import pstats
import io
from contextlib import redirect_stdout

class EnergyDataCollector:
    def __init__(self, scripts_folder="test_scripts"):
        self.scripts_folder = scripts_folder
        self.script_results = []
        self.function_results = []
    
    def extract_functions(self, filepath):
        """Extract all function names from a Python file"""
        try:
            with open(filepath, 'r') as f:
                tree = ast.parse(f.read())
            
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
            return functions
        except Exception as e:
            print(f"      Error parsing functions: {e}")
            return []
    
    def profile_function(self, script_path, function_name):
        """Profile a specific function using cProfile"""
        try:
            with open(script_path, 'r') as f:
                code = f.read()
            
            namespace = {}
            exec(code, namespace)
            
            if function_name not in namespace:
                return None
            
            func = namespace[function_name]
            profiler = cProfile.Profile()
            
            # Measure metrics
            start_time = time.time()
            cpu_before = psutil.cpu_percent(interval=0.1)
            mem_before = psutil.Process().memory_info().rss / 1024 / 1024
            
            profiler.enable()
            try:
                func()
            except TypeError:
                # Function needs arguments - skip
                return None
            except Exception as e:
                return None
            profiler.disable()
            
            cpu_after = psutil.cpu_percent(interval=0.1)
            mem_after = psutil.Process().memory_info().rss / 1024 / 1024
            exec_time = time.time() - start_time
            
            cpu_usage = max(cpu_after - cpu_before, 0)
            memory_usage = max(mem_after - mem_before, 0)
            
            # Calculate energy cost
            energy = (cpu_usage * 0.5) + (memory_usage * 0.3) + (exec_time * 100 * 0.2)
            
            return {
                'script': os.path.basename(script_path),
                'function': function_name,
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'exec_time': exec_time,
                'energy_cost': energy
            }
            
        except Exception as e:
            return None
    
    def collect_script_metrics(self, script_path):
        """Collect metrics for entire script"""
        try:
            start_time = time.time()
            cpu_before = psutil.cpu_percent(interval=0.1)
            mem_before = psutil.virtual_memory().percent
            
            # Run script
            result = subprocess.run(
                ["python", script_path], 
                capture_output=True, 
                timeout=10
            )
            
            cpu_after = psutil.cpu_percent(interval=0.1)
            mem_after = psutil.virtual_memory().percent
            exec_time = time.time() - start_time
            
            cpu_usage = max(cpu_after, cpu_before)
            memory_usage = max(mem_after, mem_before)
            
            # Calculate energy
            energy = (cpu_usage * 0.5) + (memory_usage * 0.3) + (exec_time * 100 * 0.2)
            
            return {
                'script': os.path.basename(script_path),
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'exec_time': exec_time,
                'energy_cost': energy
            }
        except subprocess.TimeoutExpired:
            print(f"      ⏱️  Timeout (skipped)")
            return None
        except Exception as e:
            print(f"      ❌ Error: {e}")
            return None
    
    def collect_all_data(self):
        """Collect both script-level and function-level data"""
        print("=" * 70)
        print("🔄 ENERGY DATA COLLECTION")
        print("=" * 70)
        print()
        
        if not os.path.exists(self.scripts_folder):
            print(f"❌ Error: Folder '{self.scripts_folder}' not found!")
            print(f"   Create it and add Python scripts to analyze.")
            return
        
        script_files = [f for f in os.listdir(self.scripts_folder) if f.endswith(".py")]
        
        if not script_files:
            print(f"❌ No Python files found in '{self.scripts_folder}'")
            return
        
        print(f"📂 Found {len(script_files)} scripts to analyze\n")
        
        for idx, file in enumerate(script_files, 1):
            script_path = os.path.join(self.scripts_folder, file)
            print(f"[{idx}/{len(script_files)}] 📄 {file}")
            
            # Collect script-level metrics
            script_metrics = self.collect_script_metrics(script_path)
            if script_metrics:
                self.script_results.append(script_metrics)
                print(f"      ✓ Script: {script_metrics['energy_cost']:.2f} units")
            
            # Extract and profile functions
            functions = self.extract_functions(script_path)
            if functions:
                print(f"      📊 Functions: {len(functions)}")
                for func_name in functions:
                    func_metrics = self.profile_function(script_path, func_name)
                    if func_metrics:
                        self.function_results.append(func_metrics)
                        print(f"         ✓ {func_name}() → {func_metrics['energy_cost']:.2f} units")
            
            print()
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save results to CSV files"""
        print("=" * 70)
        print("💾 SAVING RESULTS")
        print("=" * 70)
        print()
        
        # Create data directory
        os.makedirs("data", exist_ok=True)
        
        # Save script-level data
        if self.script_results:
            script_path = "data/code_metrics.csv"
            with open(script_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=['script', 'cpu_usage', 'memory_usage', 'exec_time', 'energy_cost'])
                writer.writeheader()
                writer.writerows(self.script_results)
            print(f"✅ {script_path} ({len(self.script_results)} records)")
        
        # Save function-level data
        if self.function_results:
            func_path = "data/function_metrics.csv"
            with open(func_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=['script', 'function', 'cpu_usage', 'memory_usage', 'exec_time', 'energy_cost'])
                writer.writeheader()
                writer.writerows(self.function_results)
            print(f"✅ {func_path} ({len(self.function_results)} records)")
        
        if not self.script_results and not self.function_results:
            print("⚠️  No data collected. Check your test scripts.")
        else:
            print()
            print("=" * 70)
            print("✅ DATA COLLECTION COMPLETE!")
            print("=" * 70)
            print()
            print("Next step: Run 'python train_model.py' to train the model")

def main():
    collector = EnergyDataCollector()
    collector.collect_all_data()

if __name__ == "__main__":
    main()