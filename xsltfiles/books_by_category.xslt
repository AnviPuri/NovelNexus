<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- Output HTML -->
  <xsl:output method="html" indent="yes"/>

  <!-- Template to match the root element -->
  <xsl:template match="/categories">
    <html>
      <head>
        <title>Book Categories and Details</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            color: #333;
            margin: 0;
            padding: 0;
          }

          .category-dropdown {
            padding: 4px 8px;
            font-size: 1.2rem;
            background: #ececec;
            border: 1px solid #404040;
            border-radius: 4px;
            cursor: pointer;
          }
          .header {
            background: #FF9800;
            text-align: center;
            color: #ffffff;
            margin: 0;
            margin-bottom: 10px;
            padding: 20px;
          }

          .content, .filters {
            padding: 20px;
          }

          .book-list {
            display: none;
            margin-top: 10px;
          }

          .book-list.open {
            display: flex;
            flex-wrap: wrap;
            gap: 32px;
          }

          .book {
            flex: 45%;
            box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
            border-radius: 4px;
            padding: 12px;
            background-color: #ffffff;

          }

          .book-summary {
            display: flex;
            align-items: start;
            justify-content: center;
            gap: 8px;
            margin-bottom: 8px;
          }

          .book-details {
            display: flex;
            flex-direction: column;
          }

          .book-btn {
            background: 
          }

          .book-description.hidden {
            display: none
          }

          .book-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
          }

         
         
        </style>
        <script>
          function selectBookCategory() {
            
            var listElems = document.querySelectorAll(".book-list")
            listElems.forEach(function(elem) {
              elem.classList.remove("open")
            })
            

            var categoryListId = document.getElementById("category-select").value
            var targetListElem = document.getElementById(categoryListId)
            targetListElem.classList.add("open")
            
          }
         
        </script>
      </head>
      <body>
      <header class="header">
        <h1 >Welcome to the Book Categories Page</h1>
      </header>
        <!-- Iterate over each category -->
        <div class="filters">
        Select Category: 
        <select class="category-dropdown" onchange="selectBookCategory()" id="category-select">
          <xsl:for-each select="category">
            <option class="category">
              <xsl:attribute name="value">
                <xsl:value-of select="book/category_name"/>
              </xsl:attribute>
                <xsl:value-of select="book/category_name"/>
            </option>
          </xsl:for-each>
        </select>
        </div>

      <div class="content">
        <xsl:for-each select="category">
          <div class="book-list open">
            <xsl:attribute name="id">
                <xsl:value-of select="book/category_name"/>
            </xsl:attribute>
            <xsl:for-each select="book">
              <xsl:sort select="title"/>
                  <div class="book" >
                    <div class="book-summary"
                    >
                      <img src="{book_cover_url}" alt="{title}"/>
                      <h3><xsl:value-of select="title"/></h3>
                    </div>
                    <div class="book-details">
                      <div class="book-row">
                        <p><strong>Price:</strong><xsl:value-of select="price"/></p>
                        <p><strong>Rating:</strong> <xsl:value-of select="rating"/></p>
                        <p><strong>In Stock:</strong> <xsl:value-of select="is_in_stock"/></p>
                        <p><strong>Availability Count:</strong> <xsl:value-of select="availability_count"/></p>
                      </div>
                      <div class="book-row book-description">
                        <p><strong>Description:</strong> <xsl:value-of select="description"/></p>
                      </div>
                    </div>
                  </div>
            </xsl:for-each>
          </div>
        </xsl:for-each>
      </div>

      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
