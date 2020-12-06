#!/usr/bin/python3

"""
Exemple d'implémentation simpliste du chiffrement par décalage.
"""

import argparse


def cesar(phrase: str, decalage: int) -> str:
    ord_a = ord('a')
    translate = str.maketrans({
        chr(i + ord_a): chr(((i + decalage) % 26) + ord_a)
        for i in range(26)
        })

    return phrase.translate(translate)


def encrypt(phrase: str, decalage: int):
    ciphertext = cesar(phrase, decalage)
    print(ciphertext)


def decrypt(phrase: str, decalage: int, show_ln: bool = False):
    cleartext = cesar(phrase, -decalage)
    if show_ln:
        cleartext = f'{decalage}:\t{cleartext}'
    print(cleartext)


def bruteforce(phrase: str):
    for decalage in range(1, 26):
        decrypt(phrase, decalage, True)


def main():
    parser = argparse.ArgumentParser(description='Chiffre de César.')
    parser.add_argument('cmd', choices=['encrypt', 'decrypt', 'bruteforce'])
    args = parser.parse_args()

    input_args = [input("phrase: ")]
    if args.cmd in ['encrypt', 'decrypt']:
        input_args.append(int(input("decalage: ")))

    globals()[args.cmd](*input_args)


if __name__ == "__main__":
    main()
