from lxml import etree
import os


def choose_selection(xml_file_name, page_title):
    convert_xml_to_html_single_page(r'output_html',
                                    xml_file_name,
                                    r'xsltfiles/books_by_filter.xslt',
                                    page_title)


'''
    function to convert xml to html page
'''
def convert_xml_to_html_single_page(output_dir_name, xml_file_name, xslt_file, page_title):
    # Create the directory if it doesn't exist
    os.makedirs(output_dir_name, exist_ok=True)

    # Load the XML document
    xml_doc = etree.parse(xml_file_name)

    # Load the main index XSLT
    books_by_filter_xslt = etree.parse(xslt_file)
    books_by_filter_transform = etree.XSLT(books_by_filter_xslt)

    # Generate the main index page
    custom_heading = etree.XSLT.strparam(page_title)
    result_tree = books_by_filter_transform(xml_doc, pageTitle=custom_heading)
    with open(os.path.join(output_dir_name, 'index.html'), 'wb') as f:
        f.write(etree.tostring(result_tree, pretty_print=True, method="html"))

    print("HTML files have been generated successfully.")

'''
    function to convert xml to html page for books by category
'''
def convert_xml_to_html_book_category(output_dir_name, xml_file_name, main_xslt_file):
    # Create the directory if it doesn't exist
    os.makedirs(output_dir_name, exist_ok=True)

    # Parse XML and XSLT
    xml_tree = etree.parse(xml_file_name)
    xslt_tree = etree.parse(main_xslt_file)

    # Create an XSLT transformer
    transform = etree.XSLT(xslt_tree)

    # Apply the transformation
    result_tree = transform(xml_tree)

    # Save the result to an HTML file
    with open(os.path.join(output_dir_name, 'index.html'), 'wb') as f:
        f.write(etree.tostring(result_tree, pretty_print=True, method="html"))

    print("HTML files have been generated successfully.")
