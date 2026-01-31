"""
视频封面提取模块
"""

import os
import subprocess
from pathlib import Path


class VideoCoverExtractor:
    """视频封面提取器"""
    
    # 支持的视频格式
    VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v', '.3gp', '.ts'}
    
    @staticmethod
    def get_video_files(path):
        """
        获取指定路径下的所有视频文件
        如果是文件夹，递归遍历所有子文件夹
        
        Args:
            path: 文件或文件夹路径
            
        Returns:
            list: 视频文件路径列表
        """
        video_files = []
        
        if os.path.isfile(path):
            # 单个文件
            if Path(path).suffix.lower() in VideoCoverExtractor.VIDEO_EXTENSIONS:
                video_files.append(path)
        elif os.path.isdir(path):
            # 文件夹，递归遍历
            for root, dirs, files in os.walk(path):
                for file in files:
                    if Path(file).suffix.lower() in VideoCoverExtractor.VIDEO_EXTENSIONS:
                        video_files.append(os.path.join(root, file))
        
        return video_files
    
    @staticmethod
    def extract_cover(video_path, output_path):
        """
        从视频中提取第一帧作为封面
        
        Args:
            video_path: 视频文件路径
            output_path: 输出图片路径
            
        Returns:
            bool: 是否成功
        """
        try:
            import shutil
            import sys
            
            # 尝试找到 ffmpeg
            ffmpeg_cmd = None
            
            # 1. 先尝试 shutil.which
            ffmpeg_cmd = shutil.which('ffmpeg')
            
            # 2. 如果找不到，尝试常见的 Homebrew 路径
            if not ffmpeg_cmd:
                homebrew_paths = [
                    '/usr/local/bin/ffmpeg',
                    '/opt/homebrew/bin/ffmpeg',
                    '/usr/local/opt/ffmpeg/bin/ffmpeg'
                ]
                for path in homebrew_paths:
                    if os.path.exists(path):
                        ffmpeg_cmd = path
                        break
            
            if not ffmpeg_cmd:
                print("[ERROR] 找不到 ffmpeg，请确保已安装: brew install ffmpeg")
                return False
            
            print(f"[DEBUG] 使用 ffmpeg: {ffmpeg_cmd}")
            
            # 使用 ffmpeg 提取视频第一帧
            cmd = [
                ffmpeg_cmd,
                '-i', video_path,
                '-vframes', '1',
                '-q:v', '2',
                '-y',  # 覆盖输出文件
                output_path
            ]
            
            print(f"[DEBUG] 执行命令: {' '.join(cmd)}")
            
            # 运行命令，抑制输出
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30
            )
            
            print(f"[DEBUG] 返回码: {result.returncode}")
            return result.returncode == 0
        except Exception as e:
            print(f"[ERROR] 提取视频封面失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def extract_covers_batch(video_files, output_folder):
        """
        批量提取视频封面
        
        Args:
            video_files: 视频文件路径列表
            output_folder: 输出文件夹
            
        Returns:
            dict: 包含成功和失败的文件列表
        """
        # 创建输出文件夹
        os.makedirs(output_folder, exist_ok=True)
        
        results = {
            'success': [],
            'failed': []
        }
        
        for video_path in video_files:
            try:
                # 获取视频文件名（不含扩展名）
                video_name = Path(video_path).stem
                
                # 输出图片路径
                output_image = os.path.join(output_folder, f"{video_name}.jpg")
                
                # 提取封面
                if VideoCoverExtractor.extract_cover(video_path, output_image):
                    results['success'].append(video_path)
                else:
                    results['failed'].append(video_path)
            except Exception as e:
                print(f"[ERROR] 处理视频失败: {video_path}, {str(e)}")
                results['failed'].append(video_path)
        
        return results
