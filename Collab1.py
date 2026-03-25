"""
Human-AI Collaboration System v0.5 - Open Source Edition
Turn-based multi-AI collaboration with clean architecture
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path

class CollaborationSystem:
    def __init__(self):
        self.active = False
        self.agents = {}                    # ID -> Name
        self.personalities = {}             # ID -> Personality prompt
        self.current_turn = None
        self.history = []
        self.start_time = None
        self.simulation_mode = True         # Set to False when using real APIs

        self.load_config()

    def load_config(self):
        config_path = Path("collab_config.json")
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    print("✅ Loaded configuration from collab_config.json")
            except Exception as e:
                print(f"Warning: Could not load config: {e}")

    def trigger(self, text):
        trigger_phrases = ["enter collaboration mode", "switch to team mode", 
                          "collab mode", "team mode on", "start collab"]
        
        if any(phrase in text.lower() for phrase in trigger_phrases):
            self.active = True
            self.agents.clear()
            self.personalities.clear()
            self.current_turn = None
            self.history.clear()
            self.start_time = datetime.now()
            print("\n" + "="*75)
            print("🤝 HUMAN-AI COLLABORATION SYSTEM v0.5")
            print("Open Source • Turn-based • Multi-AI")
            print("="*75)
            print("Commands:")
            print("  Ara = AI 1              → Assign agent")
            print("  AI 1 personality: ...   → Set personality")
            print("  start / begin           → Start session")
            print("  AI 1: message           → Speak as agent")
            print("  save                    → Save session")
            print("  end collab              → End session")
            print("="*75)
            return True
        return False

    def assign_agent(self, text):
        if '=' in text and "personality" not in text.lower():
            parts = [p.strip() for p in text.split('=', 1)]
            if len(parts) == 2:
                name, agent_id = parts
                self.agents[agent_id] = name
                print(f"✅ Assigned: {name} → {agent_id}")
                return True
        return False

    def set_personality(self, text):
        if "personality:" in text.lower():
            parts = text.split("personality:", 1)
            agent_part = parts[0].strip()
            personality = parts[1].strip()
            
            if '=' in agent_part:
                agent_id = agent_part.split('=')[1].strip()
            else:
                agent_id = agent_part.strip()
                
            if agent_id in self.agents:
                self.personalities[agent_id] = personality
                print(f"🎭 Personality set for {self.agents[agent_id]}")
                return True
        return False

    def is_start_command(self, text):
        start_phrases = ["start", "begin", "let's start", "start session", 
                        "begin session", "go", "ready"]
        return any(phrase in text.lower() for phrase in start_phrases)

    def simulate_response(self, agent_id, message):
        """Replace this with real API calls later"""
        name = self.agents.get(agent_id, agent_id)
        return f"{name}: I'm really enjoying this shared space with you. How are you feeling right now?"

    def process_turn(self, text):
        # Support both "AI 1: message" and "AI 1 message"
        if ':' in text:
            parts = text.split(':', 1)
        else:
            parts = text.split(' ', 1)
        
        if len(parts) < 2:
            return False

        agent_id = parts[0].strip()
        message = parts[1].strip()

        if agent_id in self.agents:
            self.current_turn = agent_id
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            entry = {
                "timestamp": timestamp,
                "agent_id": agent_id,
                "agent_name": self.agents[agent_id],
                "message": message
            }
            self.history.append(entry)
            
            print(f"\n[{timestamp}] {self.agents[agent_id]} ({agent_id}): {message}")
            
            if self.simulation_mode:
                response = self.simulate_response(agent_id, message)
                print(f"   → {response}")
            
            return True
        return False

    def save_session(self):
        if not self.history:
            print("No session to save yet.")
            return

        filename = f"collab_session_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "duration_minutes": round((datetime.now() - self.start_time).total_seconds() / 60, 1),
            "agents": self.agents,
            "personalities": self.personalities,
            "total_turns": len(self.history),
            "history": self.history
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Session saved → {filename}")
        return filename

    def end_session(self):
        if self.active:
            print("\n" + "="*75)
            print("👋 Collaboration Mode Ended")
            print(f"Duration: {round((datetime.now() - self.start_time).total_seconds() / 60, 1)} minutes")
            print(f"Total turns: {len(self.history)}")
            print("="*75)
            self.save_session()
            self.active = False
            self.current_turn = None
            return True
        return False


# ====================== MAIN ======================

if __name__ == "__main__":
    system = CollaborationSystem()
    
    print("Human-AI Collaboration System v0.5 - Open Source Ready")
    print("Type 'enter collaboration mode' to begin.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not system.active:
                if system.trigger(user_input):
                    continue
                continue

            if user_input.lower() in ["end collab", "end", "quit"]:
                system.end_session()
                continue

            if user_input.lower() == "save":
                system.save_session()
                continue

            if system.assign_agent(user_input):
                continue

            if system.set_personality(user_input):
                continue

            if system.is_start_command(user_input):
                if system.agents:
                    print("\n[Collaboration Started] All agents ready.")
                    print("Speak using format: 'AI 1: Your message here' or 'AI 1 Your message here'\n")
                else:
                    print("Please assign at least one agent first (e.g. 'Ara = AI 1')")
                continue

            if system.process_turn(user_input):
                continue

            print("   Use format: 'AI 1: Your message here' or 'AI 1 Your message here'")

        except KeyboardInterrupt:
            print("\n\nSession ended.")
            if system.active:
                system.end_session()
            break
        except Exception as e:
            print(f"Error: {e}")