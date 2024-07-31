<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:param name="pageTitle" select="'Library Books'"/>

    <xsl:key name="categoryById" match="category" use="id"/>

    <xsl:template match="/">
        <html>
            <head>
                <title>
                    <xsl:value-of select="$pageTitle"/>
                </title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        background-color: #f9f9f9;
                    }
                    table {
                    width: 100%;
                    max-width: 800px;
                    margin: auto;
                    border-collapse: collapse;
                    }
                    table, th, td {
                    border: 1px solid black;
                    }
                    th, td {
                        padding: 8px;
                    }
                    td {
                        text-align: left;
                        vertical-align: top;
                    }
                    th {
                        text-align: center;
                        background-color: #ececec;
                    }
                    .header {
                        background-color: #FF9800;
                        padding: 10px;
                        margin-bottom: 24px;
                    }
                    .title {
                        color: #ffffff;
                        text-align: center;
                        font-weight: bold;
                    }
                </style>
            </head>
            <body>
                <header class="header">
                    <h1 class="title"><xsl:value-of select="$pageTitle"/></h1>
                </header>
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Price</th>
                            <th>Rating</th>
                            <th>In Stock</th>
                            <th>Availability Count</th>
                            <th>Description</th>
                            <th>Category</th>
                            <th>Book Cover</th>
                        </tr>
                    </thead>
                    <tbody>
                        <xsl:for-each select="library/books/book">
                            <xsl:sort select="title"/>
                            <tr>
                                <td>
                                    <xsl:value-of select="title"/>
                                </td>
                                <td>
                                    <xsl:value-of select="price"/>
                                </td>
                                <td>
                                    <xsl:value-of select="rating"/>
                                </td>
                                <td>
                                    <xsl:value-of select="is_in_stock"/>
                                </td>
                                <td>
                                    <xsl:value-of select="availability_count"/>
                                </td>
                                <td>
                                    <xsl:value-of select="description"/>
                                </td>
                                <td>
                                    <xsl:value-of select="key('categoryById', category_id)/name"/>
                                </td>
                                <td>
                                    <img>
                                        <xsl:attribute name="src">
                                            <xsl:value-of select="normalize-space(book_cover_url)"/>
                                        </xsl:attribute>
                                        <xsl:attribute name="alt">
                                            <xsl:value-of select="title"/>
                                        </xsl:attribute>
                                        <xsl:attribute name="width">100</xsl:attribute>
                                    </img>
                                </td>
                            </tr>
                        </xsl:for-each>
                    </tbody>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
