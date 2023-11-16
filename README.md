# BizCardX: Business Card Information Extraction

BizCardX is a Streamlit application that allows users to upload an image of a business card, extract relevant information using easyOCR, and store the information in a database. This project is designed to streamline the process of managing business card data efficiently.

## Table of Contents
- [ProblemStatement](#ProblemStatement)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [License](#license)

## ProblemStatement

Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR. The extracted information should include the company name, cardholder name, designation, mobile number, email address, website URL, area, city, state, and pin code. The extracted information should then be displayed in the application's graphical user interface (GUI).
In addition, the application should allow users to save the extracted information into a database along with the uploaded business card image. The database should be able to store multiple entries, each with its own business card image and extracted information.

## Features

1. **Image Processing and OCR:**
   - Users can upload an image of a business card.
   - EasyOCR is used to extract relevant information from the uploaded image.

2. **Database Integration:**
   - Extracted information is stored in a PostgreSQL database.
   - Users can perform CRUD operations on the database through the Streamlit UI.

3. **User-Friendly Interface:**
   - Intuitive UI design guiding users through the extraction and database operations.
   - Clean display of extracted information for easy understanding.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/bizcardx.git
   cd bizcardx

## Usage
1. Open the application in a web browser.
2. Upload an image of a business card.
3. Click on the "Extract" button to extract information.
4. View and verify the extracted information.
5. Click on "Insert into Database" to save the information to the database.
6. Navigate to other sections (Records, Update, Delete, Download) for additional functionalities.

## Technologies Used
- Python
- Streamlit
- EasyOCR
- PostgreSQL

## License
This project is licensed under the MIT License.
