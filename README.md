# 🐦 Flappy Bird AI Clone – Reinforcement Learning Game Agent

> A Python-based AI-powered clone of the classic Flappy Bird game using **Pygame** and **Neuroevolution (NEAT algorithm)**.

## 📌 Project Overview

This project is a **re-implementation of Flappy Bird** where an AI agent learns to play the game by evolving neural networks through **NeuroEvolution of Augmenting Topologies (NEAT)**. Instead of controlling the bird manually, the AI trains itself using reinforcement learning concepts to maximize its survival time.

---

## 🚀 Scope of the Project

* **Game Simulation** using Python and Pygame
* **AI agent training** using NEAT to autonomously learn and improve gameplay
* Demonstrates **neuroevolution techniques** through visualization
* Builds an understanding of **genetic algorithms** applied in gaming AI

---

## 💡 Key Features

* 🎮 Fully playable clone of Flappy Bird using Pygame
* 🧠 AI agent learns to play without human input
* 📈 Evolutionary training using fitness-based selection and mutation
* 🔁 Multiple generations of AI with increasing skill levels
* 🔍 Real-time training visualization

---

## 🌟 Unique Selling Points (USP)

* **Portfolio-Grade Game + AI Hybrid**: Combines classic game mechanics with modern AI techniques.
* **Self-Learning Agent**: The bird trains itself using fitness scoring — no hardcoded rules.
* **Visualization of Learning Process**: Track how each generation performs and improves.
* **Beginner-Friendly**: Clean, well-commented codebase to help learners explore Pygame and NEAT.

---

## 🔧 Tech Stack

| Technology  | Description                              |
| ----------- | ---------------------------------------- |
| Python      | Core programming language                |
| Pygame      | For game rendering and logic             |
| NEAT-Python | For evolutionary neural network learning |

---

## 📁 Project Structure

```
flappy_bird/
│
├── assets/                # Game sprites and background
├── bird.py                # Bird class with physics and controls
├── pipe.py                # Pipe class for obstacle generation
├── base.py                # Ground logic
├── game.py                # Main game loop and training logic
├── neat-config.txt        # NEAT configuration file
├── run.py                 # Entry point for running the game
└── README.md              # Project documentation
```

---

## 🧠 How the AI Works

1. **Initialization**: Start with a population of neural networks (birds).
2. **Fitness Evaluation**: Each bird’s fitness increases with time survived.
3. **Selection & Mutation**: NEAT selects top performers and mutates them for the next generation.
4. **Evolution**: Over generations, birds become significantly better at avoiding pipes.

---

## 📦 How to Run the Project

### ✅ Prerequisites

* Python 3.7+
* Pygame
* NEAT-Python

### 🔄 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/flappy-bird-ai.git
cd flappy-bird-ai

# Install dependencies
pip install pygame neat-python
```

### ▶️ Run the Game

```bash
python run.py
```

---

## 🧠 Use Cases

* 🎓 **Education**: Learn game dev and AI training through real-time simulations
* 🧪 **Experimentation**: Try modifying game physics or NEAT parameters
* 🕹️ **Entertainment**: Watch AI agents evolve from clumsy to pro players

---

## 🧰 Further Improvements

* Add UI/UX enhancements (scoreboard, menus)
* Introduce background music and sound effects
* Save/load the best AI model
* Export trained AI to a playable game with no evolution

---


