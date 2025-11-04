#!/usr/bin/env python3
"""
Complete Energy Analysis Tool - All-in-One

Usage:
    predict_energy.py                         # Show system stats
    predict_energy.py script.py               # Basic analysis
    predict_energy.py script.py --functions   # With function breakdown
    predict_energy.py --live                  # Monitor running process
    predict_energy.py --stats                 # Quick system overview
"""

import psutil
import subprocess
import time
import joblib
import sys
import os
import ast
import cProfile
from typing import Dict, List, Optional

class CompleteEnergyAnalyzer:
    def __init__(self, model_path="models/energy_model.pkl"):
        """Initialize analyzer and load model"""
        self.model_loaded = False
        self.model = None
        self.model_path = model_path
        
        # Try to load model from multiple locations
        possible_paths = [
            model_path,
            "models/energy_model.pkl",
            os.path.join(os.path.dirname(__file__), "models/energy_model.pkl"),
            os.path.expanduser("~/.energy_analyzer/energy_model.pkl"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    self.model = joblib.load(path)
                    self.model_loaded = True
                    self.model_path = path
                    break
                except:
                    continue
        
        if not self.model_loaded:
            print("⚠️  No trained model found. Using estimation formulas.\n")
    
    def predict_energy(self, cpu: float, memory: float, exec_time: float) -> float:
        """Predict energy cost from metrics"""
        if self.model_loaded:
            return self.model.predict([[cpu, memory, exec_time]])[0]
        else:
            return (cpu * 0.5) + (memory * 0.3) + (exec_time * 100 * 0.2)
    
    # ========== SYSTEM STATS MODE ==========
    def get_python_processes(self):
        """Get all running Python processes"""
        current_pid = os.getpid()
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
            try:
                if 'python' in proc.info['name'].lower() and proc.info['pid'] != current_pid:
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline and len(cmdline) > 1:
                        processes.append({
                            'pid': proc.info['pid'],
                            'script': cmdline[1],
                            'process': proc
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return processes
    
    def show_system_stats(self):
        """Show system-wide energy statistics"""
        print("=" * 70)
        print("⚡ SYSTEM ENERGY STATS")
        print("=" * 70)
        print()
        
        # System overview
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        mem_used = mem.used / 1024 / 1024 / 1024
        
        print("💻 System Overview:")
        print(f"   CPU Usage:       {cpu_percent:>8.2f}%")
        print(f"   Memory Usage:    {mem.percent:>8.2f}%")
        print(f"   Memory Used:     {mem_used:>8.2f} GB")
        print()
        
        # Python processes
        python_procs = self.get_python_processes()
        
        if python_procs:
            print(f"🐍 Active Python Processes: {len(python_procs)}")
            print("-" * 70)
            
            total_energy = 0
            for proc_info in python_procs[:5]:
                proc = proc_info['process']
                script_name = os.path.basename(proc_info['script'])
                
                try:
                    cpu = proc.cpu_percent(interval=0.5)
                    mem = proc.memory_info().rss / 1024 / 1024
                    energy = self.predict_energy(cpu, mem, 1)
                    total_energy += energy
                    
                    icon = "🔥" if energy > 30 else "⚡" if energy > 15 else "✅"
                    print(f"{icon} {script_name[:40]:40s} | "
                          f"CPU: {cpu:5.1f}% | "
                          f"Mem: {mem:6.1f}MB | "
                          f"Energy: {energy:5.1f}")
                except:
                    continue
            
            if len(python_procs) > 5:
                print(f"\n   ... and {len(python_procs) - 5} more process(es)")
            
            print("-" * 70)
            print(f"💰 Total Python Energy:  {total_energy:.2f} units")
            print(f"💵 Estimated Cost:       ${total_energy * 0.01:.4f}")
        else:
            print("🐍 No other Python processes running")
        
        print()
        if self.model_loaded:
            print(f"🤖 Model: Loaded from {os.path.basename(self.model_path)}")
        print("=" * 70)
    
    # ========== LIVE MONITORING MODE ==========
    def monitor_live_process(self, duration=10):
        """Monitor a live Python process in real-time"""
        processes = self.get_python_processes()
        
        if not processes:
            print("=" * 70)
            print("❌ No Python processes found running.")
            print("=" * 70)
            print("\nTip: Start your Python script in another terminal first.")
            print("Example: python your_script.py &")
            return
        
        print("=" * 70)
        print("🔴 LIVE ENERGY MONITORING")
        print("=" * 70)
        print()
        
        # Select process
        if len(processes) > 1:
            print(f"Found {len(processes)} Python processes:\n")
            for idx, p in enumerate(processes, 1):
                print(f"  [{idx}] PID: {p['pid']:6d} - {os.path.basename(p['script'])}")
            print()
            
            try:
                choice = input("Select process number (or Enter for first): ").strip()
                idx = int(choice) - 1 if choice.isdigit() and int(choice) <= len(processes) else 0
                target = processes[idx]
            except (ValueError, IndexError, KeyboardInterrupt):
                print("\nUsing first process...")
                target = processes[0]
        else:
            target = processes[0]
        
        print(f"\n📍 Monitoring: {os.path.basename(target['script'])} (PID: {target['pid']})")
        print(f"⏱️  Duration: {duration} seconds\n")
        print("-" * 70)
        
        proc = target['process']
        measurements = []
        
        try:
            for i in range(duration):
                try:
                    cpu = proc.cpu_percent(interval=1)
                    mem = proc.memory_info().rss / 1024 / 1024
                    measurements.append({'cpu': cpu, 'memory': mem})
                    
                    # Progress bar
                    bar = "█" * (i + 1) + "░" * (duration - i - 1)
                    print(f"\r[{bar}] {i+1}/{duration}s | "
                          f"CPU: {cpu:6.2f}% | "
                          f"Memory: {mem:8.2f}MB", end='', flush=True)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    print("\n\n⚠️  Process terminated.")
                    break
            
            print("\n" + "-" * 70)
            
            if measurements:
                # Calculate results
                avg_cpu = sum(m['cpu'] for m in measurements) / len(measurements)
                avg_mem = sum(m['memory'] for m in measurements) / len(measurements)
                energy = self.predict_energy(avg_cpu, avg_mem, duration)
                
                print("\n📊 Monitoring Results:")
                print(f"   Average CPU:     {avg_cpu:>8.2f}%")
                print(f"   Average Memory:  {avg_mem:>8.2f} MB")
                print(f"   Duration:        {duration:>8.2f}s")
                print(f"\n⚡ Energy Cost:      {energy:>8.2f} units")
                print(f"💵 Estimated Cost:   ${energy * 0.01:>8.4f}")
                
                # Rating
                if energy < 20:
                    print("\n✅ Rating: EXCELLENT - Very efficient")
                elif energy < 40:
                    print("\n✔️  Rating: GOOD - Moderately efficient")
                elif energy < 60:
                    print("\n⚠️  Rating: FAIR - Room for optimization")
                else:
                    print("\n🚨 Rating: POOR - High power consumption")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Monitoring stopped by user.")
        
        print("=" * 70)
    
    # ========== SCRIPT ANALYSIS MODE ==========
    def measure_script_metrics(self, script_path: str) -> Dict:
        """Execute script and measure resource usage"""
        start_time = time.time()
        cpu_before = psutil.cpu_percent(interval=0.1)
        mem_before = psutil.Process().memory_info().rss / 1024 / 1024
        
        try:
            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                timeout=30,
                text=True
            )
            
            cpu_after = psutil.cpu_percent(interval=0.1)
            mem_after = psutil.Process().memory_info().rss / 1024 / 1024
            exec_time = time.time() - start_time
            
            return {
                "cpu_usage": max(cpu_after, cpu_before),
                "memory_usage": max(mem_after - mem_before, 0),
                "exec_time": exec_time,
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"error": "Script timed out (30s limit)"}
        except Exception as e:
            return {"error": f"Execution failed: {str(e)}"}
    
    def extract_functions(self, script_path: str) -> List[str]:
        """Extract function names from script"""
        try:
            with open(script_path, 'r') as f:
                tree = ast.parse(f.read())
            return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        except:
            return []
    
    def analyze_function(self, script_path: str, func_name: str) -> Optional[Dict]:
        """Analyze individual function"""
        try:
            with open(script_path, 'r') as f:
                code = f.read()
            
            namespace = {}
            exec(code, namespace)
            
            if func_name not in namespace:
                return None
            
            func = namespace[func_name]
            
            start_time = time.time()
            cpu_before = psutil.cpu_percent(interval=0.1)
            mem_before = psutil.Process().memory_info().rss / 1024 / 1024
            
            try:
                func()
            except TypeError:
                return self.estimate_function_ast(code, func_name)
            except:
                return None
            
            cpu_after = psutil.cpu_percent(interval=0.1)
            mem_after = psutil.Process().memory_info().rss / 1024 / 1024
            exec_time = time.time() - start_time
            
            cpu_usage = max(cpu_after - cpu_before, 0)
            memory_usage = max(mem_after - mem_before, 0)
            energy = self.predict_energy(cpu_usage, memory_usage, exec_time)
            
            return {
                "function": func_name,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "exec_time": exec_time,
                "energy": energy,
                "estimated": False
            }
        except:
            return None
    
    def estimate_function_ast(self, code: str, func_name: str) -> Optional[Dict]:
        """Estimate function metrics from static analysis"""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == func_name:
                    loops = sum(1 for n in ast.walk(node) if isinstance(n, (ast.For, ast.While)))
                    recursion = sum(1 for n in ast.walk(node) 
                                  if isinstance(n, ast.Call) and hasattr(n.func, 'id') 
                                  and n.func.id == func_name)
                    lines = len(node.body)
                    
                    cpu_est = loops * 5 + recursion * 10 + lines * 0.5
                    mem_est = lines * 0.2
                    time_est = (loops * 0.1 + recursion * 0.5) / 10
                    
                    energy = self.predict_energy(cpu_est, mem_est, time_est)
                    
                    return {
                        "function": func_name,
                        "cpu_usage": cpu_est,
                        "memory_usage": mem_est,
                        "exec_time": time_est,
                        "energy": energy,
                        "estimated": True
                    }
        except:
            pass
        return None
    
    def print_script_report(self, script_path: str, metrics: Dict, energy: float):
        """Print script-level analysis report"""
        print("=" * 70)
        print("🔋 ENERGY EFFICIENCY REPORT")
        print("=" * 70)
        print(f"\n📄 Script: {os.path.basename(script_path)}")
        print(f"📍 Path: {os.path.abspath(script_path)}\n")
        
        print("📊 Metrics:")
        print(f"   CPU usage:      {metrics['cpu_usage']:>8.2f}%")
        print(f"   Memory usage:   {metrics['memory_usage']:>8.2f} MB")
        print(f"   Execution time: {metrics['exec_time']:>8.4f}s\n")
        
        print(f"⚡ Predicted Energy Cost: {energy:.2f} units")
        print(f"💵 Estimated Cost: ${energy * 0.01:.4f}\n")
        
        if energy < 20:
            print("✅ Rating: EXCELLENT - Very efficient code")
        elif energy < 40:
            print("✔️  Rating: GOOD - Moderately efficient")
        elif energy < 60:
            print("⚠️  Rating: FAIR - Room for optimization")
        else:
            print("🚨 Rating: POOR - High power consumption")
        
        print("=" * 70)
    
    def print_function_report(self, results: List[Dict]):
        """Print function-level analysis report"""
        if not results:
            print("\n⚠️  No functions found or analyzed.")
            return
        
        print("\n" + "=" * 70)
        print("🔍 FUNCTION-LEVEL ANALYSIS")
        print("=" * 70 + "\n")
        
        sorted_results = sorted(results, key=lambda x: x['energy'], reverse=True)
        total_energy = sum(r['energy'] for r in sorted_results)
        
        print("Function Summary:")
        print("-" * 70)
        
        for r in sorted_results:
            icon = "🚨" if r['energy'] > 50 else "⚠️ " if r['energy'] > 20 else "✅"
            tag = " [estimated]" if r.get('estimated', False) else ""
            
            print(f"\n{r['function']}() → {r['energy']:.2f} units {icon}{tag}")
            print(f"   CPU: {r['cpu_usage']:.2f}% | "
                  f"Memory: {r['memory_usage']:.2f}MB | "
                  f"Time: {r['exec_time']:.4f}s")
        
        print("\n" + "-" * 70)
        print(f"💰 Total Function Energy: {total_energy:.2f} units")
        print(f"💵 Total Cost: ${total_energy * 0.01:.4f}")
        
        high_energy = [r for r in sorted_results if r['energy'] > 50]
        if high_energy:
            print("\n🔧 OPTIMIZATION SUGGESTIONS:")
            for func in high_energy:
                print(f"\n   🎯 {func['function']}():")
                print(f"      • Reduce computational complexity")
                print(f"      • Use built-in functions and libraries")
                print(f"      • Consider caching or memoization")
                print(f"      • Optimize loops and data structures")
        else:
            print("\n✨ All functions are energy-efficient!")
        
        print("=" * 70)
    
    def analyze_script(self, script_path: str, analyze_functions: bool = False, detailed: bool = False):
        """Analyze a specific script"""
        if not os.path.exists(script_path):
            print(f"❌ Error: File '{script_path}' not found.")
            return
        
        print("\n⏳ Analyzing script...\n")
        metrics = self.measure_script_metrics(script_path)
        
        if "error" in metrics:
            print(f"❌ {metrics['error']}")
            return
        
        energy = self.predict_energy(
            metrics['cpu_usage'],
            metrics['memory_usage'],
            metrics['exec_time']
        )
        
        self.print_script_report(script_path, metrics, energy)
        
        if detailed:
            if metrics.get("stdout"):
                print("\n📤 Script Output:")
                print("-" * 70)
                print(metrics["stdout"][:500])
            if metrics.get("stderr"):
                print("\n⚠️  Errors:")
                print(metrics["stderr"][:500])
        
        if analyze_functions:
            print("\n⏳ Analyzing individual functions...\n")
            functions = self.extract_functions(script_path)
            
            if functions:
                results = []
                for func_name in functions:
                    result = self.analyze_function(script_path, func_name)
                    if result:
                        results.append(result)
                
                self.print_function_report(results)
            else:
                print("⚠️  No functions found in script.")

def main():
    """Main CLI entry point"""
    
    # Parse arguments
    if len(sys.argv) == 1:
        # No arguments - show system stats
        print("\n✅ Energy Analyzer Ready\n")
        analyzer = CompleteEnergyAnalyzer()
        analyzer.show_system_stats()
        return
    
    # Help
    if sys.argv[1] in ["--help", "-h", "help"]:
        print("""
⚡ Complete Energy Analyzer

Usage:
    predict_energy.py                         # Show system stats
    predict_energy.py script.py               # Analyze script
    predict_energy.py script.py --functions   # With function breakdown
    predict_energy.py script.py --detailed    # Show script output
    predict_energy.py --live [seconds]        # Monitor running process
    predict_energy.py --stats                 # System overview

Examples:
    predict_energy.py                         # Quick system check
    predict_energy.py my_script.py            # Analyze a script
    predict_energy.py my_script.py --functions # Full breakdown
    predict_energy.py --live 30               # Monitor for 30s
        """)
        return
    
    # Live monitoring mode
    if sys.argv[1] == "--live":
        duration = 10
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            duration = int(sys.argv[2])
        print("\n✅ Energy Analyzer Ready\n")
        analyzer = CompleteEnergyAnalyzer()
        analyzer.monitor_live_process(duration)
        return
    
    # Stats mode
    if sys.argv[1] == "--stats":
        print("\n✅ Energy Analyzer Ready\n")
        analyzer = CompleteEnergyAnalyzer()
        analyzer.show_system_stats()
        return
    
    # Script analysis mode
    script_path = sys.argv[1]
    analyze_functions = "--functions" in sys.argv
    detailed = "--detailed" in sys.argv
    
    print("\n✅ Energy Analyzer Ready")
    analyzer = CompleteEnergyAnalyzer()
    analyzer.analyze_script(script_path, analyze_functions, detailed)

if __name__ == "__main__":
    main()