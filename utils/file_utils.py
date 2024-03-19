import os
import cv2, csv, docx, fitz, json
import pytesseract as tess
import dotenv

dotenv.load_dotenv()

debug = int(os.getenv("DEBUG", "0"))


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with fitz.open(file_path) as doc:  # Open the PDF file
            for page in doc:  # Iterate through each page
                text += page.get_text()  # Append page text to the overall text
    except Exception as e:
        print(f"Error reading PDF file {file_path}: {e}")
    return text


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    text = ""
    try:
        doc = docx.Document(file_path)  # Open the DOCX file
        text = "\n".join(
            paragraph.text for paragraph in doc.paragraphs
        )  # Concatenate all paragraphs
    except Exception as e:
        print(f"Error reading DOCX file {file_path}: {e}")
    return text


def extract_text_from_image(file_path):
    image = cv2.imread(file_path)
    text = tess.image_to_string(image)
    return text


def read_and_extract_text_from_file(file_path):
    file_text = ""

    if file_path.lower().endswith(".pdf"):
        file_text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith((".docx", ".doc")):
        file_text = extract_text_from_docx(file_path)
    elif file_path.lower().endswith((".jpg", ".jpeg", ".png")):
        file_text = extract_text_from_image(file_path)
    else:
        # Skip files with unsupported formats
        print("Unsupported file type")

    return file_text


def write_to_csv(headers, data):
    filepath = "scores.csv"
    is_new_file = not os.path.isfile(filepath)

    with open(filepath, "a+") as file:
        writer = csv.writer(file)
        if is_new_file:
            writer.writerow(headers)
        writer.writerows(data)


def write_to_json(results):
    if not results:
        return

    outjson = "result.json"
    is_outjson_exists = os.path.isfile(outjson)
    existing_results = []

    with open(outjson, "w+") as f:
        if is_outjson_exists:
            try:
                existing_results = json.load(f)
            except Exception as e:
                existing_results = []

        existing_results.extend(results)
        json.dump(existing_results, f)


def store_results(results, csv_headers=None):
    if not results:
        return
    results = [json.loads(result) for result in results]

    if debug:
        write_to_json(results)

    scores = []
    for evaluation in results:
        result = evaluation["result"]
        scores.append(
            [
                evaluation["filepath"],
                result["EB"]["score"],
                result["SA"]["score"],
                result["LP"]["score"],
                result["ALI"]["score"],
                result["CAI"]["score"],
            ]
        )
    write_to_csv(csv_headers, scores)
