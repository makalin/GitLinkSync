import argparse
from src import main, db, utils, manual_review, analytics, backup_manager, link_validator, data_cleaner, performance_monitor

def main_cli():
    parser = argparse.ArgumentParser(description='GitLinkSync CLI')
    parser.add_argument('command', choices=['scrape', 'follow', 'export', 'import', 'review', 'stats', 'backup', 'validate', 'clean', 'monitor', 'performance'])
    parser.add_argument('--format', choices=['csv', 'json'], default='csv')
    parser.add_argument('--file', help='File for import/export')
    parser.add_argument('--backup-path', help='Backup path for restore/delete operations')
    parser.add_argument('--action', choices=['create', 'list', 'restore', 'delete'], help='Backup action')
    args = parser.parse_args()

    if args.command == 'scrape':
        main.main()
    elif args.command == 'follow':
        main.follow_back_on_github([url for url, _ in db.get_links()])
    elif args.command == 'export':
        links = [url for url, _ in db.get_links()]
        if args.format == 'csv':
            utils.export_links_to_csv(links, args.file or 'links_export.csv')
        else:
            utils.export_links_to_json(links, args.file or 'links_export.json')
    elif args.command == 'import':
        if args.format == 'csv':
            links = utils.import_links_from_csv(args.file or 'links_export.csv')
        else:
            links = utils.import_links_from_json(args.file or 'links_export.json')
        for link in links:
            db.save_link(link)
    elif args.command == 'review':
        manual_review.review_links()
    elif args.command == 'stats':
        print(f"Total links: {analytics.get_total_links()}")
        print(f"Followed: {analytics.get_followed_count()}")
        print(f"Unfollowed: {analytics.get_unfollowed_count()}")
        print(f"Follow-back rate: {analytics.get_follow_back_rate():.2f}%")
    elif args.command == 'backup':
        backup_mgr = backup_manager.BackupManager()
        if args.action == 'create':
            backup_path = backup_mgr.create_backup()
            print(f"Backup created: {backup_path}")
        elif args.action == 'list':
            backups = backup_mgr.list_backups()
            for backup in backups:
                print(f"Backup: {backup['timestamp']} - {backup['path']}")
        elif args.action == 'restore':
            if args.backup_path:
                restored = backup_mgr.restore_backup(args.backup_path)
                print(f"Restored files: {restored}")
        elif args.action == 'delete':
            if args.backup_path:
                backup_mgr.delete_backup(args.backup_path)
                print("Backup deleted")
    elif args.command == 'validate':
        links = [url for url, _ in db.get_links()]
        for link in links:
            is_valid = link_validator.validate_github_link(link)
            print(f"{link}: {'Valid' if is_valid else 'Invalid'}")
    elif args.command == 'clean':
        links = [url for url, _ in db.get_links()]
        cleaned_links = data_cleaner.DataCleaner.remove_duplicates(links)
        print(f"Original: {len(links)}, After cleaning: {len(cleaned_links)}")
    elif args.command == 'monitor':
        monitor = performance_monitor.PerformanceMonitor()
        system_stats = monitor.get_system_stats()
        print(f"CPU Usage: {system_stats['cpu']}%")
        print(f"Memory Usage: {system_stats['memory']['percent']:.2f}%")
        print(f"Disk Usage: {system_stats['disk_usage']}%")
    elif args.command == 'performance':
        monitor = performance_monitor.PerformanceMonitor()
        report = monitor.generate_report()
        print("Performance Report:")
        print(f"System: {report['system']}")
        print(f"API Stats: {report['api_stats']}")

if __name__ == "__main__":
    main_cli() 