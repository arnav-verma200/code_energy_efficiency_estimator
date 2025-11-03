#!/usr/bin/env python3
"""
Energy Prediction CLI Tool
Analyzes Python scripts and predicts energy consumption

Usage:
    python predict_energy.py script.py
    python predict_energy.py script.py --functions
    python predict_energy.py script.py --functions --detailed
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

class EnergyPredictor:
    def __init__(self, model_path=None):
        """Initialize predictor and load model"""
        self.model_loaded = False
        self.model = None
        
        # FIX: Use absolute path relative to THIS script's location
        if model_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(script_dir, "models", "energy_model.pkl")
        
        print(f"🔍 Looking for model at: {model_path}")  # Debug info
        
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                self.model_loaded = True
                print("✅ Model loaded successfully\n")
            except Exception as e:
                print(f"⚠️  Error loading model: {e}")
                print("   Using estimation formulas instead.\n")
        else:
            print("⚠️  No trained model found. Using estimation formulas.")
            print(f"   Expected location: {model_path}\n")
    
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
    
    def predict_energy(self, cpu: float, memory: float, exec_time: float) -> float:
        """Predict energy cost from metrics"""
        if self.model_loaded:
            return self.model.predict([[cpu, memory, exec_time]])[0]
        else:
            # Fallback formula
            return (cpu * 0.5) + (memory * 0.3) + (exec_time * 100 * 0.2)
    
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
            
            # Measure execution
            start_time = time.time()
            cpu_before = psutil.cpu_percent(interval=0.1)
            mem_before = psutil.Process().memory_info().rss / 1024 / 1024
            
            try:
                func()
            except TypeError:
                # Function needs arguments - estimate from AST
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
                    # Count complexity indicators
                    loops = sum(1 for n in ast.walk(node) if isinstance(n, (ast.For, ast.While)))
                    recursion = sum(1 for n in ast.walk(node) 
                                  if isinstance(n, ast.Call) and hasattr(n.func, 'id') 
                                  and n.func.id == func_name)
                    lines = len(node.body)
                    
                    # Rough estimates
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
        
        # Rating
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
        
        # Sort by energy (highest first)
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
        
        # Optimization suggestions
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
    
    def analyze(self, script_path: str, analyze_functions: bool = False, detailed: bool = False):
        """Main analysis entry point"""
        if not os.path.exists(script_path):
            print(f"❌ Error: File '{script_path}' not found.")
            return
        
        # Analyze script
        print("⏳ Analyzing script...\n")
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
        
        # Show detailed output
        if detailed:
            if metrics.get("stdout"):
                print("\n📤 Script Output:")
                print("-" * 70)
                print(metrics["stdout"][:500])
            if metrics.get("stderr"):
                print("\n⚠️  Errors:")
                print(metrics["stderr"][:500])
        
        # Analyze functions
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
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Energy Prediction Tool")
        print("\nUsage:")
        print("  python predict_energy.py <script.py>")
        print("  python predict_energy.py <script.py> --functions")
        print("  python predict_energy.py <script.py> --functions --detailed")
        print("\nOptions:")
        print("  --functions    Analyze individual functions")
        print("  --detailed     Show detailed output and errors")
        sys.exit(1)
    
    script_path = sys.argv[1]
    analyze_functions = "--functions" in sys.argv
    detailed = "--detailed" in sys.argv
    
    predictor = EnergyPredictor()
    predictor.analyze(script_path, analyze_functions, detailed)

if __name__ == "__main__":
    main()