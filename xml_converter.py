import xml.etree.ElementTree as ET


def create_book_element(book):
    book_elem = ET.Element("book")

    id_elem = ET.SubElement(book_elem, "id")
    id_elem.text = book["id"]

    title_elem = ET.SubElement(book_elem, "title")
    title_elem.text = book["title"]

    price_elem = ET.SubElement(book_elem, "price")
    price_elem.text = str(book["price"])

    rating_elem = ET.SubElement(book_elem, "rating")
    rating_elem.text = str(book["rating"])

    is_in_stock_elem = ET.SubElement(book_elem, "is_in_stock")
    is_in_stock_elem.text = str(book["is_in_stock"]).lower()

    availability_count_elem = ET.SubElement(book_elem, "availability_count")
    availability_count_elem.text = str(book["availability_count"])

    description_elem = ET.SubElement(book_elem, "description")
    description_elem.text = book["description"]

    category_id_elem = ET.SubElement(book_elem, "category_id")
    category_id_elem.text = book["category"]

    book_cover_url_elem = ET.SubElement(book_elem, "book_cover_url")
    book_cover_url_elem.text = book["book_cover_url"]

    return book_elem


def convert_books_to_xml(books, categories):
    """
        Function to convert AWS Dynamodb result for books by rating availability count or price
        to xml file
    """
    library_elem = ET.Element("library")

    categories_elem = ET.SubElement(library_elem, "categories")
    books_elem = ET.SubElement(library_elem, "books")

    # will always display all categories
    for category in categories:
        category_elem = ET.SubElement(categories_elem, "category")

        category_id_elem = ET.SubElement(category_elem, "id")
        category_id_elem.text = category["id"]

        category_name_elem = ET.SubElement(category_elem, "name")
        category_name_elem.text = category["category_name"]

    # display fetched books
    for book in books:
        book_elem = create_book_element(book)
        books_elem.append(book_elem)

    return ET.tostring(library_elem, encoding='unicode')


def convert_books_to_xml_by_category(books_by_category):
    """
        Function to convert AWS Dynamodb result to xml file for the query books by category
    """
    root = ET.Element("categories")
    for category_id, books in books_by_category.items():
        category_element = ET.SubElement(root, "category", id=str(category_id))
        # books are added inside categories
        for book in books:
            book_element = ET.SubElement(category_element, "book")
            for key, value in book.items():
                if isinstance(value, bool):
                    value = str(value).lower()
                book_sub_element = ET.SubElement(book_element, key)
                book_sub_element.text = str(value)
    return ET.tostring(root, encoding='unicode')
