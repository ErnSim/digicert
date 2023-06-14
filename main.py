import os
from signature import generate_key_pair, sign_file, save_signature, load_signature, verify_signature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def main():
    choice = input("Czy chcesz utworzyć (U) czy zweryfikować (Z) podpis cyfrowy? ")
    choice = choice.lower()

    if choice == "u":
        file_name = input("Podaj nazwę pliku, dla którego chcesz utworzyć podpis cyfrowy: ")
        file_path = os.path.join(os.getcwd(), file_name)

        private_key, public_key = generate_key_pair()
        signature = sign_file(file_path, private_key)

        save_signature(signature)
        print("Podpis został zapisany do pliku signature.txt")
    elif choice == "z":
        file_name = input("Podaj nazwę pliku, dla którego chcesz zweryfikować podpis cyfrowy: ")
        file_path = os.path.join(os.getcwd(), file_name)

        loaded_signature = load_signature()

        with open("public_key.pem", "rb") as file:
            public_key_pem = file.read()

        public_key = serialization.load_pem_public_key(
            public_key_pem,
            backend=default_backend()
        )

        verify_signature(file_path, loaded_signature, public_key)
    else:
        print("Nieprawidłowy wybór.")

if __name__ == "__main__":
    main()
