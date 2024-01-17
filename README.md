# SoundScripter 🔊📝

Simplify and Automate your transcription workflow with SoundScripter

## Features

-   **Media Transcription:** Convert media files (audio/video) to text with high accuracy.
-   **Scalable:** Utilizes a distributed architecture to handle multiple requests in parallel.
-   **Real-time Notifications:** Uses Redis Pub-Sub and Server-Sent Events (SSE) for real-time notifications

## Architecture

SoundScripter's architecture is designed to handle transcription requests efficiently. Here's how it works:

1. **User Requests:** Users uploads video/audio files for transcription through API.

2. **Optimization:** Media files are optimized to be utilized for transcription service.

3. **RabbitMQ Message Broker:** Transcription requests are added to the RabbitMQ message broker.

4. **Celery Task Queue:** Celery task queues manages and distribute the tasks. When new tasks are added to the queue, Celery workers pick them up and process them asynchronously and concurrently.

5. **Task Execution:** Each task runs in its own container, allowing for parallel processing of multiple tasks based on the system configuration.

6. **Realtime Notifications:** SoundScripter leverages Redis Pub-Sub and Server-Sent Events (SSE) for real-time notifications.

## Getting Started

To run SoundScripter locally or in a server environment, follow these steps:

1. Clone this repository to your local machine

    ```bash
    git clone https://github.com/hitesh22rana/SoundScripter.git
    ```

2. Navigate to the SoundScripter directory

    ```bash
    cd SoundScripter
    ```

3. Check the requirements

    ```bash
    ./check-requirements.sh
    ```

4. Build and run the application

    ```bash
    ./build.sh
    ```

5. Now you app is up and running and you can access the app via `http://localhost:3000`.

## Contributions

We welcome contributions to improve SoundScripter. Feel free to open issues, submit pull requests, or reach out with your ideas.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
