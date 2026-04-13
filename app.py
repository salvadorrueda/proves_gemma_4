import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Configuració del model: Pots canviar-ho a gemma-7b o altres variants de Gemma (incloent les noves versions)
MODEL_ID = os.environ.get("MODEL_ID", "google/gemma-2b")

def main():
    print(f"[{MODEL_ID}] Iniciant la càrrega del model...")
    print("Assegurat de tenir configurada la variable d'entorn HF_TOKEN si el model requereix accés.")

    try:
        # Carregar el tokenitzador i el model
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        
        # 'device_map="auto"' mourà automàticament parts del model a la GPU si n'hi ha.
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            device_map="auto",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        print("\nModel carregat correctament! Pots començar a fer-li preguntes.")
        print("-" * 50)
        
    except Exception as e:
        print(f"\nError al carregar el model: {e}")
        print("Recordatori: Has acceptat les condicions del model Gemma a Hugging Face i configurat el HF_TOKEN en el fitxer .env?")
        return

    # Bucle d'interacció amb l'usuari
    while True:
        try:
            print("\nEscriu el teu missatge (o 'sortir' per acabar):")
            user_input = input("> ")
            if user_input.lower() in ('sortir', 'exit', 'quit'):
                break
                
            if not user_input.strip():
                continue

            # Tokenitzar l'entrada
            input_ids = tokenizer(user_input, return_tensors="pt").to(model.device)
            
            # Generar la resposta
            # Ajusta max_new_tokens segons la llargada que vulguis que tingui la resposta per defecte
            outputs = model.generate(
                **input_ids, 
                max_new_tokens=200,
            )
            
            # Decodificar i mostrar la resposta
            # En resposta a usuaris, sol·lem ignorar el que ja era part del prompt
            input_length = input_ids.input_ids.shape[1]
            generated_tokens = outputs[0][input_length:]
            response = tokenizer.decode(generated_tokens, skip_special_tokens=True)
            
            print(f"\nGemma:\n{response}")
            
        except KeyboardInterrupt:
            print("\nSortint...")
            break
        except Exception as e:
            print(f"\nS'ha produït un error durant la generació: {e}")

if __name__ == "__main__":
    main()
