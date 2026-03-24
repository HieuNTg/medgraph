"""
FHIR R4 CapabilityStatement generator for MEDGRAPH.

Describes the server's FHIR capabilities per the FHIR R4 spec:
https://hl7.org/fhir/R4/capabilitystatement.html
"""

from medgraph import __version__


class CapabilityStatement:
    """Generate the FHIR R4 CapabilityStatement for MEDGRAPH."""

    def generate(self) -> dict:
        """Return FHIR R4 CapabilityStatement dict."""
        return {
            "resourceType": "CapabilityStatement",
            "status": "active",
            "kind": "instance",
            "fhirVersion": "4.0.1",
            "format": ["json"],
            "software": {
                "name": "MEDGRAPH",
                "version": __version__,
            },
            "implementation": {
                "description": (
                    "MEDGRAPH Drug Interaction Cascade Analyzer — Educational CDS. "
                    "FOR INFORMATIONAL PURPOSES ONLY. Not a substitute for professional "
                    "clinical judgment."
                ),
                "url": "https://github.com/HieuNTg/medgraph",
            },
            "rest": [
                {
                    "mode": "server",
                    "documentation": (
                        "MEDGRAPH FHIR R4 endpoint for drug interaction checking. "
                        "Accepts MedicationRequest bundles and returns interaction analysis."
                    ),
                    "resource": [
                        {
                            "type": "MedicationRequest",
                            "interaction": [
                                {"code": "create"},
                            ],
                            "operation": [
                                {
                                    "name": "$check",
                                    "definition": "OperationDefinition/medgraph-check",
                                    "documentation": (
                                        "Check drug interactions for a MedicationRequest resource. "
                                        "Educational use only."
                                    ),
                                }
                            ],
                        },
                        {
                            "type": "MedicationStatement",
                            "interaction": [
                                {"code": "create"},
                            ],
                        },
                        {
                            "type": "Bundle",
                            "interaction": [
                                {"code": "create"},
                            ],
                            "documentation": (
                                "Submit a Bundle of MedicationRequest/MedicationStatement "
                                "resources for interaction analysis."
                            ),
                        },
                    ],
                    "operation": [
                        {
                            "name": "check",
                            "definition": "OperationDefinition/medgraph-check",
                        }
                    ],
                }
            ],
        }
