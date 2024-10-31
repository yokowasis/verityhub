# VerityHub

VerityHub is a new social media platform designed from scratch to provide a simple and intuitive interface similar to Mastodon. It allows users to publish articles and status posts effortlessly, with the added capability of semantic textual search to enhance content discoverability.

- **Live Demo**: [VerityHub Live Site](https://verityhub.b.app.web.id/)
- **Repository**: [GitHub - yokowasis/verityhub](https://github.com/yokowasis/verityhub)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Clone the Repository](#1-clone-the-repository)
  - [Configure Environment Variables](#2-configure-environment-variables)
  - [Run with Docker Compose](#3-run-with-docker-compose)
  - [Access the Application](#4-access-the-application)
- [Usage](#usage)
  - [Create an Account](#1-create-an-account)
  - [Log In](#2-log-in)
  - [Post a Status Update](#3-post-a-status-update)
  - [Publish an Article](#4-publish-an-article)
  - [Search for Content](#5-search-for-content)
- [Deployment](#deployment)
  - [Deploying to a Cloud Provider](#deploying-to-a-cloud-provider)
- [Environment Variables](#environment-variables)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User-Friendly Interface**: Simple and intuitive UI similar to Mastodon.
- **Content Publishing**: Users can publish both articles and status posts.
- **Semantic Search**: Enhanced content discoverability through semantic textual search.
- **File Uploads**: Secure file upload handling with validation.
- **Authentication**: Secure user authentication and session management.
- **Dockerized Deployment**: Easy setup and deployment using Docker Compose.

## Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- **Python 3.8+** (if running locally without Docker).
- An account with one of the supported cloud service providers (if deploying to the cloud).
- **OpenAI API Key** for summarization and translation features.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yokowasis/verityhub.git
cd verityhub
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory of the project. This file will hold all the necessary environment variables needed for the application to run.

```env
POSTGRES_HOSTNAME=your_postgres_hostname
POSTGRES_DATABASE=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_PORT=your_postgres_port
SALT=your_secret_salt_for_hashing
TRANSFORMER_MODEL=your_transformer_model_name
OPENAI_MODEL=your_openai_model_name
OPENAI_KEY=your_openai_api_key
```

**Explanation of Environment Variables:**

- `POSTGRES_HOSTNAME`: The hostname of your PostgreSQL database server.
- `POSTGRES_DATABASE`: The name of your PostgreSQL database.
- `POSTGRES_USER`: The username for your PostgreSQL database.
- `POSTGRES_PASSWORD`: The password for your PostgreSQL database.
- `POSTGRES_PORT`: The port number on which your PostgreSQL database is running (default is usually `5432`).
- `SALT`: A secret string used for hashing passwords; it should be kept confidential.
- `TRANSFORMER_MODEL`: The name of the transformer model used for generating embeddings (e.g., `all-MiniLM-L6-v2`).
- `OPENAI_MODEL`: The name of the OpenAI model to use for summarization and translation (e.g., `gpt-3.5-turbo`).
- `OPENAI_KEY`: Your OpenAI API key for accessing OpenAI services.

> **Note**: Ensure that you do not commit your `.env` file to any public repositories, as it contains sensitive information.

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

This command will build the Docker images and start the containers as defined in the `docker-compose.yml` file.

> _Image Placeholder: Screenshot of terminal showing successful Docker Compose build and up command_

### 4. Access the Application

- Open your browser and navigate to `http://localhost:8000`.

> _Image Placeholder: Screenshot of VerityHub homepage_

## Usage

### 1. Create an Account

- Click on the **"Create Account"** button.
- Fill in the signup form with your username, password, full name, and avatar URL.

> _Image Placeholder: Screenshot of the signup form_

### 2. Log In

- After signing up, log in with your credentials.

> _Image Placeholder: Screenshot of the login page_

### 3. Post a Status Update

- On the homepage, write a status update in the post box.
- Click **"Post"** to share it with others.

> _Image Placeholder: Screenshot of creating a new post_

### 4. Publish an Article

- Navigate to the **"New Article"** page.
- Enter the title and content of your article.
- Click **"Publish"** to share it.

> _Image Placeholder: Screenshot of the new article page_

### 5. Search for Content

- Use the search bar to find posts and articles.
- The semantic search feature will return results based on content similarity.

> _Image Placeholder: Screenshot of search results_

## Deployment

### Deploying to a Cloud Provider

#### Supported Providers

- **DigitalOcean**

[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/yokowasis/verityhub/tree/master)

#### Steps

1. **Select a Provider**

   Choose a cloud service provider that supports Docker Compose.

2. **Set Up the Environment**

   - Follow the provider's documentation to set up your environment.
   - Upload your project files to the server.
   - Ensure your `.env` file is correctly configured.

3. **Deploy the Application**

   - Run the following command on your server:

     ```bash
     docker-compose up --build -d
     ```

     > _Image Placeholder: Screenshot of deployment command execution_

4. **Access the Live Application**

   - Once deployed, access your application through the server's IP address or domain name.

     ```bash
     http://your_server_ip:8000
     ```

     > _Image Placeholder: Screenshot of the live application homepage_

## Environment Variables

Ensure you have the following environment variables set in your `.env` file:

```env
POSTGRES_HOSTNAME=
POSTGRES_DATABASE=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=
SALT=
TRANSFORMER_MODEL=
OPENAI_MODEL=
OPENAI_KEY=
```

## Technologies Used

- **FastAPI**: High-performance web framework for building APIs.
- **Python 3.8+**
- **Docker & Docker Compose**
- **PostgreSQL**: Relational database system.
- **SentenceTransformers**: For generating embeddings.
- **OpenAI API**: For summarization and translation features.
- **Jinja2 Templates**: For rendering HTML templates.
- **HTML/CSS/JavaScript**: Frontend technologies.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Prepared by**: [Your Name]  
**Position**: Lead Developer, VerityHub Project
