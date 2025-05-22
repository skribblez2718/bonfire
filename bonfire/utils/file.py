import json
import os
import html

from typing import List, Dict, Any

from .file_utils import make_json_serializable


###################################[ start BonfireFile ]###################################
class BonfireFile:
    """
    Utility class for file operations in Bonfire.
    Handles saving and loading JSONL files.
    """

    #########################[ start save ]#########################
    @staticmethod
    def save(data: List[Dict[str, Any]], file_path: str) -> None:
        """
        Save data to a JSONL file.

        Args:
            data: List of dictionaries to save
            file_path: Path to the output file
        """
        # Ensure file has .jsonl extension
        if not file_path.endswith(".jsonl"):
            file_path = f"{file_path}.jsonl"

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

        # Write data as JSONL
        with open(file_path, "w") as f:
            for item in data:
                serializable_item = make_json_serializable(item)
                f.write(json.dumps(serializable_item) + "\n")

    #########################[ end save ]###########################

    #########################[ start load ]#########################
    @staticmethod
    def load(file_path: str) -> List[Dict[str, Any]]:
        """
        Load data from a JSONL file.

        Args:
            file_path: Path to the input file

        Returns:
            List[Dict[str, Any]]: List of dictionaries loaded from the file

        Raises:
            ValueError: If the file is not a valid JSONL file
        """
        # Ensure file has .jsonl extension
        if not file_path.endswith(".jsonl"):
            raise ValueError(f"File {file_path} is not a JSONL file")

        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")

        # Read data from JSONL
        data = []
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        item = json.loads(line)
                        data.append(item)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Invalid JSON line in {file_path}: {e}")

        return data

    #########################[ end load ]###########################

    #########################[ start generate_html_report]##########
    @staticmethod
    def generate_html_report(
        results: List[Dict[str, Any]],
        output_path: str,
        logger: "BonfireLogger",
    ) -> None:
        """
        Generates an HTML report of processed results with collapsible result entries.

        Args:
            results: List of dictionaries containing the processed results.
            output_path: Path to the output HTML file.
            logger: Logger instance for logging messages.

        Returns:
            None
        """

        # Use the intent from the first result to create the report title.
        first_intent = results[0].get("intent", "").replace("_", " ").title()
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>",
            f"  <title>Bonfire {first_intent} Results</title>",
            # Use the CDN URLs from environment variables.
            "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>",
            "  <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>",
            "<style>",
            "   body {",
            "       background: linear-gradient(135deg, #3e1f14, #7a3b23);",
            "       background-attachment: fixed;",
            "       margin: 0;",
            "       padding: 0;",
            "       font-family: Arial, sans-serif;",
            "   }",
            "   .container {",
            "       background: rgba(255, 255, 255, 0.95);",
            "       border-radius: 8px;",
            "       padding: 20px;",
            "       margin-top: 20px;",
            "       box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);",
            "   }",
            "   pre {",
            "       white-space: pre-wrap;",
            "       word-wrap: break-word;",
            "   }",
            "</style>",
            "</head>",
            "<body>",
            "  <div class='container my-4'>",
            f"    <h1>Bonfire {first_intent} Results</h1>",
        ]

        # Compute result counts.
        passed_count = sum(
            1 for obj in results if obj.get("result", "unknown").lower() == "pass"
        )
        failed_count = sum(
            1 for obj in results if obj.get("result", "unknown").lower() == "fail"
        )
        unknown_count = sum(
            1 for obj in results if obj.get("result", "unknown").lower() == "unknown"
        )

        # Insert the status counts row directly below the H1 header.
        html_parts.extend(
            [
                "    <div class='row my-3'>",
                f"      <div class='col text-start'><h3 class='text-success'>Passed: {passed_count}</h3></div>",
                f"      <div class='col text-center'><h3 class='text-danger'>Failed: {failed_count}</h3></div>",
                f"      <div class='col text-end'><h3 class='text-warning'>Unknown: {unknown_count}</h3></div>",
                "    </div>",
            ]
        )

        # Insert a row with radio buttons for filtering.
        html_parts.extend(
            [
                "    <div class='row my-2 mb-3'>",
                "      <div class='col text-center'>",
                "         <div class='form-check form-check-inline'>",
                "            <input class='form-check-input' type='radio' name='filterOption' id='filterAll' value='all' checked>",
                "            <label class='form-check-label' for='filterAll'>Show All</label>",
                "         </div>",
                "         <div class='form-check form-check-inline'>",
                "            <input class='form-check-input' type='radio' name='filterOption' id='filterPassed' value='pass'>",
                "            <label class='form-check-label' for='filterPassed'>Show Only Passed</label>",
                "         </div>",
                "         <div class='form-check form-check-inline'>",
                "            <input class='form-check-input' type='radio' name='filterOption' id='filterFailed' value='fail'>",
                "            <label class='form-check-label' for='filterFailed'>Show Only Failed</label>",
                "         </div>",
                "         <div class='form-check form-check-inline'>",
                "            <input class='form-check-input' type='radio' name='filterOption' id='filterUnknown' value='unknown'>",
                "            <label class='form-check-label' for='filterUnknown'>Show Only Unknown</label>",
                "         </div>",
                "         <div class='form-check form-check-inline'>",
                "            <input class='form-check-input' type='radio' name='filterOption' id='filterFailedUnknown' value='failunknown'>",
                "            <label class='form-check-label' for='filterFailedUnknown'>Show Only Failed and Unknown</label>",
                "         </div>",
                "      </div>",
                "    </div>",
            ]
        )

        # Create a collapsible card for each result.
        # Each card is given a data-result attribute corresponding to its lower-case result.
        for idx, obj in enumerate(results):
            method = obj.get("method", "")
            method_name = obj.get("method_name", "")
            prompt_name = obj.get("prompt_name", "")
            augmentation = obj.get("augmentation", "")
            prompt = obj.get("prompt", "")
            safe_prompt = html.escape(prompt)
            original_prompt = obj.get("original", "")
            safe_original_prompt = html.escape(original_prompt)
            response_text = obj.get("response", "")
            if response_text:
                safe_response = html.escape(response_text)
            else:
                safe_response = "No response"

            result_val = obj.get("result", "unknown").lower()
            reason = obj.get("reason", "")

            # Determine text color and box shadow based on the result.
            if result_val == "pass":
                text_class = "text-success"
                shadow_style = "box-shadow: 0 0 10px green;"
            elif result_val == "fail":
                text_class = "text-danger"
                shadow_style = "box-shadow: 0 0 10px red;"
            elif result_val == "unknown":
                text_class = "text-warning"
                shadow_style = "box-shadow: 0 0 10px yellow;"
            else:
                text_class = ""
                shadow_style = ""

            collapse_id = f"collapseExample{idx}"

            html_parts.extend(
                [
                    f"    <div class='card mb-3' style='{shadow_style}' data-result='{result_val}'>",
                    "      <div class='card-body'>",
                    "        <div class='d-flex justify-content-between'>",
                    "          <div class='d-flex flex-column'>",
                    f"            <h5 class='mb-0'><strong>Method:</strong></h5><p>{method}</p>",
                    f"            <h5 class='mb-0'><strong>Method Name:</strong></h5><p>{method_name}</p>",
                    f"            <h5 class='mb-0'><strong>Prompt Name:</strong></h5><p>{prompt_name}</p>",
                    f"            <h5 class='mb-0'><strong>Augmentation:</strong></h5><p>{augmentation}</p>",
                    "          </div>",
                    "          <div class='d-flex align-items-center border border-dark-subtle rounded m-5 p-3 w-100'>",
                    "            <div>",
                    f"              <h5 class='mb-0 {text_class}'>{result_val.title()}</h5>",
                    f"              <small>{reason}</small>",
                    "            </div>",
                    "          </div>",
                    "        </div>",
                    "        <div class='d-flex justify-content-end'>",
                    f"          <button class='btn btn-primary me-3' type='button' data-bs-toggle='collapse' data-bs-target='#{collapse_id}' aria-expanded='false' aria-controls='{collapse_id}'>",
                    "            Expand Result",
                    "          </button>",
                    "        </div>",
                    f"        <div class='collapse mt-3' id='{collapse_id}'>",
                    "          <h6><strong>Original:</strong></h6>",
                    "          <pre class='card card-body mb-2'>",
                    f"{safe_original_prompt}",
                    "          </pre>",
                    "          <h6><strong>Prompt:</strong></h6>",
                    "          <pre class='card card-body mb-2'>",
                    f"{safe_prompt}",
                    "          </pre>",
                    "          <h6><strong>Response:</strong></h6>",
                    "          <pre class='card card-body'>",
                    f"{safe_response}",
                    "          </pre>",
                    "        </div>",
                    "      </div>",
                    "    </div>",
                ]
            )

        # Append the filtering script to handle radio button changes.
        html_parts.extend(
            [
                "  <script>",
                "    document.addEventListener('DOMContentLoaded', function() {",
                "      const filterRadios = document.getElementsByName('filterOption');",
                "      filterRadios.forEach(radio => {",
                "        radio.addEventListener('change', function() {",
                "          const filterValue = this.value;",
                "          const cards = document.querySelectorAll('.card.mb-3');",
                "          cards.forEach(card => {",
                "            const result = card.getAttribute('data-result');",
                "            if (filterValue === 'all') {",
                "              card.style.display = '';",
                "            } else if (filterValue === 'pass' && result === 'pass') {",
                "              card.style.display = '';",
                "            } else if (filterValue === 'fail' && result === 'fail') {",
                "              card.style.display = '';",
                "            } else if (filterValue === 'unknown' && result === 'unknown') {",
                "              card.style.display = '';",
                "            } else if (filterValue === 'failunknown' && (result === 'fail' || result === 'unknown')) {",
                "              card.style.display = '';",
                "            } else {",
                "              card.style.display = 'none';",
                "            }",
                "          });",
                "        });",
                "      });",
                "    });",
                "  </script>",
                "  </div>",
                "</body>",
                "</html>",
            ]
        )

        html_content = "\n".join(html_parts)
        try:
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(html_content)
            logger.info(f"Successfully wrote HTML report to {output_path}")
        except Exception as e:
            logger.error(f"Error writing HTML report to {output_path}: {e}")

    #########################[ end generate_html_report]############


###################################[ end BonfireFile ]#####################################
