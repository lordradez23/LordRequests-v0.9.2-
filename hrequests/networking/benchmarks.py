'''
Stealth A/B Testing
~~~~~~~~~~~~~~~~~~~

Benchmarking fingerprint/proxy combinations against WAF detection.
'''

import time
from typing import List, Dict, Any, Callable
import hrequests

class StealthBench:
    '''
    Compares the success rates of different request configurations.
    '''
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.results: List[Dict[str, Any]] = []

    def run_benchmark(self, configurations: List[Dict[str, Any]], iterations: int = 10):
        '''
        Runs multiple iterations of each configuration and records success metrics.
        '''
        print(f"Starting Stealth A/B Benchmark against {self.target_url}")
        
        for i, config in enumerate(configurations):
            name = config.get('name', f"Config {i+1}")
            print(f"Testing: {name}...")
            
            success_count = 0
            total_time = 0.0
            
            for _ in range(iterations):
                start = time.time()
                try:
                    # Execute request using provided config
                    resp = hrequests.get(self.target_url, **config.get('kwargs', {}))
                    if resp.status_code == 200 and 'captcha' not in resp.text.lower():
                        success_count += 1
                except Exception:
                    pass
                total_time += (time.time() - start)
                time.sleep(1) # Cooldown
            
            self.results.append({
                'name': name,
                'success_rate': (success_count / iterations) * 100,
                'avg_latency': total_time / iterations,
                'config_summary': str(config.get('kwargs', {}))
            })

    def print_report(self):
        '''
        Prints a summary of the benchmark results.
        '''
        print("\n" + "="*50)
        print(" STEALTH A/B BENCHMARK REPORT")
        print("="*50)
        # Sort results by success rate (highest first)
        for res in sorted(self.results, key=lambda x: x['success_rate'], reverse=True):
            print(f"[{res['name']}]")
            print(f"  Success Rate: {res['success_rate']}%")
            print(f"  Avg Latency:  {res['avg_latency']:.3f}s")
        print("="*50 + "\n")
