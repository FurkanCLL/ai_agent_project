# AI Agent Project

A modular, Python-based AI agent architecture. This project implements custom external tools (such as system monitoring) and utilizes the Observer design pattern for structured, scalable event logging.

## Features
* **Modular Architecture:** Clean separation of core logic, utility functions, and external tools.
* **Observer Pattern Logging:** Implemented a robust logging system using the Observer design pattern to track events efficiently.
* **Custom Tools:** Includes a `system info tool` for technical status monitoring, designed to be easily expandable.

## Project Structure
* `core/`: Contains the core agent logic and base components.
* `tools/`: External tools and capabilities accessible by the AI agent.
* `utils/`: Utility functions and the observer logger implementation.
* `main.py`: The entry point of the application.

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/FurkanCLL/ai_agent_project.git](https://github.com/FurkanCLL/ai_agent_project.git)
   cd ai_agent_project