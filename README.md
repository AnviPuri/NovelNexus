data_scraper.py -- scraps data from webpage and converts data into a json file
books_data.json -- contains the scraped book data

awsquery.py -- contains queries to insert and fetch data from dynamodb

execute.py -- executes create table, inserts data, queries data based on different criterias, converts the queried data into xml file and then validates that xml

xml_converter.py -- converts query output to xml files

xml_validator.py -- validates xml against xsd

xsltfiles --

1. books_by_category.xslt contains the xslt template that converts books_by_category.xml to html page
2. books_by_filter.xslt contains the xslt template that converts xml files created after executing various queries to html page. Eg to display all books which have rating equal to 3
3. convert.py contains the python script which helps in executing the xslt template to convert xml file to html page using lxml

output_html will contain the index.html file which is created using xslt(book_by_filter.xslt) for the query executed based on rating, availability count or price

output2_html will contain the index.html file which is created using xslt(books_by_category.xslt) for the query executed to fetch books based by category

book_by_category.xsd is the XML Schema Design for books_by_category.xml

library.xsd is the XML Schema Design for all xml files fetched based on queries on rating,price or availability count like books_by_rating.xml

books_by_category.xml and books_by_rating_equal.xml are xml files created after executing aws PartiQl queries

xml_converter.py is the python script used to convert data fetched from aws queries into xml file using etree python package

xml_validator.py is the python script used to validate xml against xsd using lxml
