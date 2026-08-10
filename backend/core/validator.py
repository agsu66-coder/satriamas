"""
TERATAI Validator
"""


class Validator:

    @staticmethod
    def require_headers(headers, required):

        missing = []

        for header in required:

            if header not in headers:
                missing.append(header)

        return missing