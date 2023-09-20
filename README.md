# SoundScripter 🔊📝

Simplify and Automate your transcription workflow with SoundScripter

## Features

-   **Audio Transcription:** Convert audio files to text with high accuracy.
-   **Scalable:** Utilizes a distributed architecture to handle multiple transcription requests in parallel.
-   **Easy Deployment:** Run SoundScripter as a Docker container for hassle-free deployment.
-   **Real-time Monitoring:** Use Supervisor and RabbitMQ for real-time task management and monitoring.

## Architecture

SoundScripter's architecture is designed to handle transcription requests efficiently. Here's how it works:

1. **User Requests:** Users uploads video/audio files for transcription to the SoundScripter API.

2. **RabbitMQ Message Broker:** Transcription requests are added to the RabbitMQ message broker, which acts as a message queue.

3. **Celery Task Queue:** SoundScripter uses Celery to manage and distribute transcription tasks. When new tasks are added to the queue, Celery workers pick them up and process them asynchronously.

4. **Task Execution:** The Celery workers execute the transcription tasks, converting audio to text. Each worker runs in its own container, allowing for parallel processing of tasks based on the system configuration.

5. **Realtime Notifications:** SoundScripter leverages Redis Pub-Sub and Server-Side Events (SSE) for real-time notifications:

    - **Redis Pub-Sub:** As tasks progress or complete, SoundScripter publishes updates to Redis channels.

    - **Server-Side Events (SSE):** Clients, such as web applications, establish SSE connections with the SoundScripter server. When new messages arrive on the Redis Pub-Sub channels, the server pushes these updates to connected clients in real-time using SSE. This allows users to receive live notifications about the progress and completion of their transcription tasks.

## Getting Started

To run SoundScripter locally or in a server environment, follow these steps:

1. Clone this repository to your local machine

    ```bash
    git clone https://github.com/hitesh22rana/SoundScripter.git
    ```

2. Navigate to the backend directory

    ```bash
    cd backend
    ```

3. Configuration

    - You can configure various settings, such as RabbitMQ connection details and task priorities, in the `docker-compose.yml` files.
    - Environment variables are stored in `.env`. Refer `.env.example` for a template of the required variables. Make sure to create a `.env` file with your specific configuration before running the application.

4. Build and run the application

    i. First build the transcription service

    ```bash
    docker build -t transcription-service -f Dockerfile.transcription-service
    ```

    ii. Now, run the docker-compose file to bind all the services

    ```bash
    docker-compose -f docker-compose.yml up
    ```

5. Now you backend is up and running and you can access the API docs at `http://localhost:8000/docs`.

## Contributions

We welcome contributions to improve SoundScripter. Feel free to open issues, submit pull requests, or reach out with your ideas.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
