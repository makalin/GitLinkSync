import argparse
from src import main, db, utils, manual_review, analytics

def main_cli():
    parser = argparse.ArgumentParser(description='GitLinkSync CLI')
    parser.add_argument('command', choices=['scrape', 'follow', 'export', 'import', 'review', 'stats'])
    parser.add_argument('--format', choices=['csv', 'json'], default='csv')
    parser.add_argument('--file', help='File for import/export')
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

if __name__ == "__main__":
    main_cli() 