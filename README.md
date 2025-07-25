# GitLinkSync

*A tool to extract GitHub user links from X posts and automate follow-back actions.*

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview
GitLinkSync is an innovative Python-based project designed to extract GitHub profile links from X posts (e.g., tweets like the one from @GithubProjects) and automate follow-back actions on GitHub. This tool addresses the challenge of connecting with developers in a JavaScript-disabled environment by leveraging server-side scraping and the GitHub API. Ideal for open-source enthusiasts and developers looking to build their network!

## Features
- Extracts GitHub profile URLs from X posts using web scraping.
- Automates follow-back actions on GitHub using the GitHub API.
- Handles JavaScript-disabled browser scenarios with server-side rendering.
- Stores extracted links in a local database for future reference.
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
2. Run the script to scrape X posts and extract GitHub links:
   ```bash
   python main.py
   ```
3. Review the extracted links in the `links.db` database or follow back automatically by enabling the follow-back feature:
   ```bash
   python follow_back.py
   ```

### Example Output
- Extracted link: `https://github.com/thevinodpatidar`
- Follow-back status: `Success` or `Rate limit exceeded`

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
