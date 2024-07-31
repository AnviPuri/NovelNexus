from lxml import etree


def validate_xml(xml_file, xsd_file):
    # Parse the XSD schema
    with open(xsd_file, 'rb') as schema_file:  # Read as bytes
        schema_root = etree.XML(schema_file.read())
    schema = etree.XMLSchema(schema_root)

    # Parse the XML document
    with open(xml_file, 'rb') as xml_file:  # Read as bytes
        xml_doc = etree.parse(xml_file)

    # Validate the XML document against the XSD schema
    is_valid = schema.validate(xml_doc)

    # Print validation result
    if is_valid:
        print("The XML document is valid against the XSD schema.")
    else:
        print("The XML document is not valid against the XSD schema.")
        # Print the validation errors
        for error in schema.error_log:
            print(error.message)

    return is_valid
