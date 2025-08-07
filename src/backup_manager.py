import shutil
import json
import os
from datetime import datetime
from pathlib import Path

class BackupManager:
    def __init__(self, backup_dir='backups'):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def create_backup(self, files_to_backup=None):
        """Create a backup of important files."""
        if files_to_backup is None:
            files_to_backup = ['links.db', 'config.json']
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f'backup_{timestamp}'
        backup_path.mkdir(exist_ok=True)
        
        backed_up_files = []
        for file_path in files_to_backup:
            if os.path.exists(file_path):
                shutil.copy2(file_path, backup_path / Path(file_path).name)
                backed_up_files.append(file_path)
        
        # Create backup metadata
        metadata = {
            'timestamp': timestamp,
            'files': backed_up_files,
            'created_at': datetime.now().isoformat()
        }
        
        with open(backup_path / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return str(backup_path)

    def list_backups(self):
        """List all available backups."""
        backups = []
        for backup_dir in self.backup_dir.iterdir():
            if backup_dir.is_dir() and backup_dir.name.startswith('backup_'):
                metadata_file = backup_dir / 'metadata.json'
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    backups.append({
                        'path': str(backup_dir),
                        'timestamp': metadata['timestamp'],
                        'created_at': metadata['created_at'],
                        'files': metadata['files']
                    })
        
        return sorted(backups, key=lambda x: x['timestamp'], reverse=True)

    def restore_backup(self, backup_path):
        """Restore files from a backup."""
        backup_path = Path(backup_path)
        metadata_file = backup_path / 'metadata.json'
        
        if not metadata_file.exists():
            raise Exception("Invalid backup directory")
        
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        restored_files = []
        for file_name in metadata['files']:
            backup_file = backup_path / Path(file_name).name
            if backup_file.exists():
                shutil.copy2(backup_file, file_name)
                restored_files.append(file_name)
        
        return restored_files

    def delete_backup(self, backup_path):
        """Delete a backup."""
        shutil.rmtree(backup_path)
        return True

    def cleanup_old_backups(self, keep_count=5):
        """Keep only the most recent backups."""
        backups = self.list_backups()
        if len(backups) > keep_count:
            for backup in backups[keep_count:]:
                self.delete_backup(backup['path'])
