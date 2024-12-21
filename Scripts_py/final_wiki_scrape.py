from lang_trans.arabic import buckwalter

def enhanced_transliteration(arabic_text):
    # Transliterate using Buckwalter
    transliterated_text = buckwalter.transliterate(arabic_text)
    
    # Map for refining transliteration to make it more readable
    refinement_map = {
        'A': 'a',  # Convert 'A' to 'a' for natural English-like sound
        'S': 's', 'D': 'd', 'T': 't', 'Z': 'z',  # Adjust emphatic letters
        'p': 'h',  # Convert 'p' to 'h' for the Arabic "ة"
    }
    
    # Refine Buckwalter transliteration
    readable_text = "".join(refinement_map.get(char, char) for char in transliterated_text)
    
    # Capitalize proper nouns (e.g., "Dar" instead of "dar")
    words = readable_text.split()
    refined_words = [word.capitalize() for word in words]
    
    return " ".join(refined_words)

# Arabic text
arabic_text = "TGI Fridays"

# Get enhanced transliteration
print(enhanced_transliteration(arabic_text))
