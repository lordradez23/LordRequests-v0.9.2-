'''
Video Stream Analyst
~~~~~~~~~~~~~~~~~~~~

Metadata extraction and quality monitoring for scraped video assets.
'''

import subprocess
import json
from typing import Dict, Any, Optional

class VideoAnalyst:
    '''
    Uses ffprobe to analyze video files and streams.
    '''
    @staticmethod
    def get_probe_info(file_path: str) -> Dict[str, Any]:
        '''
        Executes ffprobe to get comprehensive stream metadata.
        '''
        cmd = [
            'ffprobe', 
            '-v', 'quiet', 
            '-print_format', 'json', 
            '-show_format', 
            '-show_streams', 
            file_path
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
            return {"error": f"ffprobe failed or not installed: {str(e)}"}

    @staticmethod
    def get_summary(file_path: str) -> Dict[str, Any]:
        '''
        Returns a simplified summary of video properties.
        '''
        info = VideoAnalyst.get_probe_info(file_path)
        if "error" in info:
            return info
            
        streams = info.get('streams', [])
        video_stream = next((s for s in streams if s['codec_type'] == 'video'), {})
        
        return {
            "duration": float(info.get('format', {}).get('duration', 0)),
            "format": info.get('format', {}).get('format_name', 'unknown'),
            "resolution": f"{video_stream.get('width')}x{video_stream.get('height')}",
            "codec": video_stream.get('codec_name', 'unknown'),
            "bit_rate": int(info.get('format', {}).get('bit_rate', 0))
        }
