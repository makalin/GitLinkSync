# GitLinkSync

![GitLinkSync Logo](logo.png)

*A tool to extract GitHub user links from X posts and automate follow-back actions, now with advanced automation, analytics, dashboard, CLI, and more!*

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [CLI Usage](#cli-usage)
- [Web Dashboard](#web-dashboard)
- [Scheduler](#scheduler)
- [Notifications](#notifications)
- [Analytics & Stats](#analytics--stats)
- [Security](#security)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview
GitLinkSync is an innovative Python-based project designed to extract GitHub profile links from X posts (e.g., tweets like the one from @GithubProjects) and automate follow-back actions on GitHub. This tool addresses the challenge of connecting with developers in a JavaScript-disabled environment by leveraging server-side scraping and the GitHub API. Ideal for open-source enthusiasts and developers looking to build their network!

## Features
- Extracts GitHub profile URLs from X posts using web scraping or the X API.
- Automates follow-back actions on GitHub using the GitHub API.
- Multi-account support for GitHub and X, with account rotation.
- Handles JavaScript-disabled browser scenarios with server-side rendering.
- Stores extracted links in a local database for future reference.
- CLI utilities for scraping, following, exporting/importing, reviewing, and stats.
- Web dashboard (Flask) to view links, follow status, and analytics.
- Scheduler (APScheduler) for automated periodic scraping and follow-back.
- Notification support (email, Telegram, Slack) for new links and follow-backs.
- Link validation and enrichment (check if GitHub links are valid, fetch user info).
- Advanced rate limit handling and retry logic.
- Export/import utilities (CSV/JSON).
- Structured logging and audit trail.
- Manual review tool for approving/rejecting links before follow-back.
- Statistics and analytics (number of links, follow-back rate, top posters, etc.).
- Security: encrypt sensitive config values, environment variable support.
- Compliant with GitHub API rate limits and X's terms of service.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/makalin/GitLinkSync.git
   cd GitLinkSync
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Usage
1. Configure your GitHub API token and X credentials in the `config.json` file (see [Configuration](#configuration)).
2. Run the CLI for scraping, following, exporting, importing, reviewing, and stats:
   ```bash
   python -m src.cli scrape
   python -m src.cli follow
   python -m src.cli export --format csv
   python -m src.cli import --format json --file links.json
   python -m src.cli review
   python -m src.cli stats
   ```
3. Start the web dashboard:
   ```bash
   python -m src.dashboard
   ```
4. Start the scheduler for automated scraping/follow-back:
   ```bash
   python -m src.scheduler
   ```

## CLI Usage
- `scrape`: Scrape X posts and extract GitHub links.
- `follow`: Follow back all users in the database.
- `export`: Export links to CSV or JSON.
- `import`: Import links from CSV or JSON.
- `review`: Manually review and approve/reject links before follow-back.
- `stats`: Show statistics and analytics.

Example:
```bash
python -m src.cli export --format json --file mylinks.json
```

## Web Dashboard
- Start with `python -m src.dashboard` and visit `http://localhost:5000`.
- View all extracted links, follow status, and analytics in your browser.

## Scheduler
- Start with `python -m src.scheduler` to run scraping and follow-back jobs at regular intervals (default: scrape every 60 min, follow every 120 min).

## Notifications
- Configure email, Telegram, or Slack notifications in your custom scripts or extend `src/notifications.py`.
- Get notified when new links are found or follow-backs are performed.

## Analytics & Stats
- View stats in the dashboard or via CLI:
  - Total links
  - Followed/unfollowed
  - Follow-back rate
  - (Extend for more analytics as needed)

## Security
- Sensitive config values can be encrypted using `src/security.py` (see code for details).
- Environment variable support for secrets.

## Prerequisites
- Python 3.8+
- Git
- Internet connection
- A GitHub personal access token (generate at [GitHub Settings](https://github.com/settings/tokens))
- (Optional) A database (e.g., SQLite for local storage)

## Configuration
Create a `config.json` file in the project root with the following structure:
```json
{
  "github_token": "your_github_personal_access_token",
  "x_username": "your_x_username",
  "x_password": "your_x_password",
  "auto_follow": true
}
```
- `github_token`: Required for GitHub API authentication.
- `x_username` and `x_password`: Used for X login (ensure compliance with X's terms).
- `auto_follow`: Set to `true` to enable automatic follow-back.

**Note**: Disable privacy extensions in your browser if scraping issues arise, as suggested by X's error message.

## Contributing
We welcome contributions to enhance GitLinkSync! Here's how you can get involved:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a Pull Request with a clear description of your changes.

### Contributors
- [Mehmet T. AKALIN](https://github.com/makalin) (Project Creator)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
- **X (Twitter)**: [@makalin](https://x.com/makalin)
- **GitHub Issues**: [Open an issue](https://github.com/makalin/GitLinkSync/issues)
- **Email**: makalin@gmail.com

Feel free to reach out with questions, feedback, or collaboration ideas!
