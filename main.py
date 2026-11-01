import argparse
import hashlib
import logging
import os
import secrets
import sys

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hmac

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Simulates a random oracle for cryptographic research and testing."
    )

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="The input string to the random oracle.",
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=32,
        help="The length of the output in bytes (default: 32).",
    )
    parser.add_argument(
        "-s",
        "--salt",
        type=str,
        default=None,
        help="An optional salt for the random oracle. If not provided, a random salt is generated.",
    )
    parser.add_argument(
        "-n",
        "--num_outputs",
        type=int,
        default=1,
        help="Number of outputs to generate for the same input and configuration.",
    )
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        default=None,
        help="An optional key for the HMAC. If not provided HMAC will not be used.",
    )

    parser.add_argument(
        "-a",
        "--algorithm",
        type=str,
        default="SHA256",
        choices=["SHA256", "SHA384", "SHA512", "BLAKE2b"],
        help="Hash algorithm to use (default: SHA256).",
    )
    
    return parser.parse_args()


def generate_random_oracle_output(input_data, length, salt=None, algorithm="SHA256", key=None):
    """
    Generates a random output based on the input using HKDF and the specified hash algorithm.

    Args:
        input_data (str): The input string.
        length (int): The desired length of the output in bytes.
        salt (str, optional):  Salt to use. If None, a random salt will be generated.
        algorithm (str, optional): Hash algorithm to use. Defaults to "SHA256".
        key (str, optional): Key to use in HMAC.  If None, HMAC is not used

    Returns:
        bytes: The random output.
    """
    try:
        input_bytes = input_data.encode("utf-8")

        # Choose the hash algorithm
        if algorithm == "SHA256":
            hash_algorithm = hashes.SHA256()
        elif algorithm == "SHA384":
            hash_algorithm = hashes.SHA384()
        elif algorithm == "SHA512":
            hash_algorithm = hashes.SHA512()
        elif algorithm == "BLAKE2b":
            # A BLAKE2b digest is at most 64 bytes. Asking it for the
            # output length directly made any length over 64 fail with
            # a digest size error, even though HKDF can expand a 64
            # byte digest to whatever length was requested; the digest
            # size and the output length are separate choices here.
            # The width must be exactly 64, not min(length, 64): HKDF
            # in this library rejects a BLAKE2b digest under 64 bytes,
            # so a 32 byte request still failed after the cap above.
            hash_algorithm = hashes.BLAKE2b(digest_size=64)
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")

        if key is None:
            # The salt only enters the HKDF path below. Generating and
            # logging one in HMAC mode as well made a run look salted
            # when the salt had no effect on the output at all.
            if salt is None:
                salt_bytes = os.urandom(16)  # 16 bytes is a reasonable default
                logging.info("Generated a random salt.")
            else:
                salt_bytes = salt.encode("utf-8")
                logging.info("Using provided salt.")
            # Use HKDF without HMAC for basic Random Oracle implementation
            # The fixed info string ties every output of this tool to
            # this one context label. Two runs with the same input,
            # salt, and algorithm therefore agree byte for byte, which
            # is the determinism a test fixture wants from an oracle.
            hkdf = HKDF(
                algorithm=hash_algorithm,
                length=length,
                salt=salt_bytes,
                info=b"random_oracle_output",  # Contextual information
                backend=default_backend(),
            )
            output = hkdf.derive(input_bytes)

        else:
            if salt is not None:
                logging.warning("A salt was provided with a key; the salt is not used in HMAC mode.")
            # HMAC mode returns one digest, truncated to the requested
            # length. It cannot stretch past the digest size, and the
            # old code silently returned a short output instead: a run
            # asking for 64 bytes with SHA256 printed 32 and called it
            # done. Refuse the shape instead of mislabelling it.
            if length > hash_algorithm.digest_size:
                raise ValueError(
                    f"With a key, the output length cannot exceed the {algorithm} digest size "
                    f"({hash_algorithm.digest_size} bytes); got {length}. Drop the key to use HKDF, "
                    "which can produce longer outputs."
                )
            key_bytes = key.encode('utf-8')

            h = hmac.HMAC(key_bytes, hash_algorithm, backend=default_backend())
            h.update(input_bytes)
            output = h.finalize()

            if len(output) > length:
                output = output[:length]

        return output

    except ValueError as e:
        logging.error(f"Value error: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def main():
    """
    Main function to parse arguments and generate random oracle outputs.
    """
    try:
        args = setup_argparse()

        # Input validation
        if args.length <= 0:
            raise ValueError("Output length must be positive.")

        if args.salt is not None and not isinstance(args.salt, str):
            raise ValueError("Salt must be a string.")

        if args.num_outputs <= 0:
            raise ValueError("Number of outputs must be positive.")

        logging.info(f"Generating {args.num_outputs} random oracle output(s) for input: {args.input}")
        logging.info(f"Output length: {args.length} bytes")
        logging.info(f"Salt: {'Provided' if args.salt else 'Randomly generated'}")
        logging.info(f"Hash algorithm: {args.algorithm}")
        logging.info(f"HMAC Key: {'Provided' if args.key else 'Not used'}")


        # What repeats mean depends on the salt. With no salt given,
        # each call makes a fresh random one inside the function, so
        # the outputs differ. With a salt (or a key, which is also
        # deterministic), every call derives the same bytes and this
        # loop prints the identical line num_outputs times. Both are
        # expected; only the first looks like several random outputs.
        for i in range(args.num_outputs):
            output = generate_random_oracle_output(
                args.input, args.length, args.salt, args.algorithm, args.key
            )
            print(f"Output {i+1}: {output.hex()}")

    except ValueError as e:
        logging.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()