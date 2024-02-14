# Cine Query Website

## Website URL

The website is hosted at [Cine Query](https://cine-query.vercel.app/)


## Introduction

Cine Query is a chat application designed to provide users with detailed information about movies and series. It leverages the capabilities of LangChain and OpenAI's GPT-3.5 LLM to parse user queries and fetch relevant data from The Movie Database (TMDb). The backend is built using Node.js and Express with TypeScript, while the frontend is developed using React with TypeScript and styled using Tailwind CSS.

## Backend Setup (Node.js and Flask)

### Requirements

- Python 3.x
- Node.js
- npm or Yarn

### Python Flask Server

1. **Environment Setup**:

   - Ensure Python 3.x is installed.
   - Set up a virtual environment (venv) in your project directory:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - Windows: `venv\Scripts\activate`
     - macOS/Linux: `source venv/bin/activate`

2. **Dependencies**:

   - Install the required Python packages:
     ```bash
     pip install flask requests dotenv langchain langchain_openai
     ```

3. **Environment Variables**:

   - Create a `config.env` file in your project root.
   - Add your OpenAI API Key and TMDb API Token:
     ```
     OPENAI_API_KEY=your_openai_api_key
     TMDB_API_TOKEN=your_tmdb_api_token
     ```

4. **Running the Flask Server**:
   - Run the Flask server using:
     ```bash
     python src/main.py
     ```
   - The server will start on `http://localhost:5000`.

## Frontend Setup (React with TypeScript and Tailwind CSS)

1. **Setting Up React Project**:

- In the project directory, run `npm install` to install dependencies.

2. **Running the Frontend Server**:
   - Start the development server using:
     ```bash
     npm run dev
     ```
   - The server will start on `http://localhost:5173`.

### Node.js Server

1. **Project Setup**:

   - Install Node.js and npm.
   - In the project directory, run `npm install` to install dependencies.

2. **Running the Development Server**:
   - To run the server in development mode, use:
     ```bash
     npm run dev
     ```
   - The server will start on `http://localhost:3000`.
   - The development server will start, and any changes in the TypeScript files will automatically restart the server.

## How It Works

Users type a query in the input field on the frontend. The request is sent to the Python Flask server. The Flask server, powered by the LangChain framework, communicates with the OpenAI GPT-3.5 LLM to parse the query into a meaningful JSON format. It then queries the TMDb API and formats the response into a user-friendly format, which is sent back to the frontend and displayed to the user.

## Future Implementation

- A Node.js server has been established, although the current application does not utilize it; instead, it is prepared for future integration.
- User Authentication: To secure user data and preferences.
- Custom Response Tone: Allowing users to choose the tone of responses, e.g., "What if Elon Musk replied?"
- Free Trial and Payment Integration: Implementing a trial period followed by payment options, possibly using Stripe for payment processing.

## Reasons for Using Two Servers

Separation of Concerns emphasizes keeping authentication and payment logic distinct from AI interaction logic, fostering improved maintainability, scalability, and security. To adhere to this principle, I've opted to integrate Node.js for authentication and payment functionalities, while Flask will handle LLM interaction.
