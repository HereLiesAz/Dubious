import re

class MoralCompass:
    def __init__(self):
        # The weighted dictionary of sin.
        # Format: "word": (P_score, V_score, S_score)
        self.lexicon = {
            # LEVEL 1: Mild
            "damn": (1, 0, 0), "hell": (1, 0, 0), "crap": (1, 0, 0),
            "stupid": (1, 0, 0), "idiot": (1, 0, 0), "butt": (1, 0, 0),
            
            # LEVEL 2: Crude
            "ass": (2, 0, 1), "piss": (2, 0, 0), "bastard": (2, 1, 0),
            "bitch": (2, 1, 0), "balls": (2, 0, 2),
            
            # LEVEL 3: Strong
            "shit": (3, 0, 0), "bullshit": (3, 0, 0), "dick": (3, 0, 2),
            "cock": (3, 0, 2), "pussy": (3, 0, 2), "tits": (3, 0, 2),
            
            # LEVEL 4: Severe
            "fuck": (4, 1, 1), "motherfucker": (4, 1, 1), 
            "cunt": (4, 1, 2), "whore": (4, 0, 2),
            
            # LEVEL 5: Hateful / Extreme (The "Nuclear" Option)
            "nigger": (5, 5, 0), "faggot": (5, 5, 0), "retard": (5, 0, 0),
            "kill": (0, 3, 0), "murder": (0, 4, 0), "rape": (0, 5, 5),
            "shoot": (0, 3, 0), "stab": (0, 3, 0), "gun": (0, 2, 0)
        }
        
        # Regex to handle plurals/variations (e.g., "fucking" -> "fuck")
        self.word_pattern = re.compile(r'\b\w+\b')

    def judge_text(self, text):
        """
        Analyzes a string and returns its Max Sin Scores.
        Returns: { 'profanity': int, 'violence': int, 'sexual': int, 'triggers': list }
        """
        text_lower = text.lower()
        words = self.word_pattern.findall(text_lower)
        
        scores = {'profanity': 0, 'violence': 0, 'sexual': 0}
        triggers = []
        
        for word in words:
            # Direct match
            if word in self.lexicon:
                p, v, s = self.lexicon[word]
                scores['profanity'] = max(scores['profanity'], p)
                scores['violence'] = max(scores['violence'], v)
                scores['sexual'] = max(scores['sexual'], s)
                
            # Basic stemming check (e.g., "killer" -> "kill")
            # This is a crude heuristic for speed.
            else:
                for root, vals in self.lexicon.items():
                    if root in word and len(word) <= len(root) + 3:
                        p, v, s = vals
                        scores['profanity'] = max(scores['profanity'], p)
                        scores['violence'] = max(scores['violence'], v)
                        scores['sexual'] = max(scores['sexual'], s)

        # Contextual boosts (Logic overrides)
        if "kill" in text_lower and "you" in text_lower:
            scores['violence'] = max(scores['violence'], 4) # Direct threat

        return scores

    def suggest_replacement(self, text, scores):
        """
        If the text is sinful, suggests a Dubious replacement.
        This is where we would eventually hook into an LLM.
        For now, it does simple deterministic swaps.
        """
        if max(scores.values()) == 0:
            return text
            
        new_text = text
        # Simple swap logic for the MVP
        replacements = {
            "fuck": "fudge", "shit": "shoot", "ass": "rear",
            "bitch": "witch", "damn": "darn", "hell": "heck",
            "kill": "hug", "murder": "marry", "gun": "bun"
        }
        
        for bad, good in replacements.items():
            pattern = re.compile(re.escape(bad), re.IGNORECASE)
            new_text = pattern.sub(good, new_text)
            
        return new_text

# Usage Example
if __name__ == "__main__":
    compass = MoralCompass()
    sentence = "I'm going to kill you, you motherfucker."
    verdict = compass.judge_text(sentence)
    sanitized = compass.suggest_replacement(sentence, verdict)
    
    print(f"Original: {sentence}")
    print(f"Verdict: {verdict}")
    print(f"Dubious Version: {sanitized}")
                      
