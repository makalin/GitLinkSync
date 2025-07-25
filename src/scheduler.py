from apscheduler.schedulers.blocking import BlockingScheduler
from src import main

def schedule_jobs():
    scheduler = BlockingScheduler()
    scheduler.add_job(main.main, 'interval', minutes=60, id='scrape_job')
    scheduler.add_job(lambda: main.follow_back_on_github([url for url, _ in main.db.get_links()]), 'interval', minutes=120, id='follow_job')
    print('Scheduler started. Scraping every 60 min, follow-back every 120 min.')
    scheduler.start()

if __name__ == "__main__":
    schedule_jobs() 