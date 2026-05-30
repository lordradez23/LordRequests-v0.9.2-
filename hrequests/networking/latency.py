'''
Global Latency Map
~~~~~~~~~~~~~~~~~~

Benchmarking tool for measuring proxy latency across global endpoints.
'''

import time
from typing import List, Dict, Optional
import hrequests
from gevent.pool import Pool

class LatencyMap:
    DEFAULT_TARGETS = [
        'https://www.google.com',
        'https://www.amazon.com',
        'https://www.baidu.com',
        'https://www.cloudflare.com'
    ]

    def __init__(self, proxies: List[str], targets: Optional[List[str]] = None):
        self.proxies = proxies
        self.targets = targets or self.DEFAULT_TARGETS
        self.results: Dict[str, Dict[str, float]] = {}

    def _test_proxy(self, proxy: str):
        self.results[proxy] = {}
        for target in self.targets:
            try:
                start = time.time()
                # Use a small timeout for benchmarking
                resp = hrequests.get(target, proxy=proxy, timeout=5)
                latency = (time.time() - start) * 1000 # ms
                self.results[proxy][target] = round(latency, 2)
            except Exception:
                self.results[proxy][target] = -1 # Failure

    def run_benchmark(self, concurrency: int = 10):
        '''Runs the benchmark across all proxies.'''
        pool = Pool(concurrency)
        for proxy in self.proxies:
            pool.spawn(self._test_proxy, proxy)
        pool.join()
        return self.results

    def get_best_proxy(self, target: Optional[str] = None) -> Optional[str]:
        '''Returns the proxy with the lowest average latency or lowest latency to a specific target.'''
        if not self.results:
            return None
        
        scores = {}
        for proxy, metrics in self.results.items():
            valid_latencies = [l for l in metrics.values() if l > 0]
            if not valid_latencies:
                continue
            
            if target:
                scores[proxy] = metrics.get(target, float('inf'))
            else:
                scores[proxy] = sum(valid_latencies) / len(valid_latencies)
        
        if not scores:
            return None
            
        return min(scores, key=scores.get)

    def print_report(self):
        '''Prints a formatted report of the latency map.'''
        from rich.console import Console
        from rich.table import Table
        
        console = Console()
        table = Table(title="Global Latency Map (ms)")
        
        table.add_column("Proxy", style="cyan")
        for target in self.targets:
            table.add_column(target, justify="right")
            
        for proxy, metrics in self.results.items():
            row = [proxy]
            for target in self.targets:
                val = metrics.get(target, -1)
                if val == -1:
                    row.append("[red]FAIL[/red]")
                elif val < 200:
                    row.append(f"[green]{val}[/green]")
                elif val < 500:
                    row.append(f"[yellow]{val}[/yellow]")
                else:
                    row.append(f"[red]{val}[/red]")
            table.add_row(*row)
            
        console.print(table)
