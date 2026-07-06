from langchain_core.documents import Document

def chunk_lab_json(data: dict):
    documents = []

    for test_key, test_data in data.items():
        test_name = test_data.get("test_name", test_key)

        # 1️⃣ Overview chunk
        overview_text = (
            f"Test: {test_name}\n"
            f"What it measures: {test_data.get('what_it_measures', '')}"
        )

        documents.append(
            Document(
                page_content=overview_text,
                metadata={
                    "test": test_key,
                    "section": "overview"
                }
            )
        )

        # 2️⃣ Reference ranges chunk
        ranges = test_data.get("reference_ranges", {})
        ranges_text = f"Test: {test_name}\nReference ranges:\n"

        for level, info in ranges.items():
            ranges_text += f"- {level.capitalize()}: {info.get('value', '')}\n"

        documents.append(
            Document(
                page_content=ranges_text,
                metadata={
                    "test": test_key,
                    "section": "reference_ranges"
                }
            )
        )

        # 3️⃣ Interpretation + causes + lifestyle (PER LEVEL)
        interpretations = test_data.get("interpretations", {})
        for level, interp in interpretations.items():
            interp_text = (
                f"Test: {test_name}\n"
                f"Level: {level.upper()}\n"
                f"What it means: {interp.get('what_it_means', '')}\n"
            )

            # Causes
            common_factors = interp.get("common_factors", [])
            if common_factors:
                interp_text += "Common causes or contributing factors:\n"
                for f in common_factors:
                    interp_text += f"- {f}\n"

            # Lifestyle
            lifestyle = interp.get("lifestyle_context")
            if lifestyle:
                interp_text += f"Lifestyle context: {lifestyle}\n"

            # Age
            age_ctx = interp.get("age_context")
            if age_ctx:
                interp_text += f"Age-related context: {age_ctx}\n"

            documents.append(
                Document(
                    page_content=interp_text,
                    metadata={
                        "test": test_key,
                        "section": "interpretation",
                        "level": level
                    }
                )
            )

        # 4️⃣ Risk association / correlations chunk
        risks = test_data.get("risk_associations", {})
        for risk_name, risk_data in risks.items():
            risk_text = (
                f"Test: {test_name}\n"
                f"Associated condition: {risk_name}\n"
                f"Correlation strength: {risk_data.get('correlation_strength')}\n"
                f"Direction: {risk_data.get('direction')}\n"
                f"Interpretation: {risk_data.get('interpretation')}\n"
            )

            markers = risk_data.get("associated_markers", [])
            if markers:
                risk_text += "Associated markers:\n"
                for m in markers:
                    risk_text += f"- {m['marker']} (correlation: {m['correlation']})\n"

            documents.append(
                Document(
                    page_content=risk_text,
                    metadata={
                        "test": test_key,
                        "section": "risk_association",
                        "condition": risk_name
                    }
                )
            )

    return documents
